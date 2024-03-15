# by Richi Rod AKA @richionline / falken20
# ./falken_plants/config.py

# Library that uses type annotation to validate data and manage settings.
# from pydantic import BaseSettings # Old version
import os
from pydantic.v1 import BaseSettings
# from pydantic_settings import BaseSettings # New version

# Library to cache the data
from functools import lru_cache

from .logger import Log

__title__ = 'Falken Plants'
__version__ = '1.0.0'
__author__ = 'Falken'
__url_github__ = 'https://github.com/falken20/'
__url_twitter__ = 'https://twitter.com/richionline'
__url_linkedin__ = 'https://www.linkedin.com/in/richionline/'
__license__ = 'MIT License'
__copyright__ = '© 2023 by Richi Rod AKA @richionline / falken20'
__features__ = [
]

#######################################################################
# Config format for Flask apps, you create a class for each environment
#######################################################################


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.SQLALCHEMY_DATABASE_URI


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEVELOPMENT_DATABASE_URL")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("STAGING_DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PRODUCTION_DATABASE_URL")
    PRUEBA_ROD = True


class Settings(BaseSettings):
    # pydantic will automatically assume those default values if it doesn’t
    # find the corresponding environment variables.
    env_name: str = "Local"
    base_url: str = "http://localhost:5000"
    # db_url: str = "sqlite:///./shortener.db"
    ENV_PRO: str = "N"
    LEVEL_LOG: list = []
    DATABASE_URL: str = ""
    DB_SQLITE_URL: str = ""
    APP_DATA = {
        'title': __title__,
        'version': __version__,
        'author': __author__,
        'url_github': __url_github__,
        'url_twitter': __url_twitter__,
        'url_linkedin': __url_linkedin__,
        'license': __license__,
        'copyrigth': __copyright__,
        'features': __features__,
    }

    CONFIG_ENV = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "staging": StagingConfig,
        "production": ProductionConfig
    }

    class Config:
        # When you add the Config class with the path to your env_file to your
        # settings, pydantic loads your environment variables from the .env file.
        env_file = ".env"
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    Log.info(f"Loading settings for: {settings.env_name}")
    print_settings(settings)
    return settings


def print_settings(settings: Settings) -> None:
    Log.info(f"Settings: \
            \n env_name: {settings.env_name}\
            \n ENV_PRO: {settings.ENV_PRO}\
            \n LEVEL_LOG: {settings.LEVEL_LOG}")

    for f, v in settings.CONFIG_ENV.items():
        Log.info(f"Environment settings: {f} - {vars(v)}")

@lru_cache
def print_app_config(app):
    """ Print the app config """
    for key, value in app.config.items():
        if isinstance(value, dict):
            for k, v in value.items():
                Log.debug(f"app.config: {key}: {k} - {v}")
        else:
            Log.debug(f"app.config: {key}: {value}")
