"""
Phase 1.4.1 - Database Query Optimization
Enhanced database models with performance optimizations
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ventai.db')

# Create engine with optimization settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Disable SQL logging for performance
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    """Optimized Project model with analytics indexes"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    client_name = Column(String(255), index=True)
    status = Column(String(50), index=True)
    total_cost = Column(Float, index=True)
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), index=True)
    financial_project_id = Column(Integer, ForeignKey('financial_projects.id'), index=True)  # New field
    
    # Relationships
    financial_project = relationship("FinancialProject", backref="projects")  # New relationship
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_project_status_date', 'status', 'created_at'),
        Index('idx_project_cost_range', 'total_cost'),
        Index('idx_project_client_status', 'client_name', 'status'),
    )

class ProjectAnalytics(Base):
    """Analytics data with optimized queries"""
    __tablename__ = "project_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    metric_name = Column(String(100), index=True)
    metric_value = Column(Float, index=True)
    timestamp = Column(DateTime, default=func.now(), index=True)
    
    # Composite indexes for analytics queries
    __table_args__ = (
        Index('idx_analytics_project_metric', 'project_id', 'metric_name'),
        Index('idx_analytics_time_range', 'timestamp', 'metric_name'),
        Index('idx_analytics_value_search', 'metric_value', 'metric_name'),
    )

class CachedQuery(Base):
    """Query cache for expensive operations"""
    __tablename__ = "cached_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_hash = Column(String(64), unique=True, index=True)
    result_data = Column(Text)
    created_at = Column(DateTime, default=func.now(), index=True)
    expires_at = Column(DateTime, index=True)

# Performance monitoring
class QueryPerformance(Base):
    """Track query performance for optimization"""
    __tablename__ = "query_performance"
    
    id = Column(Integer, primary_key=True)
    query_text = Column(String)
    execution_time = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    query_type = Column(String)
    row_count = Column(Integer)
    
    __table_args__ = (
        Index('idx_query_performance_timestamp', 'timestamp'),
        Index('idx_query_performance_query_type', 'query_type'),
    )

class FinancialProject(Base):
    """Financial project model"""
    __tablename__ = "financial_projects"
    
    id = Column(Integer, primary_key=True, index=True)

def create_tables():
    """Create all tables with optimized indexes"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created with performance optimizations")

def get_db():
    """Database session with proper cleanup"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables with indexes
    Base.metadata.create_all(engine)
    print("✅ Database tables created with performance optimizations")
