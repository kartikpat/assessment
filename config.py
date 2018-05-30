# config.py

class Config(object):
    """
    Common configurations
    """
    FLASK_API_VERSION = '/v1'
    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    FLASK_CONFIG = 'development_config.py'
    FLASK_LOGGING = True
    
class ProductionConfig(Config):
    """
    Production configurations   
    """
    FLASK_CONFIG = 'production_config.py'
    FLASK_LOGGING = False

class TestingConfig(Config):
    """
    Testing configurations
    """
    FLASK_CONFIG = 'test_config.py'
    FLASK_LOGGING = True

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
