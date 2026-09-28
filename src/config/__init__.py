"""
Configuration Module

This module handles configuration management for the application.
It loads environment variables from a .env file and provides
a central Config class that other modules can import and use.

Configuration parameters include:
- Environment (dev/qa/prod)
- Debug mode
- Data directory location
- Host and port settings for the server

Usage:
    from src.config import Config
    
    # Access configuration values
    debug_mode = Config.DEBUG
    data_dir = Config.DATA_DIR
"""

import os
from dotenv import load_dotenv

# First determine which environment to use (from system env or default to 'dev')
env_name = os.environ.get('ENV_NAME', 'dev')

# Load base .env file first (common settings)
load_dotenv()

# Then load environment-specific file if it exists
# This allows for overriding base settings with environment-specific ones
# eg: .env.dev, .env.qa, .env.prod
env_file = f".env.{env_name}" if env_name != 'dev' else '.env'
load_dotenv(env_file, override=True)

class Config:
    """
    Central configuration class for the application.
    
    This class provides access to all configuration parameters,
    with sensible defaults that can be overridden through environment variables.
    
    Attributes:
        ENV (str): The environment (dev/qa/prod), defaults to 'dev'
        APP_NAME (str): The name of the application
        DEBUG (bool): Debug mode flag, True in development environment
        DATA_DIR (str): Directory where JSON files will be stored
        HOST (str): Host address to bind the server to
        PORT (int): Port number to listen on
    """
    # Application environment (dev/qa/uat/prod)
    ENV = os.getenv('ENV', 'dev')
    
    # Application name
    APP_NAME = 'gupshup-webhook-api'
    
    # Debug mode (enabled in development)
    DEBUG = ENV == 'dev'
    
    # Directory for storing JSON data files
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    
    # Server host and port
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))

# Make sure data directory exists
# This ensures the application can write files without errors
os.makedirs(Config.DATA_DIR, exist_ok=True)

