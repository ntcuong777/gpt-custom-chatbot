# configs.py
from pathlib import Path
from typing import Optional

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    """Application configurations."""

    # all the directory level information defined at app config level
    # we do not want to pollute the env level config with these information
    # this can change on the basis of usage

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    SETTINGS_DIR: Path = BASE_DIR.joinpath('settings')
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

    LOGS_DIR: Path = BASE_DIR.joinpath('logs')
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # ChatGPT chat API config
    NUM_PREVIOUS_DIALOGUES: int = 10  # only use previous 5 dialogues to generate new responses


class GlobalConfig(BaseSettings):
    """Global configurations."""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )

    # These variables will be loaded from the .env file. However, if
    # there is a shell environment variable having the same name,
    # that will take precedence.

    APP_CONFIG: AppConfig = AppConfig()

    API_NAME: Optional[str] = Field(None, alias="API_NAME")
    API_DESCRIPTION: Optional[str] = Field(None, alias="API_DESCRIPTION")
    API_VERSION: Optional[str] = Field(None, alias="API_VERSION")
    API_DEBUG_MODE: Optional[bool] = Field(None, alias="API_DEBUG_MODE")
    OPENROUTER_API_URL: Optional[str] = Field("https://openrouter.ai/api/v1", alias="OPENROUTER_API_URL")
    STREAM_RESPONSE: Optional[bool] = Field(False, alias="STREAM_RESPONSE")

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, alias="ENV_STATE")

    # logging configuration file
    LOG_CONFIG_FILENAME: Optional[str] = Field(None, alias="LOG_CONFIG_FILENAME")
    LLM_CONFIG_FILENAME: Optional[str] = Field(None, alias="LLM_CONFIG_FILENAME")

    # environment specific variables do not need the Field class
    HOST: Optional[str] = Field('0.0.0.0', alias="HOST")
    PORT: Optional[int] = Field(8000, alias="PORT")
    LOG_LEVEL: Optional[str] = Field('info', alias="LOG_LEVEL")

    DB: Optional[str] = Field('sqlite', alias="DB")


class DevConfig(GlobalConfig):
    """Development configurations."""
    model_config = SettingsConfigDict(
        env_prefix='DEV_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


class ProdConfig(GlobalConfig):
    """Production configurations."""
    model_config = SettingsConfigDict(
        env_prefix='PROD_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


settings = FactoryConfig(GlobalConfig().ENV_STATE)()
# print(settings.__repr__())
