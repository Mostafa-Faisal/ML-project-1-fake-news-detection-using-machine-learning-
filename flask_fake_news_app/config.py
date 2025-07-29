# Configuration file for Flask Fake News Detection App

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///fake_news_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # BERT Model Settings
    BERT_MODEL_NAME = 'distilbert-base-uncased'
    CLASSIFICATION_MODEL = 'martin-ha/toxic-comment-model'
    MAX_SEQUENCE_LENGTH = 512
    
    # Application Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    JSON_SORT_KEYS = False
    
    # Pagination Settings
    POSTS_PER_PAGE = 20
    API_RESULTS_PER_PAGE = 10
    
    # Cache Settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate Limiting (for future implementation)
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_DEFAULT = '100 per hour'
    
    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = 'fake_news_app.log'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/fake_news_db'
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Model configuration
SUSPICIOUS_PATTERNS = [
    'shocking', 'exclusive', 'secret', 'urgent', 'miracle', 'breaking',
    'doctors hate', 'one weird trick', 'you won\'t believe', 'leaked',
    'government cover', 'big pharma', 'they don\'t want you to know',
    'amazing discovery', 'scientists shocked', 'unbelievable', 'incredible',
    'must read', 'viral', 'exposed', 'revealed', 'hidden truth'
]

# Analysis weights
ANALYSIS_WEIGHTS = {
    'pattern_analysis': 0.4,
    'pipeline_classification': 0.4,
    'bert_features': 0.2
}

# Confidence thresholds
CONFIDENCE_THRESHOLDS = {
    'very_high': 0.8,
    'high': 0.6,
    'medium': 0.4,
    'low': 0.2
}

# UI Configuration
UI_CONFIG = {
    'app_name': 'Fake News Detection System',
    'app_description': 'AI-Powered News Analysis using BERT',
    'version': '1.0.0',
    'author': 'AI Research Team',
    'max_title_length': 200,
    'max_content_length': 10000,
    'min_title_length': 5,
    'min_content_length': 20
}
