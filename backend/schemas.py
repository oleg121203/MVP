from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Financial Models Schemas
class FinancialProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    status: Optional[str] = 'planned'

class FinancialProjectCreate(FinancialProjectBase):
    pass

class FinancialProject(FinancialProjectBase):
    id: int
    
    class Config:
        orm_mode = True

class FinancialTransactionBase(BaseModel):
    project_id: int
    amount: float
    date: Optional[datetime] = None
    category: Optional[str] = None
    description: Optional[str] = None
    vendor: Optional[str] = None

class FinancialTransactionCreate(FinancialTransactionBase):
    pass

class FinancialTransaction(FinancialTransactionBase):
    id: int
    
    class Config:
        orm_mode = True

class FinancialForecastBase(BaseModel):
    project_id: int
    forecast_date: datetime
    period: str
    forecast_amount: float
    confidence_score: Optional[float] = None

class FinancialForecastCreate(FinancialForecastBase):
    pass

class FinancialForecast(FinancialForecastBase):
    id: int
    
    class Config:
        orm_mode = True
