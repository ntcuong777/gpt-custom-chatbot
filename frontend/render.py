import time
import streamlit as st

from .query import get_assistant_response, stream_assistant_response
from common.constants import *
from common.config import settings
from frontend.events import on_selection_change


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
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_response = ""
            message_placeholder = st.empty()
            if not settings.STREAM_RESPONSE:
                tmp_response = ""
                full_response = get_assistant_response(prompt)
                for i in range(len(full_response)):
                    tmp_response += full_response[i]
                    message_placeholder.markdown(tmp_response + "▌")
                    time.sleep(0.015)

                message_placeholder.markdown(full_response)
            else:
                for response in stream_assistant_response(prompt):
                    full_response += response
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


def render_frontend():
    st.title("ChatGPT-like clone")

    # value of the selected model is saved in st.session_state["llm_model"]
    model_ids = list(ModelByCategory.all_models.keys())
    default_idx = model_ids.index(DEFAULT_LLM_MODEL_ID)
    st.selectbox(
        "Model to use:", ModelByCategory.all_models.keys(), format_func=lambda model_id: ModelByCategory.all_models[model_id].name,
        index=default_idx, key="llm_model", help="Ordered by price of using the model", on_change=on_selection_change
    )

    # Chat box
    render_chatbox()
