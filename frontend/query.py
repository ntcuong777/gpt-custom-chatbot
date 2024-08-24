import json
import requests
import streamlit as st
import traceback

from typing import Generator
from json import JSONDecodeError

from common.constants import *


def _save_user_dialogue(user_msg: str):
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/conversational/"
        request_body = {"session_id": st.session_state.session_id, "content": user_msg}
        requests.post(request_path, json=request_body)
    except ConnectionError:
        print("Cannot connect to server!!!")
    except JSONDecodeError:
        print("No valid response")
    except Exception as e:
        print(f"Server error!!! Err = {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")


def get_assistant_response(user_msg: str):
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/conversational/" + st.session_state.session_id
        response = requests.post(request_path, json={"model": st.session_state.llm_model, "user_query": user_msg})
        json_response = response.json()
        return json_response["assistant_response"] \
            if "assistant_response" in json_response \
            else DEFAULT_DUMMY_ASSISTANT_RESPONSE
    except ConnectionError:
        print("Cannot connect to server!!!")
    except JSONDecodeError:
        print("No valid assistant response")
    except Exception as e:
        print(f"Server error!!! Err = {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")

    return DEFAULT_DUMMY_ASSISTANT_RESPONSE


def stream_assistant_response(user_msg: str) -> Generator[str, str, str]:
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/conversational/" + st.session_state.session_id + "/stream"
        response = requests.post(request_path, json={"model": st.session_state.llm_model, "user_query": user_msg}, stream=True)
        for content in response.iter_content(chunk_size=None):
            yield json.loads(content)["assistant_response"]
    except ConnectionError:
        print("Cannot connect to server!!!")
        yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
    except JSONDecodeError:
        print("No valid assistant response")
        yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
    except Exception as e:
        print(f"Server error!!! Err = {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        yield DEFAULT_DUMMY_ASSISTANT_RESPONSE
