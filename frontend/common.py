import requests
import streamlit as st

from json import JSONDecodeError

from common.constants import FASTAPI_SERVER_API_PATH


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
