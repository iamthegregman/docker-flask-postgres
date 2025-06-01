import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# debug output
print("=== CONFIG DEBUG ===")
print(f"Raw env POSTGRES_PASSWORD: '{os.getenv('POSTGRES_PASSWORD')}'")
print(f"Raw env POSTGRES_USER: '{os.getenv('POSTGRES_USER')}'")
print("=== END CONFIG DEBUG ===")

class Config:
    """Base configuration class"""
    
    # Database Configuration
    DBUSER = os.getenv('POSTGRES_USER', 'marco')
    DBPASS = os.getenv('POSTGRES_PASSWORD', 'test12345')
    DBHOST = os.getenv('POSTGRES_HOST', 'db')
    DBPORT = os.getenv('POSTGRES_PORT', '5432')
    DBNAME = os.getenv('POSTGRES_DB', 'testdb')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-fallback-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add debug output for the class
    print(f"Config DBPASS: '{DBPASS}'")
    print(f"Config DBUSER: '{DBUSER}'")

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