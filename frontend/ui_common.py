import requests
import traceback
import streamlit as st

from json import JSONDecodeError

from common.constants import FASTAPI_SERVER_API_PATH, MAX_DIALOGUE_TURNS, DUMMY_SESSION_ID


def get_user_session():
    if "session_id" not in st.session_state or st.session_state.session_id is None or st.session_state.session_id == DUMMY_SESSION_ID:
        try:
            request_path = FASTAPI_SERVER_API_PATH + "/user_session/new"
            response = requests.post(request_path, json={"model": st.session_state.llm_model})
            json_response = response.json()
            st.session_state["session_id"] = json_response["session_id"] if "session_id" in json_response else None
        except ConnectionError:
            print("Cannot connect to server!!!")
        except JSONDecodeError:
            print("No valid session_id response")
        except Exception:
            exc_details = traceback.format_exc()
            print(f"Error: {exc_details}")
            expander = st.expander("[Init] Exception occurred", icon="❌")
            expander.error(f"Error occurred while trying to get a new session. Using dummy session. Exception details:\n```{exc_details}```")

        if "session_id" not in st.session_state or st.session_state["session_id"] is None:
            st.session_state["session_id"] = DUMMY_SESSION_ID


def ensure_short_dialogue_history():
    if "messages" in st.session_state and len(st.session_state.messages) > MAX_DIALOGUE_TURNS:
        # remove previous history to save resource
        st.session_state.messages = st.session_state.messages[-MAX_DIALOGUE_TURNS:]
