import os
from dotenv import load_dotenv, find_dotenv

from frontend.init import app_initialization
from frontend.render import render_frontend


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    MAX_DIALOGUE_TURNS = int(os.environ.get("STREAMLIT_MAX_DIALOGUE_TURNS", 20))

    app_initialization()
    render_frontend()
