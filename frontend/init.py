import requests
import streamlit as st

from json import JSONDecodeError

from .constants import *

def init_streamlit_page_config():
    st.set_page_config(
        page_title="ChatGPT-like app",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded"
    )


def initialize_app_states():
    # initialize "messages" session_state to save dialogue history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # initialize "session_id" session_state
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    # initialize "openai_model" session_state
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = OPENAI_MODELS[DEFAULT_OPENAI_MODEL_INDEX]


def get_user_session():
    try:
        request_path = FASTAPI_SERVER_API_PATH + "/user_session"
        response = requests.get(request_path)
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


def app_initialization():
    init_streamlit_page_config()
    initialize_app_states()
    get_user_session()
    ensure_short_dialogue_history()
