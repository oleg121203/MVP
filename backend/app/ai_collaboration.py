import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import numpy as np
import random

logger = logging.getLogger(__name__)

class AICollaboration:
    def __init__(self, collab_dir: str = 'ai_collab_data', config_path: str = 'ai_collaboration_config.json'):
        """
        Initialize Cross-Enterprise AI Collaboration Platform
        """
        self.collab_dir = collab_dir
        self.config_path = config_path
        self.config = self.load_config()
        self.collaboration_spaces = {}
        self.ai_models = {}
        os.makedirs(self.collab_dir, exist_ok=True)
        logger.info("AI Collaboration platform initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load AI collaboration configuration from file or create default if not exists
        """
        default_config = {
            "collaboration": {
                "enabled": True,
                "access_modes": ["public", "private", "restricted"],
                "default_access_mode": "restricted",
                "max_collaboration_spaces": 50,
                "max_participants_per_space": 100,
                "data_sharing": {
                    "enabled": True,
                    "anonymization_enabled": True,
                    "data_retention_days": 365,
                    "sharing_levels": ["none", "metadata_only", "aggregated", "full"],
                    "default_sharing_level": "metadata_only"
                }
            },
            "ai_models": {
                "enabled": True,
                "model_types": {
                    "decision_support": "random_forest_classifier",
                    "forecasting": "random_forest_regressor",
                    "optimization": "random_forest_regressor",
                    "nlp_analysis": "random_forest_classifier"
                },
                "training_interval_days": 7,
                "model_sharing": {
                    "enabled": True,
                    "sharing_levels": ["none", "metadata_only", "model_weights", "full_access"],
                    "default_sharing_level": "metadata_only"
                }
            },
            "integration": {
                "enabled": True,
                "api_access": True,
                "webhook_notifications": True,
                "supported_integrations": ["erp", "crm", "hr", "finance", "marketing", "operations"],
                "default_integrations": ["erp", "crm"]
            },
            "governance": {
                "enabled": True,
                "compliance_checks": ["gdpr", "ccpa", "hipaa", "soc2"],
                "audit_logging": True,
                "approval_workflow": {
                    "enabled": True,
                    "required_for": ["model_deployment", "data_sharing", "collaboration_space_creation"],
                    "default_approvers": ["ai_governance_team", "compliance_officer"]
                }
            },
            "reporting": {
                "enabled": True,
                "report_frequency_hours": 24,
                "report_types": ["collaboration_activity", "model_performance", "data_sharing", "compliance_status"],
                "distribution_channels": ["email", "dashboard"],
                "recipients": ["executives", "ai_team", "compliance_team"]
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded AI collaboration configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading AI collaboration config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default AI collaboration configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default AI collaboration config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved AI collaboration configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving AI collaboration config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def create_collaboration_space(self, space_id: str, name: str, description: str, owner: str, access_mode: Optional[str] = None, data_sharing_level: Optional[str] = None, integrations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new collaboration space for cross-enterprise AI initiatives
        Args:
            space_id: Unique identifier for the collaboration space
            name: Name of the collaboration space
            description: Description of the collaboration space purpose
            owner: Owner of the space (user or team identifier)
            access_mode: Access mode for the space ('public', 'private', 'restricted')
            data_sharing_level: Data sharing level for the space ('none', 'metadata_only', 'aggregated', 'full')
            integrations: List of enterprise systems to integrate with
        Returns:
            Dictionary with creation status
        """
        try:
            if not self.config['collaboration']['enabled']:
                return {
                    "status": "skipped",
                    "message": "AI collaboration is disabled"
                }

            if space_id in self.collaboration_spaces:
                return {
                    "status": "error",
                    "message": f"Collaboration space with ID {space_id} already exists"
                }

            if len(self.collaboration_spaces) >= self.config['collaboration']['max_collaboration_spaces']:
                return {
                    "status": "error",
                    "message": f"Maximum number of collaboration spaces reached ({self.config['collaboration']['max_collaboration_spaces']})"
                }

            access_mode = access_mode or self.config['collaboration']['default_access_mode']
            if access_mode not in self.config['collaboration']['access_modes']:
                return {
                    "status": "error",
                    "message": f"Invalid access mode: {access_mode}. Must be one of {self.config['collaboration']['access_modes']}"
                }

            data_sharing_level = data_sharing_level or self.config['collaboration']['data_sharing']['default_sharing_level']
            if data_sharing_level not in self.config['collaboration']['data_sharing']['sharing_levels']:
                return {
                    "status": "error",
                    "message": f"Invalid data sharing level: {data_sharing_level}. Must be one of {self.config['collaboration']['data_sharing']['sharing_levels']}"
                }

            integrations = integrations or self.config['integration']['default_integrations']
            invalid_integrations = [i for i in integrations if i not in self.config['integration']['supported_integrations']]
            if invalid_integrations:
                return {
                    "status": "error",
                    "message": f"Invalid integrations: {invalid_integrations}. Must be subset of {self.config['integration']['supported_integrations']}"
                }

            space_info = {
                "space_id": space_id,
                "name": name,
                "description": description,
                "owner": owner,
                "access_mode": access_mode,
                "data_sharing_level": data_sharing_level,
                "integrations": integrations,
                "participants": [owner],
                "models": [],
                "datasets": [],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "active"
            }

            self.collaboration_spaces[space_id] = space_info

            # Save to file
            space_file = os.path.join(self.collab_dir, f"space_{space_id}.json")
            try:
                with open(space_file, 'w') as f:
                    json.dump(space_info, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving collaboration space data for {space_id}: {e}")

            logger.info(f"Created collaboration space {space_id} owned by {owner}")
            return {
                "status": "success",
                "space_id": space_id,
                "name": name,
                "description": description,
                "owner": owner,
                "access_mode": access_mode,
                "data_sharing_level": data_sharing_level,
                "integrations": integrations,
                "created_at": space_info['created_at']
            }
        except Exception as e:
            logger.error(f"Error creating collaboration space {space_id}: {e}")
            return {"status": "error", "message": str(e)}

    def join_collaboration_space(self, space_id: str, participant_id: str, access_role: str = "contributor") -> Dict[str, Any]:
        """
        Join a collaboration space as a participant
        Args:
            space_id: ID of the collaboration space to join
            participant_id: ID of the participant joining
            access_role: Role of the participant in the space (e.g., 'contributor', 'viewer')
        Returns:
            Dictionary with join status
        """
        try:
            if space_id not in self.collaboration_spaces:
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} not found"
                }

            space = self.collaboration_spaces[space_id]
            if space['status'] != "active":
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} is not active (status: {space['status']})"
                }

            if len(space['participants']) >= self.config['collaboration']['max_participants_per_space']:
                return {
                    "status": "error",
                    "message": f"Maximum number of participants reached for space {space_id} ({self.config['collaboration']['max_participants_per_space']})"
                }

            if space['access_mode'] == "private":
                return {
                    "status": "error",
                    "message": f"Cannot join private collaboration space {space_id} without explicit invitation"
                }

            if participant_id in space['participants']:
                return {
                    "status": "skipped",
                    "message": f"Participant {participant_id} is already in collaboration space {space_id}"
                }

            # Add participant
            space['participants'].append(participant_id)
            space['updated_at'] = datetime.now().isoformat()

            # Save updated space data
            space_file = os.path.join(self.collab_dir, f"space_{space_id}.json")
            try:
                with open(space_file, 'w') as f:
                    json.dump(space, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving updated collaboration space data for {space_id}: {e}")

            logger.info(f"Participant {participant_id} joined collaboration space {space_id} as {access_role}")
            return {
                "status": "success",
                "space_id": space_id,
                "space_name": space['name'],
                "participant_id": participant_id,
                "access_role": access_role,
                "joined_at": space['updated_at'],
                "total_participants": len(space['participants'])
            }
        except Exception as e:
            logger.error(f"Error joining collaboration space {space_id} for participant {participant_id}: {e}")
            return {"status": "error", "message": str(e)}

    def share_model(self, space_id: str, model_id: str, model_type: str, owner: str, sharing_level: Optional[str] = None, model_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Share an AI model with a collaboration space
        Args:
            space_id: ID of the collaboration space to share model with
            model_id: Unique identifier for the model
            model_type: Type of model ('decision_support', 'forecasting', 'optimization', 'nlp_analysis')
            owner: Owner of the model (user or team identifier)
            sharing_level: Sharing level for the model ('none', 'metadata_only', 'model_weights', 'full_access')
            model_metadata: Metadata about the model (performance metrics, training data, etc.)
        Returns:
            Dictionary with sharing status
        """
        try:
            if not self.config['ai_models']['enabled'] or not self.config['ai_models']['model_sharing']['enabled']:
                return {
                    "status": "skipped",
                    "message": "AI model sharing is disabled"
                }

            if space_id not in self.collaboration_spaces:
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} not found"
                }

            space = self.collaboration_spaces[space_id]
            if space['status'] != "active":
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} is not active (status: {space['status']})"
                }

            if model_type not in self.config['ai_models']['model_types']:
                return {
                    "status": "error",
                    "message": f"Unknown model type: {model_type}. Must be one of {list(self.config['ai_models']['model_types'].keys())}"
                }

            sharing_level = sharing_level or self.config['ai_models']['model_sharing']['default_sharing_level']
            if sharing_level not in self.config['ai_models']['model_sharing']['sharing_levels']:
                return {
                    "status": "error",
                    "message": f"Invalid sharing level: {sharing_level}. Must be one of {self.config['ai_models']['model_sharing']['sharing_levels']}"
                }

            # Check if model already shared with this space
            existing_model = next((m for m in space['models'] if m['model_id'] == model_id), None)
            if existing_model:
                return {
                    "status": "skipped",
                    "message": f"Model {model_id} is already shared with collaboration space {space_id}"
                }

            model_info = {
                "model_id": model_id,
                "model_type": model_type,
                "owner": owner,
                "sharing_level": sharing_level,
                "shared_at": datetime.now().isoformat(),
                "metadata": model_metadata or {},
                "usage_count": 0,
                "last_used": None
            }

            space['models'].append(model_info)
            space['updated_at'] = datetime.now().isoformat()

            # Register model in global model registry if not already present
            if model_id not in self.ai_models:
                self.ai_models[model_id] = {
                    "model_id": model_id,
                    "model_type": model_type,
                    "owner": owner,
                    "created_at": datetime.now().isoformat(),
                    "metadata": model_metadata or {},
                    "shared_with": [space_id]
                }
            else:
                if space_id not in self.ai_models[model_id]['shared_with']:
                    self.ai_models[model_id]['shared_with'].append(space_id)

            # Save updated space data
            space_file = os.path.join(self.collab_dir, f"space_{space_id}.json")
            try:
                with open(space_file, 'w') as f:
                    json.dump(space, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving updated collaboration space data for {space_id}: {e}")

            # Save model registry
            models_file = os.path.join(self.collab_dir, "model_registry.json")
            try:
                with open(models_file, 'w') as f:
                    json.dump(self.ai_models, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving model registry: {e}")

            logger.info(f"Model {model_id} of type {model_type} shared with collaboration space {space_id} at level {sharing_level}")
            return {
                "status": "success",
                "space_id": space_id,
                "space_name": space['name'],
                "model_id": model_id,
                "model_type": model_type,
                "owner": owner,
                "sharing_level": sharing_level,
                "shared_at": model_info['shared_at']
            }
        except Exception as e:
            logger.error(f"Error sharing model {model_id} with collaboration space {space_id}: {e}")
            return {"status": "error", "message": str(e)}

    def share_dataset(self, space_id: str, dataset_id: str, dataset_type: str, owner: str, sharing_level: Optional[str] = None, dataset_metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Share a dataset with a collaboration space
        Args:
            space_id: ID of the collaboration space to share dataset with
            dataset_id: Unique identifier for the dataset
            dataset_type: Type of dataset (e.g., 'customer_data', 'financial_data', 'operational_data')
            owner: Owner of the dataset (user or team identifier)
            sharing_level: Sharing level for the dataset ('none', 'metadata_only', 'aggregated', 'full')
            dataset_metadata: Metadata about the dataset (size, schema, source, etc.)
        Returns:
            Dictionary with sharing status
        """
        try:
            if not self.config['collaboration']['data_sharing']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Data sharing is disabled"
                }

            if space_id not in self.collaboration_spaces:
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} not found"
                }

            space = self.collaboration_spaces[space_id]
            if space['status'] != "active":
                return {
                    "status": "error",
                    "message": f"Collaboration space {space_id} is not active (status: {space['status']})"
                }

            # Check space's data sharing level - cannot share at a level higher than space allows
            space_sharing_level = space['data_sharing_level']
            sharing_level = sharing_level or space_sharing_level
            sharing_levels = self.config['collaboration']['data_sharing']['sharing_levels']
            if sharing_levels.index(sharing_level) > sharing_levels.index(space_sharing_level):
                return {
                    "status": "error",
                    "message": f"Cannot share dataset at level {sharing_level} in space with sharing level {space_sharing_level}"
                }

            if sharing_level not in sharing_levels:
                return {
                    "status": "error",
                    "message": f"Invalid sharing level: {sharing_level}. Must be one of {sharing_levels}"
                }

            # Check if dataset already shared with this space
            existing_dataset = next((d for d in space['datasets'] if d['dataset_id'] == dataset_id), None)
            if existing_dataset:
                return {
                    "status": "skipped",
                    "message": f"Dataset {dataset_id} is already shared with collaboration space {space_id}"
                }

            dataset_info = {
                "dataset_id": dataset_id,
                "dataset_type": dataset_type,
                "owner": owner,
                "sharing_level": sharing_level,
                "shared_at": datetime.now().isoformat(),
                "metadata": dataset_metadata or {},
                "access_count": 0,
                "last_accessed": None
            }

            space['datasets'].append(dataset_info)
            space['updated_at'] = datetime.now().isoformat()

            # Save updated space data
            space_file = os.path.join(self.collab_dir, f"space_{space_id}.json")
            try:
                with open(space_file, 'w') as f:
                    json.dump(space, f, indent=2)
            except Exception as e:
                logger.warning(f"Error saving updated collaboration space data for {space_id}: {e}")

            logger.info(f"Dataset {dataset_id} of type {dataset_type} shared with collaboration space {space_id} at level {sharing_level}")
            return {
                "status": "success",
                "space_id": space_id,
                "space_name": space['name'],
                "dataset_id": dataset_id,
                "dataset_type": dataset_type,
                "owner": owner,
                "sharing_level": sharing_level,
                "shared_at": dataset_info['shared_at']
            }
        except Exception as e:
            logger.error(f"Error sharing dataset {dataset_id} with collaboration space {space_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_collaboration_status(self, space_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get status of collaboration spaces and shared resources
        Args:
            space_id: Optional specific space ID to get status for, if None returns summary of all spaces
        Returns:
            Dictionary with collaboration status information
        """
        try:
            if space_id is None:
                # Summary of all collaboration spaces
                space_summaries = []
                for space_id, space in self.collaboration_spaces.items():
                    space_summaries.append({
                        "space_id": space_id,
                        "name": space['name'],
                        "description": space['description'],
                        "owner": space['owner'],
                        "status": space['status'],
                        "access_mode": space['access_mode'],
                        "data_sharing_level": space['data_sharing_level'],
                        "participant_count": len(space['participants']),
                        "model_count": len(space['models']),
                        "dataset_count": len(space['datasets']),
                        "created_at": space['created_at'],
                        "updated_at": space['updated_at']
                    })

                return {
                    "status": "success",
                    "collaboration_enabled": self.config['collaboration']['enabled'],
                    "total_spaces": len(self.collaboration_spaces),
                    "max_spaces": self.config['collaboration']['max_collaboration_spaces'],
                    "space_summaries": space_summaries
                }
            else:
                # Detailed status for specific space
                if space_id not in self.collaboration_spaces:
                    return {
                        "status": "error",
                        "message": f"Collaboration space {space_id} not found"
                    }

                space = self.collaboration_spaces[space_id]
                return {
                    "status": "success",
                    "space_id": space_id,
                    "name": space['name'],
                    "description": space['description'],
                    "owner": space['owner'],
                    "space_status": space['status'],
                    "access_mode": space['access_mode'],
                    "data_sharing_level": space['data_sharing_level'],
                    "integrations": space['integrations'],
                    "participants": space['participants'],
                    "models": [
                        {
                            "model_id": m['model_id'],
                            "model_type": m['model_type'],
                            "owner": m['owner'],
                            "sharing_level": m['sharing_level'],
                            "shared_at": m['shared_at'],
                            "usage_count": m['usage_count'],
                            "last_used": m['last_used']
                        }
                        for m in space['models']
                    ],
                    "datasets": [
                        {
                            "dataset_id": d['dataset_id'],
                            "dataset_type": d['dataset_type'],
                            "owner": d['owner'],
                            "sharing_level": d['sharing_level'],
                            "shared_at": d['shared_at'],
                            "access_count": d['access_count'],
                            "last_accessed": d['last_accessed']
                        }
                        for d in space['datasets']
                    ],
                    "created_at": space['created_at'],
                    "updated_at": space['updated_at']
                }
        except Exception as e:
            logger.error(f"Error getting collaboration status for space {space_id if space_id else 'all'}: {e}")
            return {"status": "error", "message": str(e)}

# Global AI collaboration instance
ai_collaboration = AICollaboration()
