"""
Configuration settings for Audio to MIDI Backend
Created by Sergie Code
"""

import os
from pathlib import Path

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File upload settings
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_FILE_SIZE_MB', 50)) * 1024 * 1024  # 50MB default
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER') or 'output'
    
    # Supported file extensions
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'aac', 'ogg'}
    
    # Audio processing settings
    SAMPLE_RATE = int(os.environ.get('SAMPLE_RATE', 16000))
    
    # Model settings (for future ML integration)
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'models'
    USE_GPU = os.environ.get('USE_GPU', 'False').lower() == 'true'
    
    # API settings
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT') or '100 per hour'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'app.log'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        # Ensure directories exist
        Path(Config.UPLOAD_FOLDER).mkdir(exist_ok=True)
        Path(Config.OUTPUT_FOLDER).mkdir(exist_ok=True)
        Path(Config.MODEL_PATH).mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Use environment variables for sensitive settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # More restrictive settings for production
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25MB for production
    API_RATE_LIMIT = '50 per hour'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = 'test_uploads'
    OUTPUT_FOLDER = 'test_output'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
