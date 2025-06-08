#!/bin/bash

# Database Migration Script
# This script handles database migrations for VentAI

set -e

# Load environment variables
if [ -f "environments/.env.development" ]; then
    source environments/.env.development
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
ENVIRONMENT=${ENVIRONMENT:-development}
BACKUP_DIR="backups/database"
MIGRATION_DIR="backend/migrations"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    # Check if PostgreSQL is accessible
    if [ "$DATABASE_URL" ]; then
        log_info "Database URL configured: $DATABASE_URL"
    else
        log_warning "DATABASE_URL not set, using default values"
    fi
    
    # Create necessary directories
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$MIGRATION_DIR"
    
    log_success "Prerequisites checked"
}

# Create database backup
create_backup() {
    local backup_name="ventai_backup_$(date +%Y%m%d_%H%M%S).sql"
    local backup_path="$BACKUP_DIR/$backup_name"
    
    log_info "Creating database backup..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        log_warning "Creating production backup - this may take some time"
    fi
    
    # Use pg_dump to create backup
    if docker exec -i ventai-postgres pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "$backup_path" 2>/dev/null; then
        log_success "Backup created: $backup_path"
        echo "$backup_path"
    else
        log_error "Failed to create backup"
        return 1
    fi
}

# Run Django migrations
run_django_migrations() {
    log_info "Running Django migrations..."
    
    cd backend/src/django_project
    
    # Check for pending migrations
    python manage.py showmigrations --plan
    
    # Run migrations
    if python manage.py migrate; then
        log_success "Django migrations completed"
    else
        log_error "Django migrations failed"
        return 1
    fi
    
    cd ../../..
}

# Run FastAPI database setup
run_fastapi_setup() {
    log_info "Running FastAPI database setup..."
    
    cd backend
    
    # Run Alembic migrations if available
    if [ -f "alembic.ini" ]; then
        log_info "Running Alembic migrations..."
        alembic upgrade head
    fi
    
    # Run custom database setup
    if [ -f "src/database_setup.py" ]; then
        log_info "Running database setup script..."
        python src/database_setup.py
    fi
    
    cd ..
    
    log_success "FastAPI database setup completed"
}

# Initialize database with sample data
init_sample_data() {
    log_info "Initializing sample data..."
    
    cd backend
    
    # Check if fixtures exist
    if [ -d "fixtures" ]; then
        log_info "Loading fixtures..."
        cd src/django_project
        python manage.py loaddata ../../fixtures/*.json
        cd ../../..
    fi
    
    # Run custom data initialization
    if [ -f "src/init_data.py" ]; then
        log_info "Running data initialization script..."
        python src/init_data.py
    fi
    
    cd ..
    
    log_success "Sample data initialized"
}

# Migrate from SQLite to PostgreSQL
migrate_sqlite_to_postgres() {
    log_info "Migrating from SQLite to PostgreSQL..."
    
    # Backup SQLite data
    log_info "Backing up SQLite data..."
    cd backend/src/django_project
    python manage.py dumpdata --natural-foreign --natural-primary > sqlite_data.json
    
    # Switch to PostgreSQL settings
    log_info "Switching to PostgreSQL configuration..."
    export DATABASE_URL="$POSTGRES_DATABASE_URL"
    
    # Run migrations on PostgreSQL
    python manage.py migrate
    
    # Load SQLite data into PostgreSQL
    log_info "Loading data into PostgreSQL..."
    python manage.py loaddata sqlite_data.json
    
    cd ../../..
    
    log_success "Migration from SQLite to PostgreSQL completed"
}

# Restore database from backup
restore_backup() {
    local backup_file="$1"
    
    if [ ! -f "$backup_file" ]; then
        log_error "Backup file not found: $backup_file"
        return 1
    fi
    
    log_warning "This will replace the current database with the backup"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Restore cancelled"
        return 0
    fi
    
    log_info "Restoring database from backup: $backup_file"
    
    # Drop and recreate database
    docker exec -i ventai-postgres psql -U "$POSTGRES_USER" -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
    docker exec -i ventai-postgres psql -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;"
    
    # Restore backup
    if docker exec -i ventai-postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$backup_file"; then
        log_success "Database restored successfully"
    else
        log_error "Failed to restore database"
        return 1
    fi
}

# Reset database
reset_database() {
    log_warning "This will completely reset the database"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Reset cancelled"
        return 0
    fi
    
    log_info "Resetting database..."
    
    # Stop services
    npm run docker:down
    
    # Remove database volumes
    docker volume rm mvp_postgres_data 2>/dev/null || true
    docker volume rm mvp_redis_data 2>/dev/null || true
    
    # Start services
    npm run docker:db
    
    # Wait for database
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Run migrations
    run_django_migrations
    run_fastapi_setup
    
    log_success "Database reset completed"
}

# Show help
show_help() {
    echo "Database Migration Script for VentAI"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  migrate                Run all database migrations"
    echo "  backup                 Create database backup"
    echo "  restore <file>         Restore database from backup"
    echo "  reset                  Reset database completely"
    echo "  sqlite-to-postgres     Migrate from SQLite to PostgreSQL"
    echo "  init-data              Initialize sample data"
    echo "  status                 Show database status"
    echo ""
    echo "Options:"
    echo "  --environment ENV      Set environment (development|production|test)"
    echo "  --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 migrate"
    echo "  $0 backup"
    echo "  $0 restore backups/database/ventai_backup_20240101_120000.sql"
    echo "  $0 reset"
}

# Show database status
show_status() {
    log_info "Database Status"
    echo "===================="
    echo "Environment: $ENVIRONMENT"
    echo "Database URL: $DATABASE_URL"
    echo ""
    
    # Check if database is running
    if docker exec ventai-postgres pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; then
        log_success "PostgreSQL is running"
        
        # Show database info
        echo "Database info:"
        docker exec ventai-postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\l"
    else
        log_error "PostgreSQL is not running"
    fi
    
    # Check Redis
    if docker exec ventai-redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis is running"
    else
        log_error "Redis is not running"
    fi
}

# Main function
main() {
    case "$1" in
        migrate)
            check_prerequisites
            create_backup
            run_django_migrations
            run_fastapi_setup
            ;;
        backup)
            check_prerequisites
            create_backup
            ;;
        restore)
            if [ -z "$2" ]; then
                log_error "Please specify backup file to restore"
                exit 1
            fi
            check_prerequisites
            restore_backup "$2"
            ;;
        reset)
            reset_database
            ;;
        sqlite-to-postgres)
            check_prerequisites
            migrate_sqlite_to_postgres
            ;;
        init-data)
            check_prerequisites
            init_sample_data
            ;;
        status)
            show_status
            ;;
        --help|help|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Run main function
main "$@"
