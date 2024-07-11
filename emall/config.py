import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = 'localhost'
    SECRET_KEY = 'dev'

class DevelopmentDockerConfig(Config):
    DEBUG = True
    DB_HOST = 'db'
    SECRET_KEY = 'dev'

class TestingConfig(Config):
    TESTING = True
    DB_HOST = 'db'
    SECRET_KEY = 'test'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    DB_HOST = 'db'
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-very-secure-secret-key')
    # SESSION_COOKIE_SECURE = True
    # REMEMBER_COOKIE_SECURE = True
    # REMEMBER_COOKIE_HTTPONLY = True

config = {
    'development': DevelopmentConfig,
    'development_docker': DevelopmentDockerConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}