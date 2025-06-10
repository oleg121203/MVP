import asyncio
import aiohttp
from typing import List, Dict, Any
from datetime import datetime
import logging

from app.database import SessionLocal
from app.models import PriceData

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceDataCollector:
    def __init__(self):
        self.sources = [
            {"name": "Source1", "url": "https://api.example.com/prices1"},
            {"name": "Source2", "url": "https://api.example.com/prices2"},
            {"name": "Source3", "url": "https://api.example.com/prices3"},
        ]
        self.session = None

    async def initialize(self):
        """Initialize the HTTP session for data collection."""
        self.session = aiohttp.ClientSession()
        logger.info("Price Data Collector initialized")

    async def close(self):
        """Close the HTTP session."""
        if self.session:
            await self.session.close()
        logger.info("Price Data Collector session closed")

    async def fetch_data_from_source(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Fetch price data from a single source."""
        try:
            async with self.session.get(source['url']) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Successfully fetched data from {source['name']}")
                    return data
                else:
                    logger.error(f"Failed to fetch data from {source['name']}. Status: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching data from {source['name']}: {str(e)}")
            return []

    async def collect_data(self):
        """Collect price data from all configured sources."""
        if not self.session:
            await self.initialize()

        tasks = [self.fetch_data_from_source(source) for source in self.sources]
        results = await asyncio.gather(*tasks)

        all_data = []
        for source, data in zip(self.sources, results):
            if data:
                all_data.extend(data)
                logger.info(f"Collected {len(data)} price data points from {source['name']}")

        # Store data in database
        await self.store_data(all_data)
        return all_data

    async def store_data(self, data: List[Dict[str, Any]]):
        """Store collected price data in the database."""
        db = SessionLocal()
        try:
            for item in data:
                price_data = PriceData(
                    product_id=item.get('product_id'),
                    price=item.get('price'),
                    timestamp=datetime.now(),
                    source=item.get('source', 'Unknown')
                )
                db.add(price_data)
            db.commit()
            logger.info(f"Stored {len(data)} price data points in the database")
        except Exception as e:
            logger.error(f"Error storing price data: {str(e)}")
            db.rollback()
        finally:
            db.close()

# Usage example
async def main():
    collector = PriceDataCollector()
    await collector.initialize()
    await collector.collect_data()
    await collector.close()

if __name__ == "__main__":
    asyncio.run(main())
