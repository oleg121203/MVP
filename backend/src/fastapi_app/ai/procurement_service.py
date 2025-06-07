from typing import Dict, List, Optional, Any
import os
import asyncio
import logging
from datetime import datetime, timedelta
import json
import aiohttp
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

from ..ai.vector_db_service import VectorDBService

class ProcurementService:
    def __init__(self, vector_db_service: VectorDBService):
        self.vector_db_service = vector_db_service
        self.google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
        self.weights = {
            'price': float(os.getenv('PROCUREMENT_WEIGHT_PRICE', 0.4)),
            'delivery_time': float(os.getenv('PROCUREMENT_WEIGHT_DELIVERY', 0.3)),
            'proximity': float(os.getenv('PROCUREMENT_WEIGHT_PROXIMITY', 0.2)),
            'reliability': float(os.getenv('PROCUREMENT_WEIGHT_RELIABILITY', 0.1))
        }
        self.logger = logging.getLogger(__name__)

    async def _get_distance_and_time(self, origin: Dict, destination: Dict) -> Dict:
        """
        Calculate distance and estimated travel time between two locations using Google Maps API.

        Args:
            origin: Dictionary with 'lat' and 'lng' for the starting location.
            destination: Dictionary with 'lat' and 'lng' for the destination location.

        Returns:
            Dictionary with distance in kilometers and duration in hours.
        """
        if not self.google_maps_api_key:
            self.logger.warning("Google Maps API key not set, using fallback estimation")
            return {'distance_km': 100.0, 'duration_hours': 24.0}  # Fallback values

        url = (
            f"https://maps.googleapis.com/maps/api/distancematrix/json?"
            f"origins={origin['lat']},{origin['lng']}&"
            f"destinations={destination['lat']},{destination['lng']}&"
            f"mode=driving&key={self.google_maps_api_key}"
        )

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data['status'] == 'OK':
                            element = data['rows'][0]['elements'][0]
                            if element['status'] == 'OK':
                                distance_m = element['distance']['value']
                                duration_s = element['duration']['value']
                                return {
                                    'distance_km': distance_m / 1000.0,
                                    'duration_hours': duration_s / 3600.0
                                }
                        self.logger.error(f"Google Maps API error: {data.get('error_message', 'Unknown error')}")
                        return {'distance_km': 100.0, 'duration_hours': 24.0}
                    else:
                        self.logger.error(f"Google Maps API request failed: Status {response.status}")
                        return {'distance_km': 100.0, 'duration_hours': 24.0}
            except Exception as e:
                self.logger.error(f"Error fetching distance data: {str(e)}")
                return {'distance_km': 100.0, 'duration_hours': 24.0}

    def _normalize_value(self, value: float, min_val: float, max_val: float, inverse: bool = False) -> float:
        """
        Normalize a value to a 0-1 scale for scoring.

        Args:
            value: The value to normalize.
            min_val: Minimum expected value for the range.
            max_val: Maximum expected value for the range.
            inverse: If True, lower values get higher scores (e.g., for price).

        Returns:
            Normalized score between 0 and 1.
        """
        if max_val == min_val:
            return 1.0 if not inverse else 0.0
        normalized = (value - min_val) / (max_val - min_val)
        return 1.0 - normalized if inverse else normalized

    async def analyze_procurement(self, project_data: Dict) -> List[Dict]:
        """
        Analyze project material needs and recommend optimal procurement options.

        Args:
            project_data: Dictionary with project ID, materials needed, project location, and deadline.

        Returns:
            List of recommended suppliers per material with scores and details.
        """
        materials_needed = project_data.get('materials', [])
        project_location = project_data.get('project_location', {'lat': 0.0, 'lng': 0.0})
        deadline = project_data.get('deadline', (datetime.utcnow() + timedelta(days=30)).isoformat())
        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00')) if deadline else datetime.utcnow() + timedelta(days=30)

        recommendations = []
        for mat_req in materials_needed:
            material_id = mat_req.get('material_id')
            quantity = mat_req.get('quantity', 1)

            material = self.vector_db_service.fetch_vector(material_id) if material_id else None
            if not material:
                self.logger.warning(f"Material not found: {material_id}")
                recommendations.append({
                    'material_id': material_id,
                    'quantity': quantity,
                    'error': 'Material not found',
                    'suppliers': []
                })
                continue

            mat_name = material.get('metadata', {}).get('name', 'Unknown')
            mat_desc = material.get('metadata', {}).get('description', '')
            query = f"{mat_name} {mat_desc}".strip()

            # Search for similar materials or suppliers in vector DB
            search_results = self.vector_db_service.search_similar(query=query, top_k=10)

            supplier_options = []
            supplier_tasks = []
            supplier_data = []

            for result in search_results:
                metadata = result.get('metadata', {})
                if 'supplier_id' in metadata and 'cost_usd' in metadata:
                    supplier_info = {
                        'supplier_id': metadata.get('supplier_id'),
                        'material_id': result.get('id'),
                        'name': metadata.get('name', 'Unknown'),
                        'cost_usd': metadata.get('cost_usd', 0.0),
                        'location': metadata.get('location', {'lat': 0.0, 'lng': 0.0}),
                        'delivery_time_days': metadata.get('delivery_time_days', 7.0),
                        'reliability_score': metadata.get('reliability_score', 0.8),
                        'score_similarity': result.get('score', 0.0)
                    }
                    supplier_data.append(supplier_info)
                    supplier_tasks.append(self._get_distance_and_time(project_location, supplier_info['location']))

            if not supplier_tasks:
                recommendations.append({
                    'material_id': material_id,
                    'quantity': quantity,
                    'error': 'No suppliers found',
                    'suppliers': []
                })
                continue

            distance_results = await asyncio.gather(*supplier_tasks, return_exceptions=True)

            for i, dist_data in enumerate(distance_results):
                if isinstance(dist_data, Exception):
                    self.logger.error(f"Distance calculation failed for supplier index {i}: {str(dist_data)}")
                    dist_data = {'distance_km': 100.0, 'duration_hours': 24.0}

                supplier_info = supplier_data[i]
                supplier_info['distance_km'] = dist_data['distance_km']
                supplier_info['duration_hours'] = dist_data['duration_hours']
                supplier_options.append(supplier_info)

            # Score suppliers
            if supplier_options:
                # Get ranges for normalization
                prices = [s['cost_usd'] for s in supplier_options]
                delivery_times = [s['delivery_time_days'] for s in supplier_options]
                distances = [s['distance_km'] for s in supplier_options]
                reliabilities = [s['reliability_score'] for s in supplier_options]

                min_price, max_price = min(prices), max(prices) if prices else (0, 1)
                min_deliv, max_deliv = min(delivery_times), max(delivery_times) if delivery_times else (1, 7)
                min_dist, max_dist = min(distances), max(distances) if distances else (1, 100)
                min_rel, max_rel = min(reliabilities), max(reliabilities) if reliabilities else (0.5, 1.0)

                for supplier in supplier_options:
                    price_score = self._normalize_value(supplier['cost_usd'], min_price, max_price, inverse=True)
                    deliv_score = self._normalize_value(supplier['delivery_time_days'], min_deliv, max_deliv, inverse=True)
                    dist_score = self._normalize_value(supplier['distance_km'], min_dist, max_dist, inverse=True)
                    rel_score = self._normalize_value(supplier['reliability_score'], min_rel, max_rel, inverse=False)

                    total_score = (
                        price_score * self.weights['price'] +
                        deliv_score * self.weights['delivery_time'] +
                        dist_score * self.weights['proximity'] +
                        rel_score * self.weights['reliability']
                    )

                    supplier['total_score'] = total_score
                    supplier['estimated_delivery_date'] = (datetime.utcnow() + timedelta(days=supplier['delivery_time_days'])).isoformat()

                # Sort by total score
                supplier_options.sort(key=lambda x: x['total_score'], reverse=True)

            recommendations.append({
                'material_id': material_id,
                'quantity': quantity,
                'suppliers': supplier_options[:3]  # Top 3 recommendations
            })

        # Check if recommendations meet the deadline
        for rec in recommendations:
            if rec.get('suppliers'):
                for sup in rec['suppliers']:
                    est_delivery = datetime.fromisoformat(sup['estimated_delivery_date'].replace('Z', '+00:00'))
                    sup['meets_deadline'] = est_delivery <= deadline_dt

        return recommendations

    def generate_purchase_order(self, project_data: Dict, selections: List[Dict], format: str = 'pdf') -> Dict:
        """
        Generate a purchase order based on selected procurement options.

        Args:
            project_data: Dictionary with project details.
            selections: List of dictionaries with material and supplier selections.
            format: Output format ('pdf' or 'json').

        Returns:
            Dictionary with URL to generated file or JSON data.
        """
        project_id = project_data.get('project_id', 'PROJ_UNKNOWN')
        order_date = datetime.utcnow().strftime('%Y-%m-%d')
        order_id = f"PO-{project_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        order_details = {
            'order_id': order_id,
            'project_id': project_id,
            'order_date': order_date,
            'items': []
        }

        total_cost = 0.0
        for sel in selections:
            material_id = sel.get('material_id')
            supplier_id = sel.get('supplier_id')
            quantity = sel.get('quantity', 1)

            material = self.vector_db_service.fetch_vector(material_id) if material_id else None
            if material:
                cost_usd = material.get('metadata', {}).get('cost_usd', 0.0)
                name = material.get('metadata', {}).get('name', 'Unknown')
                item_cost = cost_usd * quantity
                total_cost += item_cost

                order_details['items'].append({
                    'material_id': material_id,
                    'name': name,
                    'quantity': quantity,
                    'unit_price_usd': cost_usd,
                    'total_price_usd': item_cost,
                    'supplier_id': supplier_id
                })

        order_details['total_cost_usd'] = total_cost

        if format == 'json':
            return {'format': 'json', 'data': order_details}

        # Generate PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        c = canvas.Canvas(temp_file.name, pagesize=letter)
        width, height = letter

        # Header
        c.setFont('Helvetica-Bold', 16)
        c.drawString(50, height - 50, f"Purchase Order: {order_id}")
        c.setFont('Helvetica', 12)
        c.drawString(50, height - 70, f"Project ID: {project_id}")
        c.drawString(50, height - 90, f"Order Date: {order_date}")

        # Table header
        y_position = height - 130
        c.setFont('Helvetica-Bold', 10)
        c.drawString(50, y_position, "Item")
        c.drawString(150, y_position, "Quantity")
        c.drawString(250, y_position, "Unit Price (USD)")
        c.drawString(350, y_position, "Total Price (USD)")
        c.drawString(450, y_position, "Supplier ID")
        y_position -= 20

        # Table content
        c.setFont('Helvetica', 10)
        for item in order_details['items']:
            c.drawString(50, y_position, item['name'][:20])
            c.drawString(150, y_position, str(item['quantity']))
            c.drawString(250, y_position, f"${item['unit_price_usd']:.2f}")
            c.drawString(350, y_position, f"${item['total_price_usd']:.2f}")
            c.drawString(450, y_position, item['supplier_id'])
            y_position -= 15

        # Total
        y_position -= 20
        c.setFont('Helvetica-Bold', 12)
        c.drawString(350, y_position, f"Total Cost: ${total_cost:.2f}")

        c.save()
        temp_file.close()

        # In a real deployment, this file would be uploaded to a storage service (e.g., S3)
        # For now, return the local path (though in production, return a URL)
        return {'format': 'pdf', 'file_path': temp_file.name, 'order_id': order_id}

    def update_supplier_data(self, supplier_data: List[Dict]) -> Dict:
        """
        Update or add supplier metadata in the vector database.

        Args:
            supplier_data: List of dictionaries with supplier information.

        Returns:
            Confirmation of updated supplier data.
        """
        updated_count = 0
        for data in supplier_data:
            supplier_id = data.get('supplier_id')
            if not supplier_id:
                continue

            # Find vectors associated with this supplier
            # This is a placeholder; in a real system, we'd maintain a mapping or search by supplier_id
            # For now, we'll simulate updating metadata for materials with this supplier
            # In practice, supplier data might be stored separately or as metadata

            # As a simplification, update metadata for any vector with this supplier_id
            vectors = self.vector_db_service.search_similar('', top_k=100, filter={'supplier_id': {'$eq': supplier_id}})
            for vec in vectors:
                vector_id = vec.get('id')
                metadata = vec.get('metadata', {})
                metadata.update({
                    'location': data.get('location', metadata.get('location', {'lat': 0.0, 'lng': 0.0})),
                    'delivery_time_days': data.get('delivery_time_days', metadata.get('delivery_time_days', 7.0)),
                    'reliability_score': data.get('reliability_score', metadata.get('reliability_score', 0.8))
                })
                self.vector_db_service.update_vector(vector_id, metadata=metadata)
                updated_count += 1

            self.logger.info(f"Updated supplier data for {supplier_id} across {updated_count} materials")

        return {'message': f"Updated supplier data for {updated_count} material entries", 'updated': updated_count}
