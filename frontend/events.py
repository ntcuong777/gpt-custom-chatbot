import streamlit as st

from .common import get_user_session


def on_selection_change():
    # Reset the messages
    st.session_state.messages = []
    st.session_state.session_id = None
    get_user_session()
