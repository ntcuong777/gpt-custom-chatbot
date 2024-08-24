import streamlit as st

from .ui_common import ensure_short_dialogue_history


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

    if "system_message" not in st.session_state:
        st.session_state.system_message = None

    # # initialize "llm_model" session_state
    # if "llm_model" not in st.session_state:
    #     st.session_state.llm_model = ModelByCategory.all_models[DEFAULT_LLM_MODEL_ID]


def app_initialization():
    init_streamlit_page_config()
    initialize_app_states()
    ensure_short_dialogue_history()
