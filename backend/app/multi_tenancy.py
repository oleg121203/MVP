import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class MultiTenancyManager:
    def __init__(self, config_path: str = 'multi_tenancy_config.json', tenants_dir: str = 'tenants'):
        """
        Initialize Multi-Tenancy Manager for handling multiple tenant environments
        """
        self.config_path = config_path
        self.tenants_dir = tenants_dir
        self.config = self.load_config()
        os.makedirs(self.tenants_dir, exist_ok=True)
        logger.info("Multi-Tenancy Manager initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load multi-tenancy configuration from file or create default if not exists
        """
        default_config = {
            "tenancy_mode": "schema",  # Options: 'schema', 'database', 'row'
            "default_tenant": "default",
            "tenant_isolation": {
                "data": True,
                "schema": True,
                "cache": True,
                "sessions": True
            },
            "tenant_config": {
                "allow_customization": True,
                "customization_fields": [
                    "theme",
                    "logo_url",
                    "api_endpoints",
                    "feature_flags"
                ],
                "default_feature_flags": {
                    "predictive_analytics": True,
                    "financial_reporting": True,
                    "anomaly_detection": True,
                    "resource_allocation": True,
                    "enterprise_integration": False,
                    "api_marketplace": False
                }
            },
            "resource_limits": {
                "default": {
                    "max_users": 100,
                    "max_projects": 50,
                    "max_api_calls_per_hour": 1000,
                    "max_storage_mb": 10240  # 10GB
                },
                "override_by_plan": {
                    "basic": {
                        "max_users": 10,
                        "max_projects": 5,
                        "max_api_calls_per_hour": 100,
                        "max_storage_mb": 1024  # 1GB
                    },
                    "premium": {
                        "max_users": 500,
                        "max_projects": 200,
                        "max_api_calls_per_hour": 5000,
                        "max_storage_mb": 51200  # 50GB
                    },
                    "enterprise": {
                        "max_users": 1000,
                        "max_projects": 500,
                        "max_api_calls_per_hour": 10000,
                        "max_storage_mb": 102400  # 100GB
                    }
                }
            },
            "database_config": {
                "base_connection_string": "postgresql://user:password@localhost:5432/",
                "schema_prefix": "tenant_",
                "use_dynamic_connection": True
            },
            "cache_config": {
                "redis_prefix": "tenant:",
                "use_separate_redis": False,
                "separate_redis_config": {}
            },
            "tenant_onboarding": {
                "auto_provision": True,
                "default_plan": "basic",
                "welcome_email": True,
                "setup_wizard": True
            },
            "tenants": {}
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded multi-tenancy configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading multi-tenancy config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default multi-tenancy configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default multi-tenancy config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved multi-tenancy configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving multi-tenancy config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def create_tenant(self, tenant_id: str, tenant_name: str, plan: str = None, 
                      custom_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new tenant in the system
        Args:
            tenant_id: Unique identifier for the tenant
            tenant_name: Human-readable name for the tenant
            plan: Subscription plan for the tenant, defaults to config setting
            custom_config: Custom configuration overrides for the tenant
        Returns:
            Dictionary with tenant creation status and details
        """
        try:
            if tenant_id in self.config['tenants']:
                return {
                    "status": "error",
                    "message": f"Tenant {tenant_id} already exists"
                }

            if plan is None:
                plan = self.config['tenant_onboarding'].get('default_plan', 'basic')

            # Validate plan
            available_plans = list(self.config['resource_limits']['override_by_plan'].keys()) + ['default']
            if plan not in available_plans:
                logger.warning(f"Invalid plan {plan} for tenant {tenant_id}, falling back to default")
                plan = self.config['tenant_onboarding'].get('default_plan', 'basic')

            # Determine resource limits based on plan
            if plan == 'default' or plan not in self.config['resource_limits']['override_by_plan']:
                resource_limits = self.config['resource_limits']['default']
            else:
                resource_limits = self.config['resource_limits']['override_by_plan'][plan]

            # Create tenant configuration
            tenant_config = {
                "tenant_id": tenant_id,
                "name": tenant_name,
                "plan": plan,
                "created": datetime.now().isoformat(),
                "active": True,
                "resource_limits": resource_limits,
                "customization": {
                    "theme": "default",
                    "logo_url": "",
                    "api_endpoints": {},
                    "feature_flags": self.config['tenant_config'].get('default_feature_flags', {})
                },
                "database": {
                    "schema": f"{self.config['database_config']['schema_prefix']}{tenant_id}",
                    "connection_string": f"{self.config['database_config']['base_connection_string']}{tenant_id}" if self.config['tenancy_mode'] == 'database' else f"{self.config['database_config']['base_connection_string']}ventai",
                    "provisioned": False
                },
                "cache": {
                    "prefix": f"{self.config['cache_config']['redis_prefix']}{tenant_id}:"
                },
                "statistics": {
                    "user_count": 0,
                    "project_count": 0,
                    "api_calls": 0,
                    "storage_used_mb": 0.0,
                    "last_activity": None
                }
            }

            # Apply custom configuration if provided
            if custom_config and self.config['tenant_config'].get('allow_customization', False):
                for field in self.config['tenant_config']['customization_fields']:
                    if field in custom_config:
                        if field == 'feature_flags':
                            tenant_config['customization']['feature_flags'].update(custom_config.get(field, {}))
                        elif field == 'api_endpoints':
                            tenant_config['customization']['api_endpoints'] = custom_config.get(field, {})
                        else:
                            tenant_config['customization'][field] = custom_config.get(field)

            # Provision tenant resources if auto-provisioning is enabled
            if self.config['tenant_onboarding'].get('auto_provision', True):
                provision_result = self.provision_tenant_resources(tenant_id)
                tenant_config['database']['provisioned'] = provision_result.get('database', {}).get('status') == 'success'

            # Save tenant configuration
            self.config['tenants'][tenant_id] = tenant_config
            tenant_file = os.path.join(self.tenants_dir, f"{tenant_id}.json")
            with open(tenant_file, 'w') as f:
                json.dump(tenant_config, f, indent=2)

            # Save global config with updated tenant list
            self.save_config()

            logger.info(f"Created new tenant {tenant_id} ({tenant_name}) with plan {plan}")
            return {
                "status": "success",
                "tenant_id": tenant_id,
                "name": tenant_name,
                "plan": plan,
                "created": tenant_config['created'],
                "provisioning": provision_result if self.config['tenant_onboarding'].get('auto_provision', True) else "deferred"
            }
        except Exception as e:
            logger.error(f"Error creating tenant {tenant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def provision_tenant_resources(self, tenant_id: str) -> Dict[str, Any]:
        """
        Provision resources for a specific tenant (database schema, etc.)
        Args:
            tenant_id: Unique identifier for the tenant
        Returns:
            Dictionary with provisioning status for each resource type
        """
        try:
            if tenant_id not in self.config['tenants']:
                return {
                    "status": "error",
                    "message": f"Tenant {tenant_id} not found"
                }

            tenant_config = self.config['tenants'][tenant_id]
            logger.info(f"Provisioning resources for tenant {tenant_id} in {self.config['tenancy_mode']} mode")

            results = {
                "database": {},
                "cache": {},
                "storage": {}
            }

            # Database provisioning based on tenancy mode
            if self.config['tenancy_mode'] == 'schema':
                # Create a new schema for the tenant within the same database
                schema_name = tenant_config['database']['schema']
                # In a real implementation, execute SQL to create schema:
                # CREATE SCHEMA IF NOT EXISTS tenant_xxx
                # Set search path for tenant-specific operations
                results['database'] = {
                    "status": "simulated_success",
                    "message": f"Created schema {schema_name} for tenant {tenant_id}",
                    "schema": schema_name
                }
            elif self.config['tenancy_mode'] == 'database':
                # Create a separate database for the tenant
                db_name = tenant_id
                # In a real implementation, execute SQL to create database:
                # CREATE DATABASE tenant_xxx
                results['database'] = {
                    "status": "simulated_success",
                    "message": f"Created database {db_name} for tenant {tenant_id}",
                    "database": db_name,
                    "connection_string": tenant_config['database']['connection_string']
                }
            else:  # row-level tenancy
                # No structural changes needed, data is filtered by tenant_id column
                results['database'] = {
                    "status": "simulated_success",
                    "message": f"Row-level tenancy for tenant {tenant_id}, no provisioning needed"
                }

            # Cache provisioning
            if self.config['cache_config']['use_separate_redis']:
                # Configure a separate Redis instance or database for tenant
                results['cache'] = {
                    "status": "simulated_success",
                    "message": f"Configured separate Redis for tenant {tenant_id}"
                }
            else:
                # Use prefix for tenant isolation within same Redis instance
                results['cache'] = {
                    "status": "simulated_success",
                    "message": f"Configured Redis prefix {tenant_config['cache']['prefix']} for tenant {tenant_id}",
                    "prefix": tenant_config['cache']['prefix']
                }

            # Storage provisioning (for file storage, etc.)
            # Could create tenant-specific directories or buckets
            results['storage'] = {
                "status": "simulated_success",
                "message": f"Configured storage isolation for tenant {tenant_id}"
            }

            # Update tenant config to mark as provisioned
            tenant_config['database']['provisioned'] = True
            self.config['tenants'][tenant_id] = tenant_config
            self.save_config()

            # Save individual tenant file
            tenant_file = os.path.join(self.tenants_dir, f"{tenant_id}.json")
            with open(tenant_file, 'w') as f:
                json.dump(tenant_config, f, indent=2)

            return {
                "status": "success",
                "tenant_id": tenant_id,
                "resources": results,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error provisioning resources for tenant {tenant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_tenant_context(self, tenant_id: str) -> Dict[str, Any]:
        """
        Get context information for a specific tenant to configure services
        Args:
            tenant_id: Unique identifier for the tenant
        Returns:
            Dictionary with tenant context information for service configuration
        """
        try:
            if tenant_id not in self.config['tenants']:
                logger.warning(f"Tenant {tenant_id} not found, using default tenant configuration")
                tenant_id = self.config.get('default_tenant', 'default')
                if tenant_id not in self.config['tenants']:
                    return {
                        "status": "error",
                        "message": f"Default tenant {tenant_id} also not found"
                    }

            tenant_config = self.config['tenants'][tenant_id]

            # Database connection details based on tenancy mode
            if self.config['tenancy_mode'] == 'schema':
                db_context = {
                    "type": "schema",
                    "schema": tenant_config['database']['schema'],
                    "connection_string": tenant_config['database']['connection_string'],
                    "search_path": tenant_config['database']['schema']
                }
            elif self.config['tenancy_mode'] == 'database':
                db_context = {
                    "type": "database",
                    "database": tenant_id,
                    "connection_string": tenant_config['database']['connection_string']
                }
            else:  # row-level
                db_context = {
                    "type": "row",
                    "tenant_id_filter": tenant_id,
                    "connection_string": tenant_config['database']['connection_string']
                }

            # Cache context
            if self.config['cache_config']['use_separate_redis']:
                cache_context = {
                    "type": "separate",
                    "redis_config": self.config['cache_config']['separate_redis_config']
                }
            else:
                cache_context = {
                    "type": "prefix",
                    "prefix": tenant_config['cache']['prefix']
                }

            return {
                "status": "success",
                "tenant_id": tenant_id,
                "name": tenant_config.get('name', tenant_id),
                "active": tenant_config.get('active', False),
                "plan": tenant_config.get('plan', 'unknown'),
                "database_context": db_context,
                "cache_context": cache_context,
                "resource_limits": tenant_config.get('resource_limits', self.config['resource_limits']['default']),
                "feature_flags": tenant_config['customization'].get('feature_flags', {}),
                "customization": {
                    "theme": tenant_config['customization'].get('theme', 'default'),
                    "logo_url": tenant_config['customization'].get('logo_url', ''),
                    "api_endpoints": tenant_config['customization'].get('api_endpoints', {})
                },
                "statistics": tenant_config.get('statistics', {})
            }
        except Exception as e:
            logger.error(f"Error getting tenant context for {tenant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def update_tenant(self, tenant_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update configuration for an existing tenant
        Args:
            tenant_id: Unique identifier for the tenant
            updates: Dictionary with updated configuration values
        Returns:
            Dictionary with update status
        """
        try:
            if tenant_id not in self.config['tenants']:
                return {
                    "status": "error",
                    "message": f"Tenant {tenant_id} not found"
                }

            tenant_config = self.config['tenants'][tenant_id]

            # Validate updates
            allowed_fields = ['name', 'plan', 'active', 'resource_limits', 'customization']
            invalid_fields = [k for k in updates.keys() if k not in allowed_fields]
            if invalid_fields:
                logger.warning(f"Invalid update fields for tenant {tenant_id}: {invalid_fields}")
                for field in invalid_fields:
                    del updates[field]

            # Update plan and resource limits if changed
            if 'plan' in updates and updates['plan'] != tenant_config.get('plan'):
                plan = updates['plan']
                available_plans = list(self.config['resource_limits']['override_by_plan'].keys()) + ['default']
                if plan not in available_plans:
                    logger.warning(f"Invalid plan {plan} for tenant {tenant_id}, ignoring update")
                    del updates['plan']
                else:
                    # Update resource limits based on new plan
                    if plan == 'default' or plan not in self.config['resource_limits']['override_by_plan']:
                        updates['resource_limits'] = self.config['resource_limits']['default']
                    else:
                        updates['resource_limits'] = self.config['resource_limits']['override_by_plan'][plan]
                    logger.info(f"Updated plan for tenant {tenant_id} to {plan}")

            # Update customization if provided
            if 'customization' in updates and self.config['tenant_config'].get('allow_customization', False):
                current_custom = tenant_config.get('customization', {})
                new_custom = updates['customization']
                updated_custom = {}
                for field in self.config['tenant_config']['customization_fields']:
                    if field in new_custom:
                        updated_custom[field] = new_custom[field]
                    elif field in current_custom:
                        updated_custom[field] = current_custom[field]
                updates['customization'] = updated_custom

            # Apply updates
            tenant_config.update(updates)
            self.config['tenants'][tenant_id] = tenant_config

            # Save updated configuration
            tenant_file = os.path.join(self.tenants_dir, f"{tenant_id}.json")
            with open(tenant_file, 'w') as f:
                json.dump(tenant_config, f, indent=2)

            self.save_config()

            logger.info(f"Updated configuration for tenant {tenant_id}")
            return {
                "status": "success",
                "tenant_id": tenant_id,
                "updated_fields": list(updates.keys()),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error updating tenant {tenant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def deactivate_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """
        Deactivate a tenant, suspending access
        Args:
            tenant_id: Unique identifier for the tenant
        Returns:
            Dictionary with deactivation status
        """
        try:
            if tenant_id not in self.config['tenants']:
                return {
                    "status": "error",
                    "message": f"Tenant {tenant_id} not found"
                }

            tenant_config = self.config['tenants'][tenant_id]
            tenant_config['active'] = False
            tenant_config['deactivated'] = datetime.now().isoformat()

            self.config['tenants'][tenant_id] = tenant_config
            tenant_file = os.path.join(self.tenants_dir, f"{tenant_id}.json")
            with open(tenant_file, 'w') as f:
                json.dump(tenant_config, f, indent=2)

            self.save_config()

            logger.info(f"Deactivated tenant {tenant_id}")
            return {
                "status": "success",
                "tenant_id": tenant_id,
                "deactivated_at": tenant_config['deactivated']
            }
        except Exception as e:
            logger.error(f"Error deactivating tenant {tenant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_tenancy_status(self) -> Dict[str, Any]:
        """
        Get current status of multi-tenancy system
        """
        try:
            total_tenants = len(self.config['tenants'])
            active_tenants = sum(1 for t in self.config['tenants'].values() if t.get('active', False))

            plans_distribution = {}
            for tenant in self.config['tenants'].values():
                plan = tenant.get('plan', 'unknown')
                plans_distribution[plan] = plans_distribution.get(plan, 0) + 1

            return {
                "status": "success",
                "tenancy_mode": self.config['tenancy_mode'],
                "total_tenants": total_tenants,
                "active_tenants": active_tenants,
                "plans_distribution": plans_distribution,
                "isolation_settings": self.config['tenant_isolation'],
                "auto_provisioning": self.config['tenant_onboarding'].get('auto_provision', False),
                "default_plan": self.config['tenant_onboarding'].get('default_plan', 'basic'),
                "customization_allowed": self.config['tenant_config'].get('allow_customization', False)
            }
        except Exception as e:
            logger.error(f"Error getting tenancy status: {e}")
            return {"status": "error", "message": str(e)}

# Global multi-tenancy manager instance
multi_tenancy = MultiTenancyManager()
