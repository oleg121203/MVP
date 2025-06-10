from typing import Optional
from pydantic import BaseSettings

class AnalyticsSettings(BaseSettings):
    # Data warehouse connection settings
    warehouse_host: str = "localhost"
    warehouse_port: int = 5432
    warehouse_db: str = "ventai_analytics"
    warehouse_user: str = "analytics_user"
    warehouse_password: Optional[str] = None
    
    # BigQuery settings (for future GCP integration)
    gcp_project_id: Optional[str] = None
    gcp_dataset_id: Optional[str] = None
    
    class Config:
        env_prefix = "ANALYTICS_"
        env_file = ".env"

settings = AnalyticsSettings()
ґ