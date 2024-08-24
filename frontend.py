import os
from dotenv import load_dotenv, find_dotenv

from frontend.init_ui_state import app_initialization
from frontend.chat_interface_render import render_chat_interface


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    MAX_DIALOGUE_TURNS = int(os.environ.get("STREAMLIT_MAX_DIALOGUE_TURNS", 20))

    app_initialization()
    render_chat_interface()
