import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration
DB_NAME = 'ventai.db'

DATABASE_URL = f'sqlite:///{DB_NAME}'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Example model for migration, add your schemas here
class SupplyChainMetric(Base):
    __tablename__ = 'supply_chain_metrics'
    id = Column(Integer, primary_key=True)
    metric_name = Column(String)
    value = Column(String)
    timestamp = Column(String)

Base.metadata.create_all(engine)
print('Migration completed successfully.')
