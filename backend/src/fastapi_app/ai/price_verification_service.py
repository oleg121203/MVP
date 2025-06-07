from typing import Dict, List, Optional, Any
import os
import asyncio
import logging
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

import pandas as pd

from ..ai.vector_db_service import VectorDBService

class PriceVerificationService:
    def __init__(self, vector_db_service: VectorDBService):
        self.vector_db_service = vector_db_service
        self.supplier_api_configs = self._load_supplier_configs()
        self.price_discrepancy_threshold = float(os.getenv('PRICE_DISCREPANCY_THRESHOLD', 0.1))  # 10% default
        self.auto_update_threshold = float(os.getenv('AUTO_UPDATE_THRESHOLD', 0.05))  # 5% default
        self.last_run_status = {'last_run': None, 'status': None, 'summary': None}
        self.flagged_discrepancies = []
        self.logger = logging.getLogger(__name__)

    def _load_supplier_configs(self) -> List[Dict]:
        """
        Load supplier API configurations from environment variables or a config file.
        For now, using dummy data as placeholder.
        """
        # Placeholder for real supplier configurations
        return [
            {
                'name': 'DummySupplier1',
                'api_url': os.getenv('SUPPLIER1_API_URL', 'https://api.dummysupplier1.com/prices'),
                'api_key': os.getenv('SUPPLIER1_API_KEY', 'dummy_key_1'),
                'method': 'api',
                'material_id_field': 'id',
                'price_field': 'price_usd',
                'query_param': 'item_id'
            },
            {
                'name': 'DummySupplier2',
                'api_url': os.getenv('SUPPLIER2_API_URL', 'https://www.dummysupplier2.com/product/'),
                'api_key': None,
                'method': 'scrape',
                'material_id_field': 'id',
                'price_selector': '.price-value',
            }
        ]

    async def _fetch_price_from_api(self, supplier: Dict, material_id: str) -> Optional[float]:
        """
        Fetch price data from a supplier API for a given material ID.

        Args:
            supplier: Dictionary with supplier configuration.
            material_id: ID of the material to fetch price for.

        Returns:
            Price in USD if successful, None otherwise.
        """
        async with aiohttp.ClientSession() as session:
            try:
                headers = {'Authorization': f'Bearer {supplier["api_key"]}'} if supplier['api_key'] else {}
                url = f"{supplier['api_url']}?{supplier['query_param']}={material_id}"
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return float(data.get(supplier['price_field'], 0.0))
                    else:
                        self.logger.error(f"API fetch failed for {material_id} from {supplier['name']}: Status {response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"API fetch error for {material_id} from {supplier['name']}: {str(e)}")
                return None

    async def _fetch_price_from_scrape(self, supplier: Dict, material_id: str) -> Optional[float]:
        """
        Scrape price data from a supplier website for a given material ID.

        Args:
            supplier: Dictionary with supplier configuration.
            material_id: ID of the material to fetch price for.

        Returns:
            Price in USD if successful, None otherwise.
        """
        async with aiohttp.ClientSession() as session:
            try:
                url = f"{supplier['api_url']}{material_id}"
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        price_elem = soup.select_one(supplier['price_selector'])
                        if price_elem:
                            price_text = price_elem.text.strip().replace('$', '').replace(',', '')
                            return float(price_text)
                        return None
                    else:
                        self.logger.error(f"Scrape failed for {material_id} from {supplier['name']}: Status {response.status}")
                        return None
            except Exception as e:
                self.logger.error(f"Scrape error for {material_id} from {supplier['name']}: {str(e)}")
                return None

    async def fetch_price(self, material: Dict) -> Optional[Dict]:
        """
        Fetch the latest price for a material from configured suppliers.

        Args:
            material: Dictionary with material data including ID and name for querying.

        Returns:
            Dictionary with supplier name and fetched price if successful, None otherwise.
        """
        material_id = material.get('metadata', {}).get('material_id', '')
        if not material_id:
            self.logger.warning(f"No material ID found for material: {material.get('id', 'unknown')}")
            return None

        for supplier in self.supplier_api_configs:
            price = None
            if supplier['method'] == 'api':
                price = await self._fetch_price_from_api(supplier, material_id)
            elif supplier['method'] == 'scrape':
                price = await self._fetch_price_from_scrape(supplier, material_id)

            if price is not None:
                return {'supplier': supplier['name'], 'price_usd': price}

        return None

    async def verify_prices(self, material_ids: Optional[List[str]] = None, force_update: bool = False) -> Dict:
        """
        Verify prices for materials in the vector database against supplier data.

        Args:
            material_ids: Optional list of material IDs to verify. If None, check all materials.
            force_update: If True, update prices even for large discrepancies without manual review.

        Returns:
            Summary of the verification process including counts of checked, updated, and flagged items.
        """
        start_time = datetime.utcnow().isoformat()
        self.flagged_discrepancies = []  # Reset flagged discrepancies
        summary = {'checked': 0, 'updated': 0, 'flagged': 0}

        # Fetch all materials from vector DB if no specific IDs provided
        if material_ids is None or len(material_ids) == 0:
            materials = self.vector_db_service.fetch_all_vectors()
        else:
            materials = []
            for mat_id in material_ids:
                mat = self.vector_db_service.fetch_vector(mat_id)
                if mat:
                    materials.append(mat)

        # Process each material
        tasks = []
        for material in materials:
            tasks.append(self.fetch_price(material))
            summary['checked'] += 1

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Price fetch failed for material index {i}: {str(result)}")
                continue

            material = materials[i]
            vector_id = material.get('id', 'unknown')
            current_price = material.get('metadata', {}).get('cost_usd', 0.0)

            if result and 'price_usd' in result:
                fetched_price = result['price_usd']
                discrepancy = abs(fetched_price - current_price) / current_price if current_price > 0 else 1.0

                price_history = material.get('metadata', {}).get('price_history', [])
                price_history.append({'date': datetime.utcnow().isoformat(), 'price': fetched_price})

                updated_metadata = {
                    'cost_usd': fetched_price,
                    'price_history': price_history[:10],  # Keep last 10 entries
                    'last_price_update': datetime.utcnow().isoformat(),
                    'price_source': result['supplier']
                }

                if discrepancy <= self.auto_update_threshold or force_update:
                    # Auto update for small changes or if forced
                    self.vector_db_service.update_vector(vector_id, metadata=updated_metadata)
                    summary['updated'] += 1
                    self.logger.info(f"Price updated for {vector_id}: {current_price} -> {fetched_price}")
                elif discrepancy <= self.price_discrepancy_threshold:
                    # Suggest update for moderate changes
                    self.vector_db_service.update_vector(vector_id, metadata=updated_metadata)
                    summary['updated'] += 1
                    self.logger.info(f"Price updated for {vector_id}: {current_price} -> {fetched_price} (moderate change)")
                else:
                    # Flag large discrepancies for manual review
                    self.flagged_discrepancies.append({
                        'vector_id': vector_id,
                        'material_name': material.get('metadata', {}).get('name', 'Unknown'),
                        'current_price_usd': current_price,
                        'fetched_price_usd': fetched_price,
                        'discrepancy_percent': discrepancy * 100,
                        'supplier': result['supplier'],
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    summary['flagged'] += 1
                    self.logger.warning(f"Large price discrepancy flagged for {vector_id}: {current_price} vs {fetched_price}")

        # Update last run status
        self.last_run_status = {
            'last_run': start_time,
            'status': 'success',
            'summary': summary
        }

        return summary

    def get_status(self) -> Dict:
        """
        Get the status of the last price verification run.

        Returns:
            Dictionary with last run timestamp, status, and summary.
        """
        return self.last_run_status

    def get_discrepancies(self) -> List[Dict]:
        """
        Get the list of flagged price discrepancies for manual review.

        Returns:
            List of dictionaries with details of discrepancies.
        """
        return self.flagged_discrepancies

    def resolve_discrepancy(self, vector_id: str, action: str, new_price_usd: Optional[float] = None) -> bool:
        """
        Resolve a flagged price discrepancy based on user input.

        Args:
            vector_id: ID of the vector/material with discrepancy.
            action: Action to take ('update' or 'ignore').
            new_price_usd: New price to set if action is 'update'.

        Returns:
            Boolean indicating if the resolution was successful.
        """
        discrepancy = next((d for d in self.flagged_discrepancies if d['vector_id'] == vector_id), None)
        if not discrepancy:
            self.logger.error(f"Discrepancy not found for vector_id: {vector_id}")
            return False

        if action == 'update':
            if new_price_usd is None:
                new_price_usd = discrepancy['fetched_price_usd']

            material = self.vector_db_service.fetch_vector(vector_id)
            if not material:
                self.logger.error(f"Material not found for vector_id: {vector_id}")
                return False

            price_history = material.get('metadata', {}).get('price_history', [])
            price_history.append({'date': datetime.utcnow().isoformat(), 'price': new_price_usd})

            updated_metadata = {
                'cost_usd': new_price_usd,
                'price_history': price_history[:10],
                'last_price_update': datetime.utcnow().isoformat(),
                'price_source': discrepancy['supplier']
            }
            self.vector_db_service.update_vector(vector_id, metadata=updated_metadata)
            self.logger.info(f"Price updated for {vector_id} to {new_price_usd} after manual review")

        # Remove from flagged list regardless of action
        self.flagged_discrepancies = [d for d in self.flagged_discrepancies if d['vector_id'] != vector_id]
        return True
