import os
import re

from pydantic import BaseModel, Field, field_validator
from .utility.config_loader import ConfigReaderInstance
from .config import settings

MAX_DIALOGUE_TURNS = 20
FASTAPI_SERVER_PORT = 8000
FASTAPI_SERVER_API_PATH = "http://127.0.0.1:" + str(FASTAPI_SERVER_PORT) + "/api/v1"
DEFAULT_LLM_MODEL_ID = "nousresearch/hermes-3-llama-3.1-70b"
DEFAULT_DUMMY_ASSISTANT_RESPONSE = "Meow meow meow meow meow meow meow meow. Meow meow meow? Meow meow meow meow meow~"


class ModelCost(BaseModel):
    input: float = Field(0, description="cost per 1M tokens, in USD", alias="input")
    output: float = Field(0, description="cost per 1M tokens, in USD", alias="output")
    reqs: float = Field(0, description="cost per 1K requests, in USD", alias="reqs")
    imgs: float = Field(0, description="cost per 1K images, in USD", alias="imgs")


class ModelInfo(BaseModel):
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    cost: ModelCost = Field(..., alias="cost")
    base_url: str = Field(..., alias="base_url")
    api_key: str = Field(..., alias="api_key")

    @field_validator("base_url", "api_key", mode="before")
    @classmethod
    def transform_env_vars(cls, raw: str) -> str:
        env_re = re.compile(r"\$\{(?P<env_var>[A-Z_]+)\}")
        m = env_re.match(raw)
        if m:
            var = os.getenv(m.group("env_var"), "")
            return var
        return raw

    @field_validator("base_url", mode="after")
    @classmethod
    def transform_base_url(cls, raw: str) -> str:
        url_re = re.compile(r"https?://")
        if not url_re.match(raw):
            return f"https://{raw}"
        return raw


class Models(BaseModel):
    chat_models: list[ModelInfo] = Field(..., alias="chat_models")
    search_models: list[ModelInfo] = Field(..., alias="search_models")


class LLMConfig(BaseModel):
    llm_models: Models = Field(..., alias="llm_models")


_llm_config_yaml = ConfigReaderInstance.yaml.read_config_from_file(settings.LLM_CONFIG_FILENAME, return_dict=True)
LLM_CONFIG = LLMConfig(**_llm_config_yaml)


class ModelByCategory:
    chat_models: dict[str, ModelInfo] = {model.id: model for model in LLM_CONFIG.llm_models.chat_models}
    search_models: dict[str, ModelInfo] = {model.id: model for model in LLM_CONFIG.llm_models.search_models}
    all_models: dict[str, ModelInfo] = {**chat_models, **search_models}
