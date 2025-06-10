import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class APIMarketplace:
    def __init__(self, config_path: str = 'api_marketplace_config.json', keys_dir: str = 'api_keys'):
        """
        Initialize API Marketplace module for third-party developer access
        """
        self.config_path = config_path
        self.keys_dir = keys_dir
        self.config = self.load_config()
        os.makedirs(self.keys_dir, exist_ok=True)
        logger.info("API Marketplace module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load API marketplace configuration from file or create default if not exists
        """
        default_config = {
            "api_endpoints": {
                "public": {
                    "financial_data": {
                        "name": "Financial Data API",
                        "description": "Access financial data and metrics for analysis.",
                        "base_url": "http://localhost:8000/api/v1/public/financial",
                        "methods": ["GET"],
                        "rate_limit": {"requests": 100, "period": "hour"},
                        "required_scopes": ["read:financial"],
                        "documentation_url": "http://localhost:8000/docs/api/public/financial"
                    },
                    "project_data": {
                        "name": "Project Data API",
                        "description": "Access project data and status information.",
                        "base_url": "http://localhost:8000/api/v1/public/projects",
                        "methods": ["GET"],
                        "rate_limit": {"requests": 100, "period": "hour"},
                        "required_scopes": ["read:projects"],
                        "documentation_url": "http://localhost:8000/docs/api/public/projects"
                    }
                },
                "private": {
                    "financial_operations": {
                        "name": "Financial Operations API",
                        "description": "Perform financial operations like transactions.",
                        "base_url": "http://localhost:8000/api/v1/private/financial",
                        "methods": ["GET", "POST", "PUT"],
                        "rate_limit": {"requests": 50, "period": "hour"},
                        "required_scopes": ["read:financial", "write:financial"],
                        "documentation_url": "http://localhost:8000/docs/api/private/financial"
                    },
                    "project_management": {
                        "name": "Project Management API",
                        "description": "Manage projects, tasks, and resources.",
                        "base_url": "http://localhost:8000/api/v1/private/projects",
                        "methods": ["GET", "POST", "PUT", "DELETE"],
                        "rate_limit": {"requests": 50, "period": "hour"},
                        "required_scopes": ["read:projects", "write:projects"],
                        "documentation_url": "http://localhost:8000/docs/api/private/projects"
                    }
                }
            },
            "developer_portal": {
                "url": "http://localhost:8000/developer",
                "registration_enabled": True,
                "api_key_issuance": "manual",  # Options: 'manual', 'automatic'
                "documentation_url": "http://localhost:8000/docs/developer"
            },
            "api_key_settings": {
                "key_length": 32,
                "default_expiry_days": 365,
                "default_scopes": ["read:financial", "read:projects"],
                "max_keys_per_developer": 5
            },
            "rate_limiting": {
                "enabled": True,
                "default_requests_per_hour": 100
            },
            "usage_analytics": {
                "enabled": True,
                "log_directory": "api_usage_logs",
                "retention_days": 90
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded API marketplace configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading marketplace config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default marketplace configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default marketplace config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved API marketplace configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving marketplace config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def generate_api_key(self, developer_id: str, app_name: str, scopes: List[str] = None, 
                         expiry_days: int = None) -> Dict[str, Any]:
        """
        Generate a new API key for a developer
        Args:
            developer_id: Unique identifier for the developer
            app_name: Name of the application for which the key is issued
            scopes: List of access scopes for the key, defaults to config settings
            expiry_days: Number of days until key expiry, defaults to config settings
        Returns:
            Dictionary with API key details if successful
        """
        try:
            import secrets
            import string

            key_settings = self.config['api_key_settings']
            if scopes is None:
                scopes = key_settings.get('default_scopes', [])
            if expiry_days is None:
                expiry_days = key_settings.get('default_expiry_days', 365)

            # Check if developer already has max keys
            developer_keys = self.get_developer_keys(developer_id)
            if len(developer_keys) >= key_settings.get('max_keys_per_developer', 5):
                return {
                    "status": "error",
                    "message": f"Developer {developer_id} has reached maximum number of API keys"
                }

            # Validate scopes
            valid_scopes = []
            for endpoint_type in self.config['api_endpoints'].values():
                for endpoint_data in endpoint_type.values():
                    valid_scopes.extend(endpoint_data.get('required_scopes', []))
            valid_scopes = list(set(valid_scopes))
            invalid_scopes = [s for s in scopes if s not in valid_scopes]
            if invalid_scopes:
                logger.warning(f"Invalid scopes requested for {developer_id}: {invalid_scopes}")
                scopes = [s for s in scopes if s in valid_scopes]
                if not scopes:
                    scopes = key_settings.get('default_scopes', [])

            # Generate API key
            alphabet = string.ascii_letters + string.digits
            api_key = ''.join(secrets.choice(alphabet) for _ in range(key_settings.get('key_length', 32)))

            # Calculate expiry
            expiry_date = datetime.now() + timedelta(days=expiry_days)

            # Store key data
            key_data = {
                "developer_id": developer_id,
                "app_name": app_name,
                "api_key": api_key,
                "scopes": scopes,
                "issued": datetime.now().isoformat(),
                "expires": expiry_date.isoformat(),
                "active": True,
                "usage_stats": {
                    "total_requests": 0,
                    "last_request": None
                }
            }

            key_id = f"{developer_id}_{app_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            key_file = os.path.join(self.keys_dir, f"{key_id}.json")
            with open(key_file, 'w') as f:
                json.dump(key_data, f, indent=2)

            logger.info(f"Generated new API key for developer {developer_id}, app: {app_name}")
            return {
                "status": "success",
                "key_id": key_id,
                "developer_id": developer_id,
                "app_name": app_name,
                "api_key": api_key,
                "scopes": scopes,
                "issued": key_data['issued'],
                "expires": key_data['expires'],
                "message": "Keep this API key secure and do not share it publicly."
            }
        except Exception as e:
            logger.error(f"Error generating API key for {developer_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_developer_keys(self, developer_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all API keys for a specific developer
        Args:
            developer_id: Unique identifier for the developer
        Returns:
            List of dictionaries with key details (excluding the actual API key value for security)
        """
        try:
            keys = []
            for filename in os.listdir(self.keys_dir):
                if filename.endswith('.json') and filename.startswith(f"{developer_id}_"):
                    key_file = os.path.join(self.keys_dir, filename)
                    try:
                        with open(key_file, 'r') as f:
                            key_data = json.load(f)
                            if key_data.get('developer_id') == developer_id:
                                # Exclude the actual API key for security
                                key_info = {
                                    "key_id": filename[:-5],
                                    "app_name": key_data.get('app_name'),
                                    "scopes": key_data.get('scopes', []),
                                    "issued": key_data.get('issued'),
                                    "expires": key_data.get('expires'),
                                    "active": key_data.get('active', False),
                                    "usage_stats": key_data.get('usage_stats', {})
                                }
                                keys.append(key_info)
                    except Exception as e:
                        logger.warning(f"Error reading key file {key_file}: {e}")

            logger.info(f"Retrieved {len(keys)} API keys for developer {developer_id}")
            return keys
        except Exception as e:
            logger.error(f"Error retrieving API keys for {developer_id}: {e}")
            return []

    def revoke_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        Revoke a specific API key
        Args:
            key_id: Unique identifier for the API key to revoke
        Returns:
            Dictionary with revocation status
        """
        try:
            key_file = os.path.join(self.keys_dir, f"{key_id}.json")
            if not os.path.exists(key_file):
                return {"status": "error", "message": f"API key {key_id} not found"}

            with open(key_file, 'r') as f:
                key_data = json.load(f)

            key_data['active'] = False
            key_data['revoked'] = datetime.now().isoformat()

            with open(key_file, 'w') as f:
                json.dump(key_data, f, indent=2)

            logger.info(f"Revoked API key {key_id} for developer {key_data.get('developer_id')}")
            return {
                "status": "success",
                "key_id": key_id,
                "developer_id": key_data.get('developer_id'),
                "app_name": key_data.get('app_name'),
                "revoked_at": key_data['revoked']
            }
        except Exception as e:
            logger.error(f"Error revoking API key {key_id}: {e}")
            return {"status": "error", "message": str(e)}

    def validate_api_key(self, api_key: str, endpoint: str, method: str) -> Dict[str, Any]:
        """
        Validate an API key for a specific endpoint and method
        Args:
            api_key: API key to validate
            endpoint: Target API endpoint being accessed
            method: HTTP method being used (GET, POST, etc.)
        Returns:
            Dictionary with validation status and access details if valid
        """
        try:
            key_data = None
            key_id = None
            for filename in os.listdir(self.keys_dir):
                if filename.endswith('.json'):
                    key_file = os.path.join(self.keys_dir, filename)
                    try:
                        with open(key_file, 'r') as f:
                            data = json.load(f)
                            if data.get('api_key') == api_key:
                                key_data = data
                                key_id = filename[:-5]
                                break
                    except Exception as e:
                        logger.warning(f"Error reading key file {key_file}: {e}")

            if not key_data:
                return {"status": "invalid", "message": "API key not found"}

            if not key_data.get('active', False):
                return {"status": "invalid", "message": "API key has been revoked or is inactive"}

            # Check expiry
            expiry_date = key_data.get('expires')
            if expiry_date and datetime.fromisoformat(expiry_date) < datetime.now():
                return {"status": "invalid", "message": "API key has expired"}

            # Find matching endpoint
            endpoint_type = None
            endpoint_config = None
            for etype, endpoints in self.config['api_endpoints'].items():
                for eid, econfig in endpoints.items():
                    if endpoint.startswith(econfig['base_url']):
                        endpoint_type = etype
                        endpoint_config = econfig
                        break
                if endpoint_config:
                    break

            if not endpoint_config:
                return {"status": "invalid", "message": f"Endpoint {endpoint} not found in API configuration"}

            # Check if method is allowed
            if method.upper() not in endpoint_config.get('methods', []):
                return {
                    "status": "denied",
                    "message": f"Method {method} not allowed for endpoint {endpoint}"
                }

            # Check scopes
            required_scopes = endpoint_config.get('required_scopes', [])
            key_scopes = key_data.get('scopes', [])
            missing_scopes = [s for s in required_scopes if s not in key_scopes]
            if missing_scopes:
                return {
                    "status": "denied",
                    "message": f"API key lacks required scopes: {', '.join(missing_scopes)}"
                }

            # Check rate limits if enabled
            if self.config['rate_limiting'].get('enabled', False):
                rate_limit = endpoint_config.get('rate_limit', 
                                                {"requests": self.config['rate_limiting'].get('default_requests_per_hour', 100), 
                                                 "period": "hour"})
                usage_stats = key_data.get('usage_stats', {"total_requests": 0, "last_request": None})
                current_time = datetime.now()
                last_request_str = usage_stats.get('last_request')
                reset_count = False

                if last_request_str:
                    last_request = datetime.fromisoformat(last_request_str)
                    if rate_limit['period'] == 'hour':
                        reset_time = last_request + timedelta(hours=1)
                    elif rate_limit['period'] == 'day':
                        reset_time = last_request + timedelta(days=1)
                    else:  # minute for testing
                        reset_time = last_request + timedelta(minutes=1)

                    if current_time > reset_time:
                        reset_count = True
                else:
                    reset_count = True

                if reset_count:
                    usage_stats['total_requests'] = 0

                if usage_stats['total_requests'] >= rate_limit['requests']:
                    return {
                        "status": "rate_limited",
                        "message": f"Rate limit exceeded. Limit is {rate_limit['requests']} requests per {rate_limit['period']}",
                        "retry_after": reset_time.isoformat() if 'reset_time' in locals() else 'N/A'
                    }

                # Update usage stats (even though this is before the request is processed, 
                # we'll increment to reserve the slot)
                usage_stats['total_requests'] += 1
                usage_stats['last_request'] = current_time.isoformat()
                key_data['usage_stats'] = usage_stats
                key_file = os.path.join(self.keys_dir, f"{key_id}.json")
                with open(key_file, 'w') as f:
                    json.dump(key_data, f, indent=2)

            logger.info(f"Validated API key {key_id} for developer {key_data.get('developer_id')} accessing {endpoint}")
            return {
                "status": "valid",
                "key_id": key_id,
                "developer_id": key_data.get('developer_id'),
                "app_name": key_data.get('app_name'),
                "scopes": key_data.get('scopes', []),
                "endpoint_type": endpoint_type
            }
        except Exception as e:
            logger.error(f"Error validating API key for endpoint {endpoint}: {e}")
            return {"status": "error", "message": str(e)}

    def get_api_documentation(self, endpoint_id: str = None, endpoint_type: str = 'public') -> Dict[str, Any]:
        """
        Retrieve API documentation for endpoints
        Args:
            endpoint_id: Specific endpoint ID to retrieve documentation for, if None, returns summary of all
            endpoint_type: Type of endpoint ('public' or 'private'), used when endpoint_id is specified
        Returns:
            Dictionary with documentation details
        """
        try:
            if endpoint_id is None:
                # Return summary of all endpoints
                public_endpoints = [
                    {
                        "id": eid,
                        "name": econfig['name'],
                        "description": econfig['description'],
                        "documentation_url": econfig['documentation_url']
                    }
                    for eid, econfig in self.config['api_endpoints']['public'].items()
                ]
                private_endpoints = [
                    {
                        "id": eid,
                        "name": econfig['name'],
                        "description": econfig['description'],
                        "documentation_url": econfig['documentation_url']
                    }
                    for eid, econfig in self.config['api_endpoints']['private'].items()
                ]

                return {
                    "status": "success",
                    "public_endpoints": public_endpoints,
                    "private_endpoints": private_endpoints,
                    "developer_portal_url": self.config['developer_portal']['url'],
                    "general_documentation": self.config['developer_portal']['documentation_url']
                }
            else:
                # Return detailed documentation for specific endpoint
                if endpoint_type not in self.config['api_endpoints']:
                    return {"status": "error", "message": f"Invalid endpoint type: {endpoint_type}"}

                if endpoint_id not in self.config['api_endpoints'][endpoint_type]:
                    return {"status": "error", "message": f"Endpoint {endpoint_id} not found in {endpoint_type} APIs"}

                endpoint_config = self.config['api_endpoints'][endpoint_type][endpoint_id]
                return {
                    "status": "success",
                    "endpoint_id": endpoint_id,
                    "endpoint_type": endpoint_type,
                    "name": endpoint_config['name'],
                    "description": endpoint_config['description'],
                    "base_url": endpoint_config['base_url'],
                    "methods": endpoint_config['methods'],
                    "required_scopes": endpoint_config.get('required_scopes', []),
                    "rate_limit": endpoint_config.get('rate_limit', 
                                                    {"requests": self.config['rate_limiting'].get('default_requests_per_hour', 100),
                                                     "period": "hour"}),
                    "documentation_url": endpoint_config['documentation_url']
                }
        except Exception as e:
            logger.error(f"Error retrieving API documentation: {e}")
            return {"status": "error", "message": str(e)}

    def get_marketplace_status(self) -> Dict[str, Any]:
        """
        Get current status of API marketplace
        """
        try:
            # Count total API keys
            total_keys = len([f for f in os.listdir(self.keys_dir) if f.endswith('.json')])

            # Count unique developers
            developer_ids = set()
            for filename in os.listdir(self.keys_dir):
                if filename.endswith('.json'):
                    key_file = os.path.join(self.keys_dir, filename)
                    try:
                        with open(key_file, 'r') as f:
                            data = json.load(f)
                            dev_id = data.get('developer_id')
                            if dev_id:
                                developer_ids.add(dev_id)
                    except Exception:
                        pass

            return {
                "status": "success",
                "total_api_keys": total_keys,
                "unique_developers": len(developer_ids),
                "public_endpoints": len(self.config['api_endpoints']['public']),
                "private_endpoints": len(self.config['api_endpoints']['private']),
                "developer_portal_url": self.config['developer_portal']['url'],
                "registration_enabled": self.config['developer_portal']['registration_enabled'],
                "rate_limiting_enabled": self.config['rate_limiting']['enabled'],
                "usage_analytics_enabled": self.config['usage_analytics']['enabled']
            }
        except Exception as e:
            logger.error(f"Error getting marketplace status: {e}")
            return {"status": "error", "message": str(e)}

# Global API marketplace instance
api_marketplace = APIMarketplace()
