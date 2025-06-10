from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from .database import Base

class FinancialProject(Base):
    __tablename__ = 'financial_projects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Float)
    actual_cost = Column(Float)
    status = Column(String, default='planned', index=True)
    client_id = Column(Integer, index=True)  # Added for client association
    region = Column(String, index=True)  # Added for regional analysis
    industry = Column(String, index=True)  # Added for industry-specific reporting
    
    # Relationships
    transactions = relationship("FinancialTransaction", back_populates="project")
    forecasts = relationship("FinancialForecast", back_populates="project")
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_financial_project_status', 'status'),
        Index('idx_financial_project_dates', 'start_date', 'end_date'),
        Index('idx_financial_project_region_industry', 'region', 'industry'),
    )

class FinancialTransaction(Base):
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('financial_projects.id'), index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, index=True)
    category = Column(String, index=True)
    description = Column(String)
    vendor = Column(String)
    payment_method = Column(String, index=True)  # Added for payment analysis
    cost_center = Column(String, index=True)  # Added for departmental cost tracking
    
    # Relationships
    project = relationship("FinancialProject", back_populates="transactions")
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_financial_transaction_date', 'date'),
        Index('idx_financial_transaction_category', 'category'),
        Index('idx_financial_transaction_project_date', 'project_id', 'date'),
    )

class FinancialForecast(Base):
    __tablename__ = 'financial_forecasts'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('financial_projects.id'), index=True)
    forecast_date = Column(DateTime, index=True)
    period = Column(String, index=True)  # weekly, monthly, quarterly
    forecast_amount = Column(Float)
    confidence_score = Column(Float)
    forecast_type = Column(String, index=True)  # Added for different forecast models (baseline, optimistic, pessimistic)
    
    # Relationships
    project = relationship("FinancialProject", back_populates="forecasts")
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_financial_forecast_date', 'forecast_date'),
        Index('idx_financial_forecast_period', 'period'),
        Index('idx_financial_forecast_project_date', 'project_id', 'forecast_date'),
    )
