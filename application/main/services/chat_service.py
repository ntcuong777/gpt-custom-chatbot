import os
import openai

from typing import Generator, AsyncIterable
from sqlalchemy.orm import Session

from application.main.chains import get_langchain_chain, get_langchain_custom_model_kwargs_chain

from application.main.database.sql.schemas import ChatDialogueCreate
from application.main.database.sql import models
from application.main.database.sql import crud
from application.initializer import LoggerInstance
from application.main.strategy.chat import SimpleChatDialogueConstructorStrategy, AbstractChatDialogueConstructorStrategy

from .base_service import BaseService

openai.api_key = os.environ["OPENAI_API_KEY"]
logger = LoggerInstance().get_logger(__name__)


class ConversationalChatService(BaseService):
    chat_dialogue_constructor_strategy: AbstractChatDialogueConstructorStrategy = None

    def __init__(self, chat_dialogue_constructor_strategy) -> None:
        self.chat_dialogue_constructor_strategy = chat_dialogue_constructor_strategy

    def save_user_dialouge(self, db: Session, session_id: str, user_input: str) -> models.ChatDialogue:
        user_dialogue = ChatDialogueCreate(session_id=session_id, role="user", content=user_input)
        return crud.ChatDialogueCrud.create_chat_dialogue(db, user_dialogue)

    def save_assistant_response(self, db: Session, session_id: str, assistant_response: str) -> models.ChatDialogue:
        assistant_dialogue = ChatDialogueCreate(session_id=session_id, role="assistant", content=assistant_response)
        return crud.ChatDialogueCrud.create_chat_dialogue(db, assistant_dialogue)

    def get_assistant_response(self, db: Session, session_id: str, model: str = "gpt-4o-mini", **model_kwargs) -> str:
        messages = self.chat_dialogue_constructor_strategy.construct_chat_dialogue(db, session_id)

        llm_chain = get_langchain_chain(model) if len(model_kwargs) == 0 else get_langchain_custom_model_kwargs_chain(model, **model_kwargs)
        assistant_response = llm_chain.invoke(messages)

        self.save_assistant_response(db, session_id=session_id, assistant_response=assistant_response)

        return assistant_response

    async def aget_assistant_response(self, db: Session, session_id: str, model: str = "gpt-4o-mini", **model_kwargs) -> AsyncIterable[str]:
        messages = self.chat_dialogue_constructor_strategy.construct_chat_dialogue(db, session_id)

        llm_chain = get_langchain_chain(model) if len(model_kwargs) == 0 else get_langchain_custom_model_kwargs_chain(model, **model_kwargs)
        assistant_response = ""
        async for chunk in llm_chain.astream(messages):
            assistant_response += chunk
            yield chunk

        self.save_assistant_response(db, session_id=session_id, assistant_response=assistant_response)


# Dependency
def get_conversational_chat_service():
    # Initialize service with corresponding strategy
    return ConversationalChatService(SimpleChatDialogueConstructorStrategy())
