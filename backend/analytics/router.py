from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional

from .warehouse import data_warehouse

router = APIRouter()

@router.post("/query")
async def execute_query(
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Execute a raw query against the data warehouse
    Note: In production, this should be secured and limited
    """
    try:
        return data_warehouse.query(query, params)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Query execution failed: {str(e)}"
        )

@router.get("/tables")
async def list_tables() -> Dict[str, Any]:
    """List available tables in the warehouse"""
    try:
        if data_warehouse.get_bigquery():
            # BigQuery implementation
            dataset_ref = data_warehouse.get_bigquery().dataset(settings.gcp_dataset_id)
            tables = list(data_warehouse.get_bigquery().list_tables(dataset_ref))
            return {"tables": [table.table_id for table in tables]}
        else:
            # Traditional SQL implementation
            engine = data_warehouse.get_sql_warehouse()
            with engine.connect() as conn:
                tables = conn.execute(
                    """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    """
                ).fetchall()
                return {"tables": [t[0] for t in tables]}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to list tables: {str(e)}"
        )
