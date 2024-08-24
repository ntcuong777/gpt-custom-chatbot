import requests
import streamlit as st

from json import JSONDecodeError

from common.constants import FASTAPI_SERVER_API_PATH, MAX_DIALOGUE_TURNS


def get_user_session():
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/user_session/new"
        response = requests.post(request_path, json={"model": st.session_state.llm_model})
        json_response = response.json()
        st.session_state["session_id"] = json_response["session_id"] if "session_id" in json_response else None
    except ConnectionError:
        print("Cannot connect to server!!!")
    except JSONDecodeError:
        print("No valid session_id response")


def ensure_short_dialogue_history():
    if "messages" in st.session_state and len(st.session_state.messages) > MAX_DIALOGUE_TURNS:
        # remove previous history to save resource
        st.session_state.messages = st.session_state.messages[-MAX_DIALOGUE_TURNS:]
