from fastapi import APIRouter, HTTPException, Body, Response
from typing import Dict, List, Optional

from ..ai.crm_service import CRMService

router = APIRouter()
crm_service = CRMService()

@router.post('/setup', response_model=Dict)
async def setup_crm_connection(setup_data: Dict = Body(...)):
    """
    Configures CRM connection settings and initiates authentication.

    Args:
        setup_data: Dictionary containing CRM type and API key or token.

    Returns:
        Confirmation of successful connection setup.
    """
    try:
        crm_type = setup_data.get('crm_type', 'hubspot')
        if crm_type != 'hubspot':
            raise HTTPException(status_code=400, detail="Only HubSpot CRM is supported at this time")
        api_key = setup_data.get('api_key', '')
        if not api_key:
            raise HTTPException(status_code=400, detail="API key is required for HubSpot connection")
        result = crm_service.setup_connection(api_key)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting up CRM connection: {str(e)}")

@router.post('/sync-projects', response_model=Dict)
async def sync_projects(sync_data: Dict = Body(...)):
    """
    Manually triggers synchronization of VentAI projects to CRM or vice versa.

    Args:
        sync_data: Dictionary containing direction ('push' or 'pull') and optional list of project IDs.

    Returns:
        Summary of synchronized projects and any errors.
    """
    try:
        direction = sync_data.get('direction', 'push')
        project_ids = sync_data.get('project_ids', [])
        if direction not in ('push', 'pull'):
            raise HTTPException(status_code=400, detail="Direction must be 'push' or 'pull'")
        if direction == 'push':
            projects = sync_data.get('projects', []) if 'projects' in sync_data else []
            if not projects and not project_ids:
                raise HTTPException(status_code=400, detail="Projects data or project IDs required for push sync")
            # If project_ids are provided but no projects data, placeholder for fetching project data
            # In a real system, fetch project data from a DB using project_ids
            if not projects and project_ids:
                projects = [{'project_id': pid} for pid in project_ids]  # Placeholder
            result = crm_service.sync_projects_push(projects)
        else:
            result = crm_service.sync_projects_pull(project_ids if project_ids else None)
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing projects: {str(e)}")

@router.post('/webhook', response_model=Dict)
async def process_crm_webhook(webhook_data: Dict = Body(...)):
    """
    Receives real-time updates from CRM (e.g., deal stage changes) and updates VentAI accordingly.

    Args:
        webhook_data: Webhook payload from CRM.

    Returns:
        Acknowledgment of received webhook.
    """
    try:
        result = crm_service.process_webhook(webhook_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@router.get('/status', response_model=Dict)
async def get_crm_status():
    """
    Returns the current status of CRM integration.

    Returns:
        Dictionary with connection status, CRM type, and last sync times.
    """
    try:
        status = crm_service.get_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CRM status: {str(e)}")
