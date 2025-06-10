"""
Database initialization and migration script for VentAI Enterprise
Sets up the database schema for workflow automation and mobile features
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from ventai.backend.database.models import Base, create_tables, get_table_names

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ventai_enterprise.db")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_engine():
    """Create and return database engine"""
    engine = create_engine(DATABASE_URL, echo=True)
    return engine

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()

def initialize_database():
    """Initialize the database with all required tables"""
    try:
        engine = create_database_engine()
        logger.info("Creating database tables...")
        create_tables(engine)
        logger.info("Database tables created successfully!")
        
        # Verify tables were created
        with engine.connect() as conn:
            if "sqlite" in DATABASE_URL:
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
                tables = [row[0] for row in result]
            else:
                # For PostgreSQL or other databases
                result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public';"))
                tables = [row[0] for row in result]
            
            expected_tables = get_table_names()
            missing_tables = set(expected_tables) - set(tables)
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
            else:
                logger.info("All required tables present!")
            
            logger.info(f"Created tables: {tables}")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def add_sample_data():
    """Add sample data for testing"""
    try:
        from ventai.backend.database.models import WorkflowTemplate, WebhookEndpoint
        
        with get_db_session() as session:
            # Check if sample data already exists
            existing_templates = session.query(WorkflowTemplate).count()
            if existing_templates > 0:
                logger.info("Sample data already exists, skipping...")
                return
            
            # Add sample workflow templates
            templates = [
                WorkflowTemplate(
                    id="project_creation",
                    name="HVAC Project Creation",
                    description="Automated workflow for creating new HVAC projects",
                    category="project_management",
                    task_definitions={
                        "tasks": [
                            {
                                "id": "validate_requirements",
                                "name": "Validate Project Requirements",
                                "handler": "validation_handler",
                                "estimated_duration": 15,
                                "priority": 1
                            },
                            {
                                "id": "create_project_structure",
                                "name": "Create Project Structure",
                                "handler": "project_creation_handler",
                                "estimated_duration": 30,
                                "priority": 2,
                                "dependencies": ["validate_requirements"]
                            }
                        ]
                    },
                    estimated_duration=45
                ),
                WorkflowTemplate(
                    id="compliance_check",
                    name="Regulatory Compliance Check",
                    description="Automated compliance verification for HVAC installations",
                    category="compliance",
                    task_definitions={
                        "tasks": [
                            {
                                "id": "check_permits",
                                "name": "Verify Required Permits",
                                "handler": "permit_check_handler",
                                "estimated_duration": 20,
                                "priority": 1
                            },
                            {
                                "id": "validate_codes",
                                "name": "Validate Building Codes",
                                "handler": "code_validation_handler",
                                "estimated_duration": 25,
                                "priority": 1
                            }
                        ]
                    },
                    estimated_duration=45
                ),
                WorkflowTemplate(
                    id="cost_optimization",
                    name="Cost Optimization Analysis",
                    description="AI-powered cost optimization for HVAC projects",
                    category="optimization",
                    task_definitions={
                        "tasks": [
                            {
                                "id": "analyze_materials",
                                "name": "Analyze Material Costs",
                                "handler": "material_analysis_handler",
                                "estimated_duration": 30,
                                "priority": 2
                            },
                            {
                                "id": "optimize_design",
                                "name": "Optimize System Design",
                                "handler": "design_optimization_handler",
                                "estimated_duration": 45,
                                "priority": 1,
                                "dependencies": ["analyze_materials"]
                            }
                        ]
                    },
                    estimated_duration=75
                )
            ]
            
            for template in templates:
                session.add(template)
            
            # Add sample webhook endpoints
            webhooks = [
                WebhookEndpoint(
                    name="Project Updates",
                    url="https://api.example.com/ventai/project-updates",
                    event_types=["project.created", "project.updated", "project.completed"],
                    headers={"Content-Type": "application/json"},
                    secret_key="webhook_secret_123"
                ),
                WebhookEndpoint(
                    name="Cost Alerts",
                    url="https://api.example.com/ventai/cost-alerts", 
                    event_types=["cost.exceeded", "cost.optimized"],
                    headers={"Content-Type": "application/json", "X-Source": "VentAI"},
                    secret_key="cost_webhook_456"
                )
            ]
            
            for webhook in webhooks:
                session.add(webhook)
            
            session.commit()
            logger.info("Sample data added successfully!")
            
    except Exception as e:
        logger.error(f"Failed to add sample data: {e}")
        raise

def check_database_health():
    """Check database health and connectivity"""
    try:
        engine = create_database_engine()
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute(text("SELECT 1"))
            logger.info("Database connectivity: OK")
            
            # Check table counts
            table_stats = {}
            for table_name in get_table_names():
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = count_result.scalar()
                    table_stats[table_name] = count
                except Exception as e:
                    table_stats[table_name] = f"Error: {e}"
            
            logger.info("Table statistics:")
            for table, count in table_stats.items():
                logger.info(f"  {table}: {count} records")
            
            return True
            
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

def migrate_database():
    """Run database migrations"""
    logger.info("Running database migrations...")
    
    try:
        # For now, just recreate tables
        # In production, you'd use Alembic for proper migrations
        initialize_database()
        logger.info("Database migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        raise

if __name__ == "__main__":
    """Command line interface for database operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description="VentAI Database Management")
    parser.add_argument(
        "command",
        choices=["init", "migrate", "health", "sample-data"],
        help="Database operation to perform"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force operation even if database exists"
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        logger.info("Initializing VentAI Enterprise database...")
        initialize_database()
        
    elif args.command == "migrate":
        logger.info("Running database migrations...")
        migrate_database()
        
    elif args.command == "health":
        logger.info("Checking database health...")
        if check_database_health():
            logger.info("Database is healthy!")
            sys.exit(0)
        else:
            logger.error("Database health check failed!")
            sys.exit(1)
            
    elif args.command == "sample-data":
        logger.info("Adding sample data...")
        add_sample_data()
    
    logger.info("Database operation completed!")
