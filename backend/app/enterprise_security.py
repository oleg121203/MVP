import logging
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime, timedelta
import secrets
import string
import hashlib
import hmac
import base64

logger = logging.getLogger(__name__)

class EnterpriseSecurity:
    def __init__(self, config_path: str = 'enterprise_security_config.json', keys_dir: str = 'security_keys'):
        """
        Initialize Enterprise Security module for advanced data protection and compliance
        """
        self.config_path = config_path
        self.keys_dir = keys_dir
        self.config = self.load_config()
        os.makedirs(self.keys_dir, exist_ok=True)
        logger.info("Enterprise Security module initialized")

    def load_config(self) -> Dict[str, Any]:
        """
        Load enterprise security configuration from file or create default if not exists
        """
        default_config = {
            "encryption": {
                "algorithm": "AES-256-GCM",
                "key_length": 32,
                "key_rotation_days": 90,
                "active_key_id": "default",
                "keys": {
                    "default": {
                        "id": "default",
                        "generated": "2025-06-11T00:00:00Z",
                        "expires": "2025-09-09T00:00:00Z",
                        "key_file": "default_encryption_key.bin"
                    }
                },
                "data_types": {
                    "sensitive_fields": [
                        "credit_card_number",
                        "ssn",
                        "bank_account",
                        "api_key",
                        "password",
                        "personal_health_information"
                    ],
                    "pii_fields": [
                        "name",
                        "email",
                        "phone",
                        "address",
                        "date_of_birth"
                    ]
                }
            },
            "access_control": {
                "rbac_enabled": True,
                "abac_enabled": False,
                "default_policy": "deny",
                "roles": {
                    "admin": {
                        "permissions": ["all"],
                        "description": "Administrator with full access"
                    },
                    "manager": {
                        "permissions": ["read:all", "write:projects", "write:financial", "delete:limited"],
                        "description": "Manager with project and financial management capabilities"
                    },
                    "analyst": {
                        "permissions": ["read:all", "write:reports"],
                        "description": "Analyst with read access and report creation"
                    },
                    "developer": {
                        "permissions": ["read:api", "write:api", "access:developer_portal"],
                        "description": "Developer with API access"
                    },
                    "viewer": {
                        "permissions": ["read:limited"],
                        "description": "Viewer with limited read-only access"
                    }
                },
                "attribute_rules": {
                    "department": {
                        "finance": ["read:financial", "write:financial"],
                        "engineering": ["read:projects", "write:projects", "read:technical"],
                        "marketing": ["read:campaigns", "write:campaigns"]
                    },
                    "clearance": {
                        "high": ["read:sensitive", "write:sensitive"],
                        "medium": ["read:pii"],
                        "low": []
                    }
                }
            },
            "audit_logging": {
                "enabled": True,
                "log_directory": "audit_logs",
                "retention_days": 365,
                "log_fields": [
                    "timestamp",
                    "user_id",
                    "tenant_id",
                    "action",
                    "resource",
                    "status",
                    "ip_address",
                    "user_agent"
                ],
                "log_sensitive_actions": True,
                "log_failed_attempts": True
            },
            "compliance": {
                "standards": {
                    "gdpr": {
                        "enabled": True,
                        "data_subject_rights": ["access", "rectification", "erasure", "restriction", "objection", "portability"],
                        "consent_management": True,
                        "data_breach_notification_hours": 72
                    },
                    "ccpa": {
                        "enabled": True,
                        "consumer_rights": ["know", "delete", "opt_out"],
                        "business_obligations": ["disclosure", "non_discrimination"]
                    },
                    "hipaa": {
                        "enabled": False,
                        "safeguards": ["administrative", "physical", "technical"],
                        "phi_fields": ["personal_health_information"]
                    },
                    "pci_dss": {
                        "enabled": True,
                        "requirements": ["protect_cardholder_data", "encrypt_transmission", "restrict_access"],
                        "cardholder_fields": ["credit_card_number", "card_expiry", "cvv"]
                    },
                    "iso_27001": {
                        "enabled": False,
                        "controls": ["information_security_policies", "access_control", "incident_management"]
                    }
                },
                "data_retention": {
                    "default_retention_days": 1825,  # 5 years
                    "pii_retention_days": 1095,     # 3 years
                    "financial_retention_days": 2555 # 7 years
                },
                "data_residency": {
                    "enabled": False,
                    "allowed_regions": ["EU", "US"],
                    "default_region": "EU"
                }
            },
            "data_loss_prevention": {
                "enabled": True,
                "rules": {
                    "block_sensitive_export": {
                        "enabled": True,
                        "fields": ["credit_card_number", "ssn", "bank_account"],
                        "channels": ["email", "file_download", "api"],
                        "action": "block_and_notify"
                    },
                    "mask_pii_in_logs": {
                        "enabled": True,
                        "fields": ["name", "email", "phone", "address"],
                        "mask_with": "[REDACTED]"
                    },
                    "prevent_unauthorized_access": {
                        "enabled": True,
                        "sensitivity_levels": ["sensitive", "confidential"],
                        "action": "block_and_log"
                    }
                },
                "watermarking": {
                    "enabled": False,
                    "text": "CONFIDENTIAL - {tenant_id} - {date}",
                    "apply_to": ["reports", "exports"]
                }
            },
            "threat_detection": {
                "enabled": True,
                "brute_force_protection": {
                    "max_attempts": 5,
                    "lockout_duration_minutes": 15,
                    "track_by": ["ip", "username"]
                },
                "anomaly_detection": {
                    "enabled": True,
                    "sensitivity": "medium",  # Options: low, medium, high
                    "monitor": ["login_locations", "access_patterns", "data_volume"]
                },
                "ddos_protection": {
                    "enabled": True,
                    "rate_limit_per_ip": {"requests": 100, "period": "minute"},
                    "action": "temporary_block"
                }
            },
            "session_management": {
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 3,
                "secure_cookies": True,
                "cookie_attributes": {
                    "http_only": True,
                    "secure": True,
                    "same_site": "strict"
                }
            }
        }

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded enterprise security configuration from file")
                    return config
            except Exception as e:
                logger.error(f"Error loading security config: {e}")
                return default_config
        else:
            # Save default config to file
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default security configuration at {self.config_path}")
            except Exception as e:
                logger.error(f"Error creating default security config: {e}")
            return default_config

    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Save current configuration to file
        """
        config_to_save = config if config else self.config
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            logger.info("Saved enterprise security configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving security config: {e}")
            return False

    def update_config(self, updates: Dict[str, Any]) -> bool:
        """
        Update configuration with new values and save
        """
        self.config.update(updates)
        return self.save_config()

    def generate_encryption_key(self, key_id: str = None, key_length: int = None) -> Dict[str, Any]:
        """
        Generate a new encryption key for data protection
        Args:
            key_id: Identifier for the new key, auto-generated if None
            key_length: Length of the key in bytes, defaults to config setting
        Returns:
            Dictionary with key generation status and details
        """
        try:
            if key_length is None:
                key_length = self.config['encryption'].get('key_length', 32)

            if key_id is None:
                key_id = f"key_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            if key_id in self.config['encryption']['keys']:
                return {
                    "status": "error",
                    "message": f"Key ID {key_id} already exists"
                }

            # Generate secure random key
            new_key = secrets.token_bytes(key_length)

            # Calculate expiry based on rotation policy
            rotation_days = self.config['encryption'].get('key_rotation_days', 90)
            expiry_date = datetime.now() + timedelta(days=rotation_days)

            # Save key to file
            key_file = os.path.join(self.keys_dir, f"{key_id}_encryption_key.bin")
            with open(key_file, 'wb') as f:
                f.write(new_key)

            # Update configuration
            key_info = {
                "id": key_id,
                "generated": datetime.now().isoformat(),
                "expires": expiry_date.isoformat(),
                "key_file": os.path.basename(key_file)
            }
            self.config['encryption']['keys'][key_id] = key_info

            # Optionally set as active key
            if self.config['encryption']['active_key_id'] == 'default':
                self.config['encryption']['active_key_id'] = key_id

            self.save_config()

            logger.info(f"Generated new encryption key {key_id}")
            return {
                "status": "success",
                "key_id": key_id,
                "generated": key_info['generated'],
                "expires": key_info['expires'],
                "key_length": key_length,
                "key_file": key_file
            }
        except Exception as e:
            logger.error(f"Error generating encryption key: {e}")
            return {"status": "error", "message": str(e)}

    def encrypt_data(self, data: str, key_id: str = None) -> Dict[str, Any]:
        """
        Encrypt sensitive data using the specified or active key
        Args:
            data: Data to encrypt
            key_id: ID of encryption key to use, defaults to active key
        Returns:
            Dictionary with encrypted data and metadata
        """
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            if key_id is None:
                key_id = self.config['encryption']['active_key_id']

            if key_id not in self.config['encryption']['keys']:
                return {
                    "status": "error",
                    "message": f"Encryption key {key_id} not found"
                }

            key_info = self.config['encryption']['keys'][key_id]
            key_file = os.path.join(self.keys_dir, key_info['key_file'])

            if not os.path.exists(key_file):
                return {
                    "status": "error",
                    "message": f"Encryption key file for {key_id} not found"
                }

            with open(key_file, 'rb') as f:
                raw_key = f.read()

            # Derive a Fernet key from the raw key using PBKDF2
            salt = b'fixed_salt_for_determinism'  # In production, use a random salt per encryption
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(raw_key))
            fernet = Fernet(key)

            # Encrypt the data
            encrypted_data = fernet.encrypt(data.encode())

            logger.info(f"Encrypted data with key {key_id}")
            return {
                "status": "success",
                "encrypted_data": encrypted_data.decode(),
                "key_id": key_id,
                "encryption_algorithm": self.config['encryption'].get('algorithm', 'AES-256-GCM'),
                "timestamp": datetime.now().isoformat(),
                "salt": base64.b64encode(salt).decode()  # Store salt with metadata in production
            }
        except Exception as e:
            logger.error(f"Error encrypting data: {e}")
            return {"status": "error", "message": str(e)}

    def decrypt_data(self, encrypted_data: str, key_id: str = None, salt: str = None) -> Dict[str, Any]:
        """
        Decrypt data that was encrypted with our encryption keys
        Args:
            encrypted_data: Encrypted data to decrypt
            key_id: ID of encryption key used, defaults to active key
            salt: Base64-encoded salt used during encryption, if applicable
        Returns:
            Dictionary with decrypted data if successful
        """
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            if key_id is None:
                key_id = self.config['encryption']['active_key_id']

            if key_id not in self.config['encryption']['keys']:
                return {
                    "status": "error",
                    "message": f"Encryption key {key_id} not found"
                }

            key_info = self.config['encryption']['keys'][key_id]
            key_file = os.path.join(self.keys_dir, key_info['key_file'])

            if not os.path.exists(key_file):
                return {
                    "status": "error",
                    "message": f"Encryption key file for {key_id} not found"
                }

            with open(key_file, 'rb') as f:
                raw_key = f.read()

            # Derive the Fernet key using the same salt
            if salt is None:
                salt_bytes = b'fixed_salt_for_determinism'
            else:
                salt_bytes = base64.b64decode(salt)

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(raw_key))
            fernet = Fernet(key)

            # Decrypt the data
            decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()

            logger.info(f"Decrypted data with key {key_id}")
            return {
                "status": "success",
                "decrypted_data": decrypted_data,
                "key_id": key_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error decrypting data: {e}")
            return {"status": "error", "message": str(e)}

    def check_access(self, user_id: str, action: str, resource: str, 
                    user_attributes: Dict[str, Any] = None, 
                    tenant_id: str = None) -> Dict[str, Any]:
        """
        Check if a user has permission to perform an action on a resource
        Args:
            user_id: Identifier for the user
            action: Action being attempted (e.g., 'read', 'write', 'delete')
            resource: Resource being accessed (e.g., 'financial', 'projects')
            user_attributes: Dictionary of user attributes for ABAC checks
            tenant_id: Tenant context for the access request
        Returns:
            Dictionary with access decision and rationale
        """
        try:
            # Get user role - in a real system, this would come from a user database
            # For simulation, extract from user_attributes or default to 'viewer'
            user_role = user_attributes.get('role', 'viewer') if user_attributes else 'viewer'

            # Check if role exists in configuration
            if user_role not in self.config['access_control']['roles']:
                logger.warning(f"Unknown role {user_role} for user {user_id}, defaulting to viewer")
                user_role = 'viewer'

            role_config = self.config['access_control']['roles'][user_role]
            role_permissions = role_config.get('permissions', [])

            # Construct the permission being checked
            permission_needed = f"{action}:{resource}"

            # Check RBAC permissions if enabled
            if self.config['access_control']['rbac_enabled']:
                # Check for 'all' permission
                if 'all' in role_permissions:
                    logger.info(f"User {user_id} granted access to {action} {resource} by 'all' permission")
                    return {
                        "status": "granted",
                        "user_id": user_id,
                        "role": user_role,
                        "action": action,
                        "resource": resource,
                        "reason": "Role has full access with 'all' permission",
                        "decision_by": "rbac"
                    }

                # Check for specific permission
                if permission_needed in role_permissions:
                    logger.info(f"User {user_id} granted access to {action} {resource} by specific RBAC permission")
                    return {
                        "status": "granted",
                        "user_id": user_id,
                        "role": user_role,
                        "action": action,
                        "resource": resource,
                        "reason": f"Role {user_role} has specific permission {permission_needed}",
                        "decision_by": "rbac"
                    }

                # Check for wildcard permissions like 'read:all'
                action_all = f"{action}:all"
                if action_all in role_permissions:
                    logger.info(f"User {user_id} granted access to {action} {resource} by wildcard RBAC permission")
                    return {
                        "status": "granted",
                        "user_id": user_id,
                        "role": user_role,
                        "action": action,
                        "resource": resource,
                        "reason": f"Role {user_role} has wildcard permission {action_all}",
                        "decision_by": "rbac"
                    }

            # Check ABAC (Attribute-Based Access Control) if enabled
            if self.config['access_control']['abac_enabled'] and user_attributes:
                for attr_name, attr_config in self.config['access_control']['attribute_rules'].items():
                    if attr_name in user_attributes:
                        user_attr_value = user_attributes[attr_name]
                        if user_attr_value in attr_config:
                            attr_permissions = attr_config[user_attr_value]
                            if permission_needed in attr_permissions:
                                logger.info(f"User {user_id} granted access to {action} {resource} by ABAC rule")
                                return {
                                    "status": "granted",
                                    "user_id": user_id,
                                    "role": user_role,
                                    "action": action,
                                    "resource": resource,
                                    "reason": f"Attribute {attr_name}={user_attr_value} grants permission {permission_needed}",
                                    "decision_by": "abac",
                                    "attribute": {attr_name: user_attr_value}
                                }
                            if f"{action}:all" in attr_permissions:
                                logger.info(f"User {user_id} granted access to {action} {resource} by wildcard ABAC rule")
                                return {
                                    "status": "granted",
                                    "user_id": user_id,
                                    "role": user_role,
                                    "action": action,
                                    "resource": resource,
                                    "reason": f"Attribute {attr_name}={user_attr_value} grants wildcard permission {action}:all",
                                    "decision_by": "abac",
                                    "attribute": {attr_name: user_attr_value}
                                }

            # If no permissions matched and default policy is deny, access is denied
            default_policy = self.config['access_control'].get('default_policy', 'deny')
            if default_policy == 'deny':
                logger.warning(f"User {user_id} denied access to {action} {resource} by default deny policy")
                return {
                    "status": "denied",
                    "user_id": user_id,
                    "role": user_role,
                    "action": action,
                    "resource": resource,
                    "reason": "Access denied by default policy; no matching permissions found",
                    "decision_by": "default_policy"
                }
            else:
                logger.info(f"User {user_id} granted access to {action} {resource} by default allow policy")
                return {
                    "status": "granted",
                    "user_id": user_id,
                    "role": user_role,
                    "action": action,
                    "resource": resource,
                    "reason": "Access granted by default allow policy",
                    "decision_by": "default_policy"
                }
        except Exception as e:
            logger.error(f"Error checking access for user {user_id}: {e}")
            return {"status": "error", "message": str(e)}

    def log_audit_event(self, user_id: str, action: str, resource: str, status: str, 
                       tenant_id: str = None, ip_address: str = None, 
                       user_agent: str = None, details: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Log an audit event for security tracking
        Args:
            user_id: Identifier for the user performing the action
            action: Action performed (e.g., 'login', 'access', 'modify')
            resource: Resource involved in the action
            status: Outcome of the action ('success', 'failure', 'denied')
            tenant_id: Tenant context for the event
            ip_address: IP address of the user
            user_agent: User agent string of the client
            details: Additional details about the event
        Returns:
            Dictionary with logging status
        """
        try:
            if not self.config['audit_logging']['enabled']:
                return {
                    "status": "skipped",
                    "message": "Audit logging is disabled"
                }

            event = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "tenant_id": tenant_id if tenant_id else "N/A",
                "action": action,
                "resource": resource,
                "status": status,
                "ip_address": ip_address if ip_address else "N/A",
                "user_agent": user_agent if user_agent else "N/A",
                "details": details if details else {}
            }

            # Create log directory if it doesn't exist
            log_dir = self.config['audit_logging'].get('log_directory', 'audit_logs')
            os.makedirs(log_dir, exist_ok=True)

            # Create log file name based on date
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = os.path.join(log_dir, f"audit_{date_str}.log")

            # Write event to log file
            with open(log_file, 'a') as f:
                json.dump(event, f)
                f.write('\n')  # Add newline after each JSON object for readability

            logger.info(f"Logged audit event: {action} on {resource} by {user_id} - {status}")
            return {
                "status": "success",
                "event_id": f"event_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "timestamp": event['timestamp'],
                "action": action,
                "resource": resource,
                "user_id": user_id
            }
        except Exception as e:
            logger.error(f"Error logging audit event for {user_id}: {e}")
            return {"status": "error", "message": str(e)}

    def check_compliance(self, standard: str, tenant_id: str = None) -> Dict[str, Any]:
        """
        Check compliance status for a specific standard
        Args:
            standard: Compliance standard to check (e.g., 'gdpr', 'ccpa')
            tenant_id: Tenant context for compliance check
        Returns:
            Dictionary with compliance status and requirements
        """
        try:
            standard = standard.lower()
            if standard not in self.config['compliance']['standards']:
                return {
                    "status": "error",
                    "message": f"Unknown compliance standard: {standard}"
                }

            standard_config = self.config['compliance']['standards'][standard]
            if not standard_config.get('enabled', False):
                return {
                    "status": "not_applicable",
                    "standard": standard.upper(),
                    "message": f"Compliance with {standard.upper()} is not enabled in configuration"
                }

            # In a real system, this would perform actual checks against data handling practices,
            # encryption status, access controls, audit logs, etc.
            # For simulation, return a mock compliance report

            compliance_report = {
                "status": "simulated_compliant",
                "standard": standard.upper(),
                "checked_at": datetime.now().isoformat(),
                "tenant_id": tenant_id if tenant_id else "N/A",
                "requirements": {},
                "issues": []
            }

            if standard == 'gdpr':
                compliance_report['requirements'] = {
                    "data_subject_rights": standard_config['data_subject_rights'],
                    "consent_management": standard_config['consent_management'],
                    "data_breach_notification": f"Within {standard_config['data_breach_notification_hours']} hours"
                }
                # Simulated check
                compliance_report['issues'] = []

            elif standard == 'ccpa':
                compliance_report['requirements'] = {
                    "consumer_rights": standard_config['consumer_rights'],
                    "business_obligations": standard_config['business_obligations']
                }
                compliance_report['issues'] = []

            elif standard == 'hipaa':
                compliance_report['requirements'] = {
                    "safeguards": standard_config['safeguards'],
                    "phi_protection": "Encryption and access controls for PHI"
                }
                compliance_report['issues'] = []

            elif standard == 'pci_dss':
                compliance_report['requirements'] = {
                    "cardholder_data_protection": standard_config['requirements']
                }
                compliance_report['issues'] = []

            elif standard == 'iso_27001':
                compliance_report['requirements'] = {
                    "controls": standard_config['controls']
                }
                compliance_report['issues'] = []

            logger.info(f"Generated compliance report for {standard.upper()} (Tenant: {tenant_id if tenant_id else 'N/A'})")
            return compliance_report
        except Exception as e:
            logger.error(f"Error checking compliance for {standard}: {e}")
            return {"status": "error", "message": str(e)}

    def handle_data_subject_request(self, request_type: str, user_id: str, tenant_id: str = None, 
                                  additional_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle a data subject request under GDPR or other privacy regulations
        Args:
            request_type: Type of request ('access', 'rectification', 'erasure', etc.)
            user_id: Identifier for the data subject
            tenant_id: Tenant context for the request
            additional_data: Additional information for processing the request
        Returns:
            Dictionary with request handling status
        """
        try:
            # Check if GDPR or similar standard is enabled
            gdpr_enabled = self.config['compliance']['standards']['gdpr'].get('enabled', False)
            ccpa_enabled = self.config['compliance']['standards']['ccpa'].get('enabled', False)

            if not gdpr_enabled and not ccpa_enabled:
                return {
                    "status": "not_applicable",
                    "message": "Privacy compliance features (GDPR/CCPA) are not enabled"
                }

            request_type = request_type.lower()
            if gdpr_enabled:
                if request_type not in self.config['compliance']['standards']['gdpr']['data_subject_rights']:
                    return {
                        "status": "error",
                        "message": f"Invalid GDPR request type: {request_type}"
                    }
            elif ccpa_enabled:
                ccpa_rights = self.config['compliance']['standards']['ccpa']['consumer_rights']
                # Map GDPR terms to CCPA terms for simplicity
                rights_mapping = {
                    "access": "know",
                    "erasure": "delete",
                    "objection": "opt_out"
                }
                mapped_type = rights_mapping.get(request_type, request_type)
                if mapped_type not in ccpa_rights:
                    return {
                        "status": "error",
                        "message": f"Invalid CCPA request type: {mapped_type}"
                    }
                request_type = mapped_type

            # In a real implementation, this would:
            # 1. Log the request
            # 2. Authenticate the data subject
            # 3. Process the request based on type (e.g., gather data for access, delete for erasure)
            # 4. Record the fulfillment for compliance
            # For simulation, log a simulated handling

            request_id = f"dsr_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            handling_result = {
                "status": "request_received",
                "request_id": request_id,
                "request_type": request_type,
                "user_id": user_id,
                "tenant_id": tenant_id if tenant_id else "N/A",
                "received_at": datetime.now().isoformat(),
                "message": f"Your {request_type} request has been received and is being processed.",
                "standard": "GDPR" if gdpr_enabled else "CCPA"
            }

            # Log as an audit event
            self.log_audit_event(
                user_id=user_id,
                action=f"data_subject_request:{request_type}",
                resource="personal_data",
                status="received",
                tenant_id=tenant_id,
                details={"request_id": request_id, "additional_data": additional_data if additional_data else {}}
            )

            logger.info(f"Handled data subject request {request_type} for user {user_id} (Request ID: {request_id})")
            return handling_result
        except Exception as e:
            logger.error(f"Error handling data subject request for {user_id}: {e}")
            return {"status": "error", "message": str(e)}

    def get_security_status(self) -> Dict[str, Any]:
        """
        Get current status of enterprise security systems
        """
        try:
            active_encryption_key = self.config['encryption'].get('active_key_id', 'none')
            total_encryption_keys = len(self.config['encryption']['keys'])

            compliance_status = {}
            for standard, config in self.config['compliance']['standards'].items():
                compliance_status[standard.upper()] = {
                    "enabled": config.get('enabled', False)
                }

            return {
                "status": "success",
                "encryption": {
                    "enabled": True,
                    "algorithm": self.config['encryption'].get('algorithm', 'N/A'),
                    "active_key_id": active_encryption_key,
                    "total_keys": total_encryption_keys,
                    "key_rotation_days": self.config['encryption'].get('key_rotation_days', 'N/A')
                },
                "access_control": {
                    "rbac_enabled": self.config['access_control']['rbac_enabled'],
                    "abac_enabled": self.config['access_control']['abac_enabled'],
                    "default_policy": self.config['access_control']['default_policy'],
                    "roles_defined": list(self.config['access_control']['roles'].keys())
                },
                "audit_logging": {
                    "enabled": self.config['audit_logging']['enabled'],
                    "log_directory": self.config['audit_logging'].get('log_directory', 'N/A'),
                    "retention_days": self.config['audit_logging'].get('retention_days', 'N/A')
                },
                "compliance": compliance_status,
                "data_loss_prevention": {
                    "enabled": self.config['data_loss_prevention']['enabled'],
                    "rules": list(self.config['data_loss_prevention']['rules'].keys())
                },
                "threat_detection": {
                    "enabled": self.config['threat_detection']['enabled'],
                    "brute_force_protection": self.config['threat_detection']['brute_force_protection']['max_attempts'] > 0,
                    "anomaly_detection": self.config['threat_detection']['anomaly_detection']['enabled'],
                    "ddos_protection": self.config['threat_detection']['ddos_protection']['enabled']
                },
                "session_management": {
                    "timeout_minutes": self.config['session_management']['session_timeout_minutes'],
                    "max_concurrent_sessions": self.config['session_management']['max_concurrent_sessions'],
                    "secure_cookies": self.config['session_management']['secure_cookies']
                }
            }
        except Exception as e:
            logger.error(f"Error getting security status: {e}")
            return {"status": "error", "message": str(e)}

# Global enterprise security instance
enterprise_security = EnterpriseSecurity()
