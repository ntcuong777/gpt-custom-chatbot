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

MAX_CONCURRENCY = 5
_MODEL_LIST = [
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
    "gpt-4", "gpt-4o", "gpt-4o-mini"
]
_LLM_COMPLETIONS = {
    model: ChatOpenAI(
            model=model,
            temperature=0,
            max_retries=5,
            max_tokens=1000,
            request_timeout=1800,  # 30 minutes
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
    for model in _MODEL_LIST
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
    for model in _MODEL_LIST
}


def get_langchain_chain(model: str = "gpt-4o-mini"):
    return _LLM_CHAINS[model]
