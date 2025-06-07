import os
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

import requests

class CRMService:
    def __init__(self):
        self.hubspot_api_key = os.getenv('HUBSPOT_API_KEY', '')
        self.base_url = 'https://api.hubapi.com'
        self.logger = logging.getLogger(__name__)
        self.connected = bool(self.hubspot_api_key)
        self.last_sync_push = None
        self.last_sync_pull = None

        # Custom properties in HubSpot for VentAI data
        self.custom_properties = {
            'deal': {
                'project_id': 'project_id',
                'ventilation_type': 'ventilation_type',
                'compliance_status': 'compliance_status',
                'cost_estimate': 'cost_estimate',
                'material_cost': 'material_cost'
            }
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Generic method to make requests to HubSpot API.

        Args:
            method: HTTP method ('GET', 'POST', 'PATCH', etc.)
            endpoint: API endpoint to call.
            data: Data to send in the request body (for POST, PATCH).

        Returns:
            Response data as dictionary.
        """
        if not self.connected:
            raise Exception("HubSpot API key not configured")

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f"Bearer {self.hubspot_api_key}",
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request(method, url, headers=headers, json=data)
            if response.status_code in (200, 201, 207):
                return response.json()
            elif response.status_code == 404:
                self.logger.error(f"Resource not found: {endpoint}")
                raise Exception(f"Resource not found: {response.text}")
            elif response.status_code == 429:
                self.logger.error("Rate limit exceeded")
                raise Exception("Rate limit exceeded, please try again later")
            else:
                self.logger.error(f"HubSpot API error: {response.status_code} - {response.text}")
                raise Exception(f"API error: {response.text}")
        except Exception as e:
            self.logger.error(f"Error making request to HubSpot: {str(e)}")
            raise

    def setup_connection(self, api_key: str) -> Dict:
        """
        Set up connection to HubSpot CRM with provided API key.

        Args:
            api_key: HubSpot API key or token.

        Returns:
            Confirmation of connection status.
        """
        self.hubspot_api_key = api_key
        self.connected = bool(api_key)
        if not self.connected:
            return {'connected': False, 'message': 'No API key provided'}

        # Test connection by fetching a simple endpoint
        try:
            self._make_request('GET', '/crm/v3/objects/deals?limit=1')
            return {'connected': True, 'message': 'Successfully connected to HubSpot', 'crm_type': 'hubspot'}
        except Exception as e:
            self.connected = False
            self.hubspot_api_key = ''
            return {'connected': False, 'message': f"Connection failed: {str(e)}", 'crm_type': 'hubspot'}

    def get_status(self) -> Dict:
        """
        Get the current status of CRM integration.

        Returns:
            Dictionary with connection status and last sync times.
        """
        return {
            'connected': self.connected,
            'crm_type': 'hubspot' if self.connected else 'none',
            'last_sync_push': self.last_sync_push.isoformat() if self.last_sync_push else None,
            'last_sync_pull': self.last_sync_pull.isoformat() if self.last_sync_pull else None
        }

    def sync_projects_push(self, projects: List[Dict]) -> Dict:
        """
        Push VentAI project data to HubSpot as deals.

        Args:
            projects: List of project data dictionaries to sync to HubSpot.

        Returns:
            Summary of synchronization results.
        """
        if not self.connected:
            raise Exception("CRM not connected")

        results = {'success': 0, 'failed': 0, 'details': []}
        for project in projects:
            try:
                project_id = project.get('project_id')
                if not project_id:
                    results['failed'] += 1
                    results['details'].append({'project_id': 'unknown', 'error': 'No project ID provided'})
                    continue

                # Search for existing deal with this project_id
                search_data = {
                    'filterGroups': [{
                        'filters': [{
                            'propertyName': self.custom_properties['deal']['project_id'],
                            'operator': 'EQ',
                            'value': project_id
                        }]
                    }],
                    'limit': 1
                }
                search_resp = self._make_request('POST', '/crm/v3/objects/deals/search', search_data)
                existing_deal = None
                if search_resp.get('total', 0) > 0:
                    existing_deal = search_resp['results'][0]

                # Map VentAI project data to HubSpot deal properties
                deal_data = {
                    'properties': {
                        'dealname': project.get('name', f"Project {project_id}"),
                        'dealstage': self._map_project_status_to_deal_stage(project.get('status', 'Planning')),
                        'amount': str(project.get('cost_estimate', 0.0)),
                        self.custom_properties['deal']['project_id']: project_id,
                        self.custom_properties['deal']['ventilation_type']: project.get('ventilation_type', 'Unknown'),
                        self.custom_properties['deal']['compliance_status']: project.get('compliance_status', 'Not Checked'),
                        self.custom_properties['deal']['cost_estimate']: str(project.get('cost_estimate', 0.0)),
                        self.custom_properties['deal']['material_cost']: str(project.get('material_cost', 0.0))
                    }
                }

                if existing_deal:
                    # Update existing deal
                    deal_id = existing_deal['id']
                    self._make_request('PATCH', f"/crm/v3/objects/deals/{deal_id}", deal_data)
                    results['success'] += 1
                    results['details'].append({'project_id': project_id, 'action': 'updated', 'deal_id': deal_id})
                else:
                    # Create new deal
                    create_resp = self._make_request('POST', '/crm/v3/objects/deals', deal_data)
                    deal_id = create_resp.get('id')
                    results['success'] += 1
                    results['details'].append({'project_id': project_id, 'action': 'created', 'deal_id': deal_id})

            except Exception as e:
                results['failed'] += 1
                results['details'].append({'project_id': project.get('project_id', 'unknown'), 'error': str(e)})
                self.logger.error(f"Failed to sync project {project.get('project_id', 'unknown')}: {str(e)}")

        self.last_sync_push = datetime.utcnow()
        return results

    def sync_projects_pull(self, project_ids: Optional[List[str]] = None) -> Dict:
        """
        Pull project-related data from HubSpot to update VentAI.

        Args:
            project_ids: Optional list of project IDs to sync. If None, sync all deals with project_id.

        Returns:
            Summary of pulled data (placeholder for actual updates).
        """
        if not self.connected:
            raise Exception("CRM not connected")

        results = {'success': 0, 'failed': 0, 'details': []}
        try:
            if project_ids:
                # Sync specific projects
                for proj_id in project_ids:
                    try:
                        search_data = {
                            'filterGroups': [{
                                'filters': [{
                                    'propertyName': self.custom_properties['deal']['project_id'],
                                    'operator': 'EQ',
                                    'value': proj_id
                                }]
                            }],
                            'limit': 1
                        }
                        search_resp = self._make_request('POST', '/crm/v3/objects/deals/search', search_data)
                        if search_resp.get('total', 0) > 0:
                            deal = search_resp['results'][0]
                            # Placeholder: In a real system, update VentAI project with deal data
                            results['success'] += 1
                            results['details'].append({
                                'project_id': proj_id,
                                'deal_id': deal['id'],
                                'deal_stage': deal['properties'].get('dealstage', 'unknown'),
                                'updated': 'placeholder'
                            })
                        else:
                            results['failed'] += 1
                            results['details'].append({'project_id': proj_id, 'error': 'Deal not found'})
                    except Exception as e:
                        results['failed'] += 1
                        results['details'].append({'project_id': proj_id, 'error': str(e)})
            else:
                # Sync all deals with project_id custom property
                search_data = {
                    'filterGroups': [{
                        'filters': [{
                            'propertyName': self.custom_properties['deal']['project_id'],
                            'operator': 'HAS_PROPERTY'
                        }]
                    }],
                    'limit': 100
                }
                search_resp = self._make_request('POST', '/crm/v3/objects/deals/search', search_data)
                for deal in search_resp.get('results', []):
                    proj_id = deal['properties'].get(self.custom_properties['deal']['project_id'], 'unknown')
                    # Placeholder: Update VentAI project
                    results['success'] += 1
                    results['details'].append({
                        'project_id': proj_id,
                        'deal_id': deal['id'],
                        'deal_stage': deal['properties'].get('dealstage', 'unknown'),
                        'updated': 'placeholder'
                    })

        except Exception as e:
            self.logger.error(f"Error pulling data from HubSpot: {str(e)}")
            results['failed'] += len(project_ids or [])
            results['details'].append({'project_id': 'all', 'error': str(e)})

        self.last_sync_pull = datetime.utcnow()
        return results

    def process_webhook(self, webhook_data: Dict) -> Dict:
        """
        Process incoming webhook from HubSpot to update VentAI data in real-time.

        Args:
            webhook_data: Webhook payload from HubSpot.

        Returns:
            Acknowledgment of processed webhook.
        """
        if not self.connected:
            raise Exception("CRM not connected")

        self.logger.info(f"Received webhook: {json.dumps(webhook_data, indent=2)}")
        event_type = webhook_data.get('objectType', 'unknown')
        object_id = webhook_data.get('objectId', 'unknown')
        changes = webhook_data.get('propertyName', 'unknown')

        if event_type == 'deal':
            try:
                deal_resp = self._make_request('GET', f"/crm/v3/objects/deals/{object_id}")
                proj_id = deal_resp['properties'].get(self.custom_properties['deal']['project_id'], 'unknown')
                if proj_id != 'unknown':
                    # Placeholder: Update VentAI project status based on deal stage
                    self.logger.info(f"Updating project {proj_id} based on deal {object_id} change: {changes}")
                    return {
                        'received': True,
                        'message': f"Processed deal update for project {proj_id}",
                        'event': {'project_id': proj_id, 'deal_id': object_id, 'change': changes}
                    }
                else:
                    return {'received': True, 'message': 'Deal not linked to a VentAI project', 'event': {'deal_id': object_id}}
            except Exception as e:
                self.logger.error(f"Error processing webhook for deal {object_id}: {str(e)}")
                return {'received': False, 'message': f"Failed to process webhook: {str(e)}", 'event': {'deal_id': object_id}}
        else:
            return {'received': True, 'message': f"Ignored webhook for unsupported type {event_type}", 'event': {}}

    def _map_project_status_to_deal_stage(self, status: str) -> str:
        """
        Map VentAI project status to HubSpot deal stage.

        Args:
            status: VentAI project status string.

        Returns:
            Corresponding HubSpot deal stage identifier.
        """
        status_map = {
            'Planning': 'appointmentscheduled',
            'In Progress': 'qualifiedtobuy',
            'Completed': 'closedwon',
            'On Hold': 'decisionmakerboughtin',
            'Cancelled': 'closedlost'
        }
        return status_map.get(status, 'appointmentscheduled')
