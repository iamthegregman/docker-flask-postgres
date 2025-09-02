# Configuration Reference

## Overview
The Flask application uses a class-based configuration system with environment-specific settings. Configuration values are loaded from environment files (`.env`, `.env.prod`) and fall back to defaults for development.

## Configuration Structure

### Environment Variable Loading
The application attempts to load environment variables in this order:
1. `.env.prod` (production environment file)
2. `../.env` (parent directory environment file)
3. `.env` (default environment file)

### Configuration Classes

#### Base Config Class
All configurations inherit from the base `Config` class which provides:

**Database Configuration:**
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password  
- `POSTGRES_HOST` - Database host (default: localhost)
- `POSTGRES_PORT` - Database port (default: 5432)
- `POSTGRES_DB` - Database name

**Flask Configuration:**
- `SECRET_KEY` - Flask secret key for sessions/forms
- `SQLALCHEMY_TRACK_MODIFICATIONS` - Set to False for performance
- `DEBUG` - Debug mode setting (default: False)

#### Environment-Specific Configs

**DevelopmentConfig:**
- `DEBUG = True`
- `TESTING = False`
- Uses PostgreSQL database from environment variables

**ProductionConfig:**
- `DEBUG = False` 
- `TESTING = False`
- Uses PostgreSQL database from environment variables
- Production-specific optimizations

**TestingConfig:**
- `TESTING = True`
- `DEBUG = True`
- Uses in-memory SQLite database (`sqlite:///:memory:`)

## Current Configuration Code

```python
import os
from dotenv import load_dotenv

# Load environment variables - try multiple locations
if os.path.exists('.env.prod'):
    print("Loading .env.prod")
    load_dotenv('.env.prod')
elif os.path.exists('../.env'):
    print("Loading ../.env")
    load_dotenv('../.env')
else:
    print("Loading default .env")
    load_dotenv()

# Add debug output
print(f"POSTGRES_HOST from env: {os.getenv('POSTGRES_HOST')}")
print(f"POSTGRES_PORT from env: {os.getenv('POSTGRES_PORT')}")

class Config:
    """Base configuration class"""
    
    # Database Configuration
    DBUSER = os.getenv('POSTGRES_USER', 'defaultuser')
    DBPASS = os.getenv('POSTGRES_PASSWORD', 'defaultpassword')
    DBHOST = os.getenv('POSTGRES_HOST', 'localhost')
    DBPORT = os.getenv('POSTGRES_PORT', '5432')
    DBNAME = os.getenv('POSTGRES_DB', 'defaultdb')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Construct database URI
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}/{DBNAME}'
    )
    
    # Security Configuration
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Add production-specific settings here

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    # Use a separate test database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

## Environment Variables Required

### Required for All Environments
```bash
# Database Connection
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost                # or docker service name
POSTGRES_PORT=5432                     # 443 for production cloud deployment
POSTGRES_DB=lab_database

# Flask Application
SECRET_KEY=your_secure_random_key
DEBUG=false                           # true for development
```

### Development Environment (.env)
```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=lab_dev_user
POSTGRES_DB=lab_dev_database
DEBUG=true
```

### Production Environment (.env.prod)
```bash
POSTGRES_HOST=your-cloud-postgres-host
POSTGRES_PORT=443                     # Cloud SQL proxy port
POSTGRES_USER=lab_prod_user
POSTGRES_DB=lab_production_database
DEBUG=false
```

## Configuration Selection
The configuration is selected in `app.py` based on the `FLASK_ENV` environment variable:
```python
config_name = os.getenv('FLASK_ENV', 'development')
app_config = config.get(config_name, config['default'])
```

## Docker Configuration

### Development Container (Dockerfile)
- **Base Image**: python:3.9-alpine
- **Exposed Port**: 5000 (Flask development server)
- **Dependencies**: PostgreSQL dev libraries, gcc, musl-dev
- **Entry Point**: Direct Python execution (`python3 app.py`)

### Production Container (Dockerfile.prod)  
- **Base Image**: python:3.9-slim (Debian-based for cloud compatibility)
- **Exposed Port**: 8080 (Cloud Run standard)
- **Web Server**: Gunicorn with 2 workers, 120s timeout
- **Security**: Non-root user (appuser)
- **Dependencies**: PostgreSQL client, gcc, libpq-dev

### PostgreSQL Container (Dockerfile.postgres)
- **Base Image**: postgres:17.4-alpine  
- **Exposed Port**: 5432
- **Default Database**: reagentdb
- **Default User**: produser

## Kubernetes Deployment

### Port Configuration
- **External Access**: Port 80 (LoadBalancer) → 8080 (Flask container)
- **Internal Database**: postgres-service:5432
- **Flask Service**: flask-service (LoadBalancer type)
- **PostgreSQL Service**: postgres-service (ClusterIP type)

### Container Registry
- **Location**: europe-west2-docker.pkg.dev
- **Project**: weighty-diorama-461616-h5/reagent-flask-trial
- **Images**: flask-app:latest, postgres-db:latest

### Storage & Scaling
- **Flask Replicas**: 2 instances
- **PostgreSQL Storage**: 10Gi persistent volume
- **Configuration Management**: Kubernetes secrets (postgres-secret, flask-secret)