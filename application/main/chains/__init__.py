import os

from huggingface_hub import model_info
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from openai import (
    APITimeoutError,
    APIConnectionError,
    APIResponseValidationError,
    RateLimitError,
    InternalServerError,
)

from common.constants import ModelByCategory

_default_openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "dummy_key")
_default_openrouter_api_url = os.getenv("OPENROUTER_API_URL", "http://127.0.0.1/api/v1")
MAX_CONCURRENCY = 5
_LLM_COMPLETIONS = {
    model: ChatOpenAI(
            api_key=_default_openrouter_api_key if model_info.api_key is None else model_info.api_key,
            model=model,
            temperature=0,
            max_retries=5,
            max_tokens=1000,
            request_timeout=1800,  # 30 minutes
            base_url=_default_openrouter_api_url if model_info.base_url is None else model_info.base_url,
            # default_headers={
            #     "X-Title": "Handsome Cuong (Tam's Husband)'s Chatbot",
            # }
        ).with_retry(
            retry_if_exception_type=(
                APITimeoutError,
                APIConnectionError,
                APIResponseValidationError,
                RateLimitError,
                InternalServerError,
            ),
            wait_exponential_jitter=True,
            stop_after_attempt=5,
        ).with_config(RunnableConfig(max_concurrency=MAX_CONCURRENCY, run_name=f"{model}__llm_call"))
    for model, model_info in ModelByCategory.all_models.items()
}


def _message_list_dicts_to_langchain_msgs(messages: list[dict]):
    result = []
    for msg in messages:
        if msg["role"] == "user":
            result.append(HumanMessage(msg["content"]))
        elif msg["role"] == "assistant":
            result.append(AIMessage(msg["content"]))
        elif msg["role"] == "system":
            result.append(SystemMessage(msg["content"]))

    return result


_msg_list_to_valid_langchain_msg = RunnableLambda(_message_list_dicts_to_langchain_msgs).with_config({"run_name": "to_langchain_msgs"})
_LLM_CHAINS = {
    model: _msg_list_to_valid_langchain_msg | _LLM_COMPLETIONS[model] | StrOutputParser()
    for model in ModelByCategory.all_models.keys()
}


def get_langchain_chain(model: str = "gpt-4o-mini"):
    assert model in ModelByCategory.all_models, f"Model {model} not found in available models: {ModelByCategory.all_models.keys()}"
    return _LLM_CHAINS[model]
