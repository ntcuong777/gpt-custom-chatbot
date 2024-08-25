import requests
import traceback
import streamlit as st

from .ui_common import get_user_session
from .init_ui_state import initialize_app_states
from common.constants import *
from common.logging import LoggerInstance

logger = LoggerInstance().get_logger(__name__)


def on_selection_change():
    # Reset the messages
    st.session_state.messages = []
    st.session_state.session_id = None
    get_user_session()


def on_system_message_change():
    session_id = st.session_state.session_id
    system_msg = st.session_state.system_message if "system_message" in st.session_state else None
    if system_msg is not None:
        try:
            request_path = FASTAPI_SERVER_API_PATH + "/user_session/set-system-message"
            response = requests.post(request_path, json={"session_id": session_id, "system_message": system_msg})
            logger.debug(f"Update system message: {response.text}")
        except ConnectionError:
            logger.error("Cannot connect to server!!!")
        except Exception:
            exc_details = traceback.format_exc()
            logger.error(f"Error updating system message: {exc_details}")


def on_new_chat():
    # delete all messages and reset session_id
    st.session_state.messages = []
    st.session_state.session_id = None
    st.session_state.system_message = None
    initialize_app_states()
