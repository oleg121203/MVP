from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    status = Column(String, default='planned')
    
    # Relationships
    transactions = relationship("FinancialTransaction", back_populates="project")
    forecasts = relationship("FinancialForecast", back_populates="project")

class FinancialTransaction(Base):
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('financial_projects.id'))
    amount = Column(Float, nullable=False)
    date = Column(DateTime)
    category = Column(String)
    description = Column(String)
    vendor = Column(String)
    
    # Relationships
    project = relationship("FinancialProject", back_populates="transactions")

class FinancialForecast(Base):
    __tablename__ = 'financial_forecasts'
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('financial_projects.id'))
    forecast_date = Column(DateTime)
    period = Column(String)  # weekly, monthly, quarterly
    forecast_amount = Column(Float)
    confidence_score = Column(Float)
    
    # Relationships
    project = relationship("FinancialProject", back_populates="forecasts")
