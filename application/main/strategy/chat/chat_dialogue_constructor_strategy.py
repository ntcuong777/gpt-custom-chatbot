from abc import ABC, abstractmethod
from typing import List, Dict
from sqlalchemy.orm import Session
from common.config import settings
from application.initializer import LoggerInstance
from application.main.database.sql import crud
from application.main.decorator import overrides


logger = LoggerInstance().get_logger(__name__)


class AbstractChatDialogueConstructorStrategy(ABC):
    """
    Using strategy pattern to make future app extension easier for chat ChatGPT API.
    For example, we might choose to construct chat dialogue history by taking dialogues that are
    semantically equivalent for the current user chat message using OpenAI's embeddings API
    """
    @abstractmethod
    def construct_chat_dialogue(self, db: Session, session_id: str) -> List[Dict]:
        raise NotImplementedError()


class SimpleChatDialogueConstructorStrategy(AbstractChatDialogueConstructorStrategy):
    def __init__(self):
        self.num_previous_dialogues = settings.APP_CONFIG.NUM_PREVIOUS_DIALOGUES

    @overrides(AbstractChatDialogueConstructorStrategy)
    def construct_chat_dialogue(self, db: Session, session_id: str) -> List[Dict]:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        message_history = crud.ChatDialogueCrud.fetch_all_dialogues_given_session_id(
            db, session_id=session_id, max_results=self.num_previous_dialogues)
        for dialogue in message_history:
            message = {"role": dialogue.role, "content": dialogue.content}
            messages.append(message)

        return messages
