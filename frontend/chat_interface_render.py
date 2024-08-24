import time
import streamlit as st

from .ui_common import get_user_session, ensure_short_dialogue_history
from .api_queries import get_assistant_response, stream_assistant_response
from common.constants import (
    llm_config, ModelByCategory,
    DEFAULT_LLM_CHAT_MODEL_ID,
    DEFAULT_LLM_WEB_SEARCH_MODEL_ID
)
from common.config import settings
from frontend.ui_events import on_selection_change, on_system_message_change, on_new_chat


def render_chatbox():
    if st.session_state.advanced_mode:
        sys_msg_popover = st.popover("🤖Custom instructions", use_container_width=True)
        sys_msg_popover.text_area("Custom instructions", key="system_message", height=300, on_change=on_system_message_change)

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

    ensure_short_dialogue_history()


def render_chat_interface():
    st.title("ChatGPT-like clone")

    with st.sidebar:
        # options_col1, options_col2 = st.columns(2, vertical_alignment="top")
        #
        # opt1_col1, opt1_col2 = options_col1.columns(2, vertical_alignment="top")
        # opt1_col1.radio("Mode:", ["Chat", "Web Search"], key="chat_mode", index=0)
        # opt1_col2.toggle("Advanced mode", key="advanced_mode")
        st.radio("Mode:", ["Chat", "Web Search"], key="chat_mode", index=0)

        chat_mode = st.session_state["chat_mode"]
        # value of the selected model is saved in st.session_state["llm_model"]
        model_dict = ModelByCategory.SimpleMode.chat_models if chat_mode == "Chat" else ModelByCategory.SimpleMode.search_models
        if "advanced_mode" in st.session_state and st.session_state.advanced_mode:
            model_dict = ModelByCategory.chat_models if chat_mode == "Chat" else ModelByCategory.search_models
        model_ids = list(model_dict.keys())
        default_idx = model_ids.index(DEFAULT_LLM_CHAT_MODEL_ID) if chat_mode == "Chat" else model_ids.index(DEFAULT_LLM_WEB_SEARCH_MODEL_ID)
        # options_col2.selectbox(
        #     "Model to use:", model_ids, format_func=lambda model_id: model_dict[model_id].name,
        #     index=default_idx, key="llm_model", help="Ordered by price of using the model", on_change=on_selection_change
        # )
        st.selectbox(
            "Model to use:", model_ids, format_func=lambda model_id: model_dict[model_id].name,
            index=default_idx, key="llm_model", help="Ordered by price of using the model", on_change=on_selection_change
        )
        st.toggle("Advanced mode", key="advanced_mode")
        if st.session_state.advanced_mode:
            # params_popover = options_col2.popover("⚙️Advanced parameters")
            params_popover = st.popover("⚙️Advanced parameters")
            advanced_components = llm_config.streamlit_advanced_components
            for param, st_comp in advanced_components.items():
                comp_fn = getattr(params_popover, st_comp["streamlit_component"])
                comp_fn(*st_comp["args"], **st_comp["kwargs"])

        st.button("New chat", key="reset_chat", on_click=on_new_chat)

    # Chat box
    get_user_session()
    render_chatbox()
