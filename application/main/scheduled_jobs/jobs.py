import json
import os
import requests

from application.main.database.sql import crud
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from common.config import settings


def remove_stale_chats(days: int = 7):
    # Remove chat sessions that have no dialogues
    db: Session = next(get_db_session())
    crud.ChatSessionCrud.delete_stale_chat_sessions(db, days)


def remove_empty_chats():
    # Remove chat sessions that have no dialogues
    db: Session = next(get_db_session())
    crud.ChatSessionCrud.delete_empty_chat_sessions(db)


def fetch_openrouter_models_info():
    data_dir = os.path.join(settings.BASE_DIR, "data")
    model_info_file = os.path.join(data_dir, "openrouter_models_info.json")
    if os.path.exists(model_info_file):
        api_url = "https://openrouter.ai/api/v1/models"
        response = requests.get(api_url)
        s = json.dumps(response.json(), ensure_ascii=False)
        with open(model_info_file, "r") as f:
            prev_s = f.read()

        if prev_s != s:
            with open(model_info_file, "w") as f:
                f.write(s)
