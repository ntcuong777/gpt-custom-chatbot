import time
import streamlit as st

from .query import get_assistant_response
from .constants import *


def render_chatbox():
    # Render previous history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # formatted_message(message["content"], is_user=(message["role"] == "user"))
            st.markdown(message["content"])

    # Render input box and request assistant answer upon user input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            # st_markdown(prompt)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = get_assistant_response(prompt)
            message_placeholder = st.empty()
            tmp_response = ""
            for i in range(len(full_response)):
                tmp_response += full_response[i]
                message_placeholder.markdown(tmp_response + "▌")
                time.sleep(0.015)

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


def render_frontend():
    st.title("ChatGPT-like clone")

    # value of the selected model is saved in st.session_state["openai_model"]
    st.selectbox("Model to use:", OPENAI_MODELS, index=0,
        key="openai_model", help="Ordered by price of using the model")

    # Chat box
    render_chatbox()
