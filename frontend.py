import os
import time
import requests
import streamlit as st

from typing import Generator
from streamlit_markdown import st_markdown, st_streaming_markdown
from requests.exceptions import JSONDecodeError, ConnectionError
from dotenv import load_dotenv, find_dotenv

################ BEGIN : Global constants ################
MAX_DIALOGUE_TURNS = 20
FASTAPI_SERVER_PORT = 8000
FASTAPI_SERVER_API_PATH = "http://127.0.0.1:" + str(FASTAPI_SERVER_PORT) + "/api/v1"
OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4o", "gpt-4o-mini"]
DEFAULT_OPENAI_MODEL_INDEX = 0
DEFAULT_DUMMY_ASSISTANT_RESPONE = "dummy response"
################ END   : Global constants ################


################ BEGIN : Initialization steps ################
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

################ END   : Initialization steps ################


################ BEGIN : Querying steps ################
def get_assistant_response(user_message):
    def save_user_dialogue():
        try:
            request_path = FASTAPI_SERVER_API_PATH + "/conversational/"
            request_body = {"session_id": st.session_state.session_id, "content": user_message}
            requests.post(request_path, json=request_body)
        except ConnectionError:
            print("Cannot connect to server!!!")
        except JSONDecodeError:
            print("No valid response")
        except:
            print("Server error!!!")

    def get_assistant_response():
        try:
            request_path = FASTAPI_SERVER_API_PATH + "/conversational/" + st.session_state.openai_model \
                + "/" + st.session_state.session_id
            response = requests.get(request_path)
            json_response = response.json()
            return json_response["assistant_response"] if "assistant_response" in json_response else DEFAULT_DUMMY_ASSISTANT_RESPONE
        except ConnectionError:
            print("Cannot connect to server!!!")
        except JSONDecodeError:
            print("No valid assistant response")
        except:
            print("Server error!!!")

        return DEFAULT_DUMMY_ASSISTANT_RESPONE

    save_user_dialogue()
    return get_assistant_response()

################ END   : Querying steps ################


################ BEGIN : Rendering steps ################
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

################ END   : Rendering steps ################


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    MAX_DIALOGUE_TURNS = int(os.environ.get("STREAMLIT_MAX_DIALOGUE_TURNS", 20))

    app_initialization()
    render_frontend()
