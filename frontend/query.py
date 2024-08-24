import requests
import streamlit as st

from json import JSONDecodeError

from .constants import *


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
