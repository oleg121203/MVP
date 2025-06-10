from typing import Dict, Any, Optional
import sqlalchemy
from sqlalchemy.engine import Engine
from google.cloud import bigquery

from .config import settings

class DataWarehouse:
    """
    Unified interface for data warehouse connections
    Supports both traditional SQL warehouses and BigQuery
    """
    def __init__(self):
        self._engines: Dict[str, Engine] = {}
        self._bigquery_client: Optional[bigquery.Client] = None
    
    def get_sql_warehouse(self) -> Engine:
        """Get connection to traditional SQL data warehouse"""
        if "sql" not in self._engines:
            connection_string = (
                f"postgresql://{settings.warehouse_user}:{settings.warehouse_password}@"
                f"{settings.warehouse_host}:{settings.warehouse_port}/{settings.warehouse_db}"
            )
            self._engines["sql"] = sqlalchemy.create_engine(connection_string)
        return self._engines["sql"]
    
    def get_bigquery(self) -> bigquery.Client:
        """Get connection to Google BigQuery"""
        if not self._bigquery_client and settings.gcp_project_id:
            self._bigquery_client = bigquery.Client(project=settings.gcp_project_id)
        return self._bigquery_client
    
    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a query against the appropriate warehouse
        Automatically detects if query should go to SQL or BigQuery
        """
        if "`" in sql or settings.gcp_project_id:  # BigQuery style
            client = self.get_bigquery()
            if not client:
                raise ValueError("BigQuery client not configured")
            query_job = client.query(sql, job_config=bigquery.QueryJobConfig())
            return query_job.result().to_dataframe()
        else:  # Traditional SQL
            engine = self.get_sql_warehouse()
            with engine.connect() as conn:
                result = conn.execute(sqlalchemy.text(sql), params or {})
                return [dict(row) for row in result]

# Singleton instance
data_warehouse = DataWarehouse()
