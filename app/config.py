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