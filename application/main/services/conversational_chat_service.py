import os
import openai
from typing import List
from application.main.config import settings
from application.main.database.sql.schemas import ChatDialogueCreate
from application.main.database.sql import crud
from sqlalchemy.orm import Session

openai.api_key = os.environ["OPENAI_API_KEY"]

class ConversationalChatService(object):

    def __init__(self) -> None:
        self.num_previous_dialogues = settings.APP_CONFIG.NUM_PREVIOUS_DIALOGUES


    def construct_chat_dialogue(self, db: Session, user_dialogue: ChatDialogueCreate) -> List[str]:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        message_history = crud.fetch_all_dialogues_given_session_id(db, session_id=user_dialogue.session_id, \
            max_results=self.num_previous_dialogues)[::-1]
        for dialogue in message_history:
            message = {"role": dialogue.role, "content": dialogue.content}
            messages.append(message)

        return messages


    def save_assistant_response(self, db: Session, session_id: str, assistant_response: str):
        assistant_dialogue = ChatDialogueCreate(session_id=session_id, role="assistant", content=assistant_response)
        crud.create_chat_dialogue(db, assistant_dialogue)


    def get_assistant_response(self, db: Session, model: str, user_dialogue: ChatDialogueCreate) -> str:
        messages = self.construct_chat_dialogue(db, user_dialogue)

        response = openai.ChatCompletion.create(model=model, messages=messages)
        assistant_response = response["choices"][0]["message"]["content"].replace("\n", "").replace("\t", "") # simple post-processing

        self.save_assistant_response(db, session_id=user_dialogue.session_id, assistant_response=assistant_response)

        return assistant_response


# Dependency
def get_conversational_chat_service():
    return ConversationalChatService()