from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Optional

from ..ai.vector_db_service import VectorDBService

router = APIRouter()
vector_db_service = VectorDBService()

@router.post('/ingest', response_model=Dict)
async def ingest_vector(data: Dict = Body(...)):
    """
    Ingest a single material/component into the vector database.

    Args:
        data: Dictionary containing material/component data.

    Returns:
        Dictionary confirming ingestion with vector ID.
    """
    try:
        vector_id = data.get('material_id')
        if not vector_id:
            raise ValueError("material_id is required")
        
        text = f"{data.get('name', '')} {data.get('description', '')}"
        vector = vector_db_service.generate_embedding(text)
        metadata = {
            'material_id': data['material_id'],
            'name': data.get('name', ''),
            'category': data.get('category', ''),
            'description': data.get('description', ''),
            'specs': data.get('specs', {}),
            'cost_usd': float(data.get('cost_usd', 0.0)),
            'project_id': data.get('project_id', '')
        }
        vector_db_service.upsert_vector(vector_id, vector, metadata)
        return {'status': 'success', 'vector_id': vector_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting vector: {str(e)}")

@router.post('/batch-ingest', response_model=Dict)
async def batch_ingest_vectors(data: List[Dict] = Body(...)):
    """
    Ingest multiple materials/components into the vector database in a batch.

    Args:
        data: List of dictionaries containing material/component data.

    Returns:
        Dictionary summarizing the batch ingestion.
    """
    try:
        vectors_data = []
        for item in data:
            vector_id = item.get('material_id')
            if not vector_id:
                continue
            text = f"{item.get('name', '')} {item.get('description', '')}"
            vector = vector_db_service.generate_embedding(text)
            metadata = {
                'material_id': item['material_id'],
                'name': item.get('name', ''),
                'category': item.get('category', ''),
                'description': item.get('description', ''),
                'specs': item.get('specs', {}),
                'cost_usd': float(item.get('cost_usd', 0.0)),
                'project_id': item.get('project_id', '')
            }
            vectors_data.append({'id': vector_id, 'vector': vector, 'metadata': metadata})
        
        vector_db_service.batch_upsert_vectors(vectors_data)
        return {'status': 'success', 'processed_count': len(vectors_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error batch ingesting vectors: {str(e)}")

@router.post('/search', response_model=List[Dict])
async def search_vectors(search_data: Dict = Body(...)):
    """
    Search for similar materials/components based on a query.

    Args:
        search_data: Dictionary containing query, top_k, and optional filter.

    Returns:
        List of matching results with metadata and similarity scores.
    """
    try:
        query = search_data.get('query', '')
        top_k = search_data.get('top_k', 5)
        filter_data = search_data.get('filter', None)
        results = vector_db_service.search_similar(query, top_k, filter_data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching vectors: {str(e)}")

@router.put('/update', response_model=Dict)
async def update_vector(update_data: Dict = Body(...)):
    """
    Update an existing vector or its metadata.

    Args:
        update_data: Dictionary containing vector_id and optional vector or metadata to update.

    Returns:
        Dictionary confirming the update.
    """
    try:
        vector_id = update_data.get('vector_id')
        if not vector_id:
            raise ValueError("vector_id is required")
        
        vector = update_data.get('vector', None)
        metadata = update_data.get('metadata', None)
        vector_db_service.update_vector(vector_id, vector, metadata)
        return {'status': 'success', 'vector_id': vector_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating vector: {str(e)}")

@router.delete('/delete/{vector_id}', response_model=Dict)
async def delete_vector(vector_id: str):
    """
    Delete a vector from the database.

    Args:
        vector_id: ID of the vector to delete.

    Returns:
        Dictionary confirming the deletion.
    """
    try:
        vector_db_service.delete_vector(vector_id)
        return {'status': 'success', 'vector_id': vector_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting vector: {str(e)}")
