import os
import re

from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, field_validator, computed_field
from .utility.config_loader import ConfigReaderInstance
from .config import settings

MAX_DIALOGUE_TURNS = 20
FASTAPI_SERVER_PORT = 8000
FASTAPI_SERVER_API_PATH = "http://127.0.0.1:" + str(FASTAPI_SERVER_PORT) + "/api/v1"
DEFAULT_LLM_CHAT_MODEL_ID = "meta-llama/llama-3.1-70b-instruct"
DEFAULT_LLM_WEB_SEARCH_MODEL_ID = "perplexity/llama-3.1-sonar-large-128k-online"
DEFAULT_DUMMY_ASSISTANT_RESPONSE = "Meow meow meow meow meow meow meow meow. Meow meow meow? Meow meow meow meow meow~"
DUMMY_SESSION_ID = "dummy_session_id"

_UsageMode = Literal["simple", "advanced"]
_ParamType = Literal["float", "int", "dict"]


class ParameterInfo(BaseModel):
    id: str = Field(..., alias="id")
    type: _ParamType = Field(..., alias="type")
    name: str = Field(..., alias="name")
    description: Optional[str] = Field(..., alias="description")
    min: Optional[Any] = Field(0, alias="min")
    max: Optional[Any] = Field(0, alias="max")
    default: Optional[Any] = Field(0, alias="default")
    openrouter_only: Optional[bool] = Field(False, alias="openrouter_only")


class ModelCost(BaseModel):
    prompt: float = Field(0, description="cost per 1M tokens, in USD", alias="prompt")
    completion: float = Field(0, description="cost per 1M tokens, in USD", alias="completion")
    request: float = Field(0, description="cost per 1K requests, in USD", alias="request")
    image: float = Field(0, description="cost per 1K images, in USD", alias="image")


class ModelInfo(BaseModel):
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
    pricing: ModelCost = Field(..., alias="pricing")
    base_url: str = Field(..., alias="base_url")
    api_key: str = Field(..., alias="api_key")
    usage_mode: str = Field("prompt", alias="usage_mode")

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
    parameters: list[ParameterInfo] = Field(..., alias="parameters")
    llm_models: Models = Field(..., alias="llm_models")

    @computed_field
    @property
    def streamlit_advanced_components(self) -> dict:
        if not hasattr(self, '_streamlit_advanced_components'):
            self._streamlit_advanced_components = None

        if self._streamlit_advanced_components is None:
            self._streamlit_advanced_components = {}
            for info in self.parameters:
                param = info.id
                if info.type not in ["float", "int"]:
                    continue

                param_elem_args = {
                    "help": info.description,
                    "min_value": (int(info.min) if info.type == "int" else float(info.min)) if info.min is not None else None,
                    "max_value": (int(info.max) if info.type == "int" else float(info.max)) if info.max is not None else None,
                    "value": (float(info.default) if info.type == "float" else int(info.default)) if info.default is not None else None,
                    "key": f"llm_param___{param}" if not info.openrouter_only else f"llm_param___extra_body___{param}",
                }
                if info.type == "int":
                    param_elem_args["step"] = 1
                elif info.type == "float":
                    param_elem_args["step"] = 0.1
                    param_elem_args["format"] = "%.1f"

                self._streamlit_advanced_components[param] = {
                    "streamlit_component": "number_input" if info.max is None else "slider",  # Apply label parameter
                    "args": [info.name],
                    "kwargs": param_elem_args,
                }

        return self._streamlit_advanced_components


_llm_config_yaml = ConfigReaderInstance.yaml.read_config_from_file(settings.LLM_CONFIG_FILENAME, return_dict=True)
llm_config = LLMConfig(**_llm_config_yaml)


class ModelByCategory:
    class SimpleMode:
        chat_models: dict[str, ModelInfo] = {model.id: model for model in llm_config.llm_models.chat_models if model.usage_mode == "simple"}
        search_models: dict[str, ModelInfo] = {model.id: model for model in llm_config.llm_models.search_models if model.usage_mode == "simple"}
        all_models: dict[str, ModelInfo] = {**chat_models, **search_models}

    chat_models: dict[str, ModelInfo] = {model.id: model for model in llm_config.llm_models.chat_models}
    search_models: dict[str, ModelInfo] = {model.id: model for model in llm_config.llm_models.search_models}
    all_models: dict[str, ModelInfo] = {**chat_models, **search_models}
