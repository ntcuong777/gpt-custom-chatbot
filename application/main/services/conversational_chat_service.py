import os
import openai
from application.main.config import settings
from application.main.database.sql.schemas import ChatDialogueCreate
from application.main.database.sql import models
from application.main.database.sql import crud
from sqlalchemy.orm import Session
from application.initializer import LoggerInstance
from application.main.strategy.conversational import SimpleChatDialogueConstructorStrategy, AbstractChatDialogueConstructorStrategy

openai.api_key = os.environ["OPENAI_API_KEY"]
logger = LoggerInstance().get_logger(__name__)

class ConversationalChatService(object):
    chat_dialogue_constructor_strategy: AbstractChatDialogueConstructorStrategy = None

    def __init__(self, chat_dialogue_constructor_strategy) -> None:
        self.chat_dialogue_constructor_strategy = chat_dialogue_constructor_strategy


    def save_user_dialouge(self, db: Session, session_id: str, user_input: str):
        user_dialogue = ChatDialogueCreate(session_id=session_id, role="user", content=user_input)
        return crud.create_chat_dialogue(db, user_dialogue)


    def save_assistant_response(self, db: Session, session_id: str, assistant_response: str) -> models.ChatDialogue:
        assistant_dialogue = ChatDialogueCreate(session_id=session_id, role="assistant", content=assistant_response)
        return crud.create_chat_dialogue(db, assistant_dialogue)


    def get_assistant_response(self, db: Session, model: str, session_id: str) -> str:
        messages = self.chat_dialogue_constructor_strategy.construct_chat_dialogue(db, session_id)

        response = openai.ChatCompletion.create(model=model, messages=messages)
        assistant_response = response["choices"][0]["message"]["content"]

        self.save_assistant_response(db, session_id=session_id, assistant_response=assistant_response)

        return assistant_response


# Dependency
def get_conversational_chat_service():
    # Initialize service with corresponding strategy
    return ConversationalChatService(SimpleChatDialogueConstructorStrategy())