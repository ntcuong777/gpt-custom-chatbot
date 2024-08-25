import json
import time

import requests
import streamlit as st
import traceback

from typing import Generator
from json import JSONDecodeError

from common.constants import *
from common.logging import LoggerInstance

logger = LoggerInstance().get_logger(__name__)


def _save_user_dialogue(user_msg: str):
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/chat/"
        request_body = {"session_id": st.session_state.session_id, "content": user_msg}
        requests.post(request_path, json=request_body)
    except ConnectionError:
        logger.error("Cannot connect to server!!!")
    except JSONDecodeError:
        logger.error("No valid response")
    except Exception as e:
        logger.error(f"Server error!!! Err = {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")


def _collect_model_kwargs() -> dict:
    model_kwargs = {}
    for state, val in st.session_state.items():
        if state.startswith("llm_param___"):
            param_name = state.replace("llm_param___", "")
            if param_name.startswith("extra_body___"):
                param_name = param_name.replace("extra_body___", "")
                if "extra_body" not in model_kwargs:
                    model_kwargs["extra_body"] = {}
                model_kwargs["extra_body"][param_name] = val
            else:
                model_kwargs[param_name] = val

    return model_kwargs


def get_assistant_response(user_msg: str, model_kwargs: dict = None) -> str:
    if st.session_state.session_id == DUMMY_SESSION_ID:
        return DEFAULT_DUMMY_ASSISTANT_RESPONSE

    if model_kwargs is None:
        model_kwargs = _collect_model_kwargs()

    try:
        request_path = FASTAPI_SERVER_API_PATH + "/chat/" + st.session_state.session_id
        response = requests.post(request_path, json={"model": st.session_state.llm_model, "user_query": user_msg, "llm_params": model_kwargs})
        json_response = response.json()
        return json_response["assistant_response"] \
            if "assistant_response" in json_response \
            else DEFAULT_DUMMY_ASSISTANT_RESPONSE
    except ConnectionError:
        logger.error("Cannot connect to server!!!")
    except JSONDecodeError:
        logger.error("No valid assistant response")
    except Exception as e:
        logger.error(f"Server error!!! Err = {str(e)}")
        logger.error(f"Stack trace: {traceback.format_exc()}")

    return DEFAULT_DUMMY_ASSISTANT_RESPONSE


def stream_assistant_response(user_msg: str, model_kwargs: dict = None) -> Generator[str, str, str]:
    if st.session_state.session_id == DUMMY_SESSION_ID:
        words = DEFAULT_DUMMY_ASSISTANT_RESPONSE.split()
        for word in words:
            yield word + " "
            time.sleep(0.05)
    else:
        if model_kwargs is None:
            model_kwargs = _collect_model_kwargs()

        try:
            request_path = FASTAPI_SERVER_API_PATH + "/chat/" + st.session_state.session_id + "/stream"
            response = requests.post(request_path, json={"model": st.session_state.llm_model, "user_query": user_msg, "llm_params": model_kwargs}, stream=True)
            for content in response.iter_content(chunk_size=None):
                yield json.loads(content)["assistant_response"]
        except ConnectionError:
            logger.error("Cannot connect to server!!!")
            yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
        except JSONDecodeError:
            logger.error("No valid assistant response")
            yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
        except Exception as e:
            logger.error(f"Server error!!! Err = {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
