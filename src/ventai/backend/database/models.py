"""
Database models for VentAI Enterprise Features
Includes workflow automation, mobile sync, and project management
"""
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class WorkflowTemplate(Base):
    """Template for workflow automation"""
    __tablename__ = "workflow_templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)
    task_definitions = Column(JSON)  # Store task structure as JSON
    estimated_duration = Column(Integer)  # Duration in minutes
    version = Column(String(50), default="1.0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    workflows = relationship("WorkflowInstance", back_populates="template")

class WorkflowInstance(Base):
    """Individual workflow execution instance"""
    __tablename__ = "workflow_instances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String, ForeignKey("workflow_templates.id"), nullable=False)
    name = Column(String(255), nullable=False)
    status = Column(String(50), default="CREATED")  # CREATED, RUNNING, COMPLETED, FAILED, CANCELLED
    progress = Column(Float, default=0.0)
    context = Column(JSON)  # Workflow execution context
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Project association
    project_id = Column(String)
    client_id = Column(String)
    
    # Relationships
    template = relationship("WorkflowTemplate", back_populates="workflows")
    tasks = relationship("WorkflowTask", back_populates="workflow")

class WorkflowTask(Base):
    """Individual tasks within a workflow"""
    __tablename__ = "workflow_tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflow_instances.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    handler_name = Column(String(100), nullable=False)
    status = Column(String(50), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED, SKIPPED
    priority = Column(Integer, default=3)  # 1=HIGH, 2=MEDIUM, 3=LOW
    
    # Dependencies
    dependencies = Column(JSON)  # List of task IDs this task depends on
    
    # Timing
    estimated_duration = Column(Integer)  # Duration in minutes
    actual_duration = Column(Integer)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Results
    result = Column(JSON)
    error_message = Column(Text)
    
    # Relationships
    workflow = relationship("WorkflowInstance", back_populates="tasks")

class MobileDevice(Base):
    """Registered mobile devices for field work"""
    __tablename__ = "mobile_devices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(255), unique=True, nullable=False)
    device_name = Column(String(255))
    platform = Column(String(50))  # ios, android
    app_version = Column(String(50))
    
    # User association
    user_id = Column(String, nullable=False)
    user_name = Column(String(255))
    user_role = Column(String(100))
    
    # Device status
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sync_records = relationship("MobileSyncRecord", back_populates="device")

class MobileSyncRecord(Base):
    """Track mobile data synchronization"""
    __tablename__ = "mobile_sync_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, ForeignKey("mobile_devices.id"), nullable=False)
    sync_type = Column(String(50), nullable=False)  # upload, download, conflict_resolution
    
    # Sync details
    table_name = Column(String(100))
    record_count = Column(Integer, default=0)
    sync_status = Column(String(50), default="PENDING")  # PENDING, SUCCESS, FAILED, PARTIAL
    
    # Data integrity
    data_hash = Column(String(255))
    conflict_count = Column(Integer, default=0)
    
    # Timing
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Relationships
    device = relationship("MobileDevice", back_populates="sync_records")

class FieldTaskUpdate(Base):
    """Field task updates from mobile devices"""
    __tablename__ = "field_task_updates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, nullable=False)
    device_id = Column(String, ForeignKey("mobile_devices.id"))
    
    # Update details
    status = Column(String(50))
    progress = Column(Float, default=0.0)
    notes = Column(Text)
    
    # Location data
    latitude = Column(Float)
    longitude = Column(Float)
    location_accuracy = Column(Float)
    
    # Media attachments
    photos = Column(JSON)  # List of photo URLs/paths
    attachments = Column(JSON)  # List of attachment URLs/paths
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime)
    
    # Data integrity
    is_synced = Column(Boolean, default=False)
    sync_version = Column(Integer, default=1)
    
    # Relationships
    device = relationship("MobileDevice")

class ProjectRisk(Base):
    """AI-identified project risks"""
    __tablename__ = "project_risks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, nullable=False)
    
    # Risk details
    risk_type = Column(String(100), nullable=False)  # schedule, budget, technical, resource
    severity = Column(String(50), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # AI analysis
    confidence_score = Column(Float)  # 0.0 to 1.0
    impact_score = Column(Float)  # 0.0 to 1.0
    likelihood = Column(Float)  # 0.0 to 1.0
    
    # Mitigation
    mitigation_strategy = Column(Text)
    assigned_to = Column(String(255))
    due_date = Column(DateTime)
    
    # Status tracking
    status = Column(String(50), default="IDENTIFIED")  # IDENTIFIED, ASSIGNED, IN_PROGRESS, MITIGATED, CLOSED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectInsight(Base):
    """AI-generated project insights"""
    __tablename__ = "project_insights"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, nullable=False)
    
    # Insight details
    insight_type = Column(String(100), nullable=False)  # performance, recommendation, prediction
    category = Column(String(100))  # schedule, budget, quality, resources
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # AI analysis
    confidence_score = Column(Float)  # 0.0 to 1.0
    priority = Column(String(50), default="MEDIUM")  # LOW, MEDIUM, HIGH
    
    # Recommendations
    recommendations = Column(JSON)  # List of recommended actions
    expected_impact = Column(Text)
    
    # Status
    status = Column(String(50), default="ACTIVE")  # ACTIVE, REVIEWED, IMPLEMENTED, DISMISSED
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)
    reviewed_by = Column(String(255))

class WebhookEndpoint(Base):
    """External webhook endpoints for integrations"""
    __tablename__ = "webhook_endpoints"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    
    # Configuration
    event_types = Column(JSON)  # List of events to send
    headers = Column(JSON)  # Custom headers
    secret_key = Column(String(255))  # For signature verification
    
    # Status
    is_active = Column(Boolean, default=True)
    retry_count = Column(Integer, default=3)
    timeout_seconds = Column(Integer, default=30)
    
    # Analytics
    total_calls = Column(Integer, default=0)
    successful_calls = Column(Integer, default=0)
    failed_calls = Column(Integer, default=0)
    last_called = Column(DateTime)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(255))

class WebhookLog(Base):
    """Log of webhook deliveries"""
    __tablename__ = "webhook_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    endpoint_id = Column(String, ForeignKey("webhook_endpoints.id"), nullable=False)
    
    # Request details
    event_type = Column(String(100), nullable=False)
    payload = Column(JSON)
    headers = Column(JSON)
    
    # Response details
    status_code = Column(Integer)
    response_body = Column(Text)
    response_time_ms = Column(Integer)
    
    # Retry information
    attempt_number = Column(Integer, default=1)
    max_attempts = Column(Integer, default=3)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime)
    
    # Status
    delivery_status = Column(String(50), default="PENDING")  # PENDING, SUCCESS, FAILED, RETRY
    error_message = Column(Text)
    
    # Relationships
    endpoint = relationship("WebhookEndpoint")

# Database utility functions
def create_tables(engine):
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_table_names():
    """Get list of all table names"""
    return [
        "workflow_templates",
        "workflow_instances", 
        "workflow_tasks",
        "mobile_devices",
        "mobile_sync_records",
        "field_task_updates",
        "project_risks",
        "project_insights",
        "webhook_endpoints",
        "webhook_logs"
    ]
