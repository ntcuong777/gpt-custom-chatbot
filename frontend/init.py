import streamlit as st

from common.constants import MAX_DIALOGUE_TURNS
from .common import get_user_session


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

    # # initialize "llm_model" session_state
    # if "llm_model" not in st.session_state:
    #     st.session_state.llm_model = ModelByCategory.all_models[DEFAULT_LLM_MODEL_ID]


def ensure_short_dialogue_history():
    if "messages" in st.session_state and len(st.session_state.messages) > MAX_DIALOGUE_TURNS:
        # remove previous history to save resource
        st.session_state.messages = st.session_state.messages[-MAX_DIALOGUE_TURNS:]


def app_initialization():
    init_streamlit_page_config()
    initialize_app_states()
    get_user_session()
    ensure_short_dialogue_history()
