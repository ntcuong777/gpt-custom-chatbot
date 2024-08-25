from abc import ABC, abstractmethod
from typing import List, Dict
from sqlalchemy.orm import Session
from common.config import settings
from common.logging import LoggerInstance
from application.main.database.sql import crud
from application.main.decorator import overrides

from datetime import datetime

logger = LoggerInstance().get_logger(__name__)
_time_str = f"* Today is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (UTC)"


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
        global _time_str

        messages = [{"role": "system", "content": f"You are a helpful assistant.\n\n{_time_str}"}]
        chat_session = crud.ChatSessionCrud.fetch_single_session_given_id(db, session_id)
        if chat_session.system_message:
            messages = [{"role": "system", "content": f"{chat_session.system_message}\n\n\n{_time_str}"}]
        message_history = crud.ChatDialogueCrud.fetch_all_dialogues_given_session_id(
            db, session_id=session_id, max_results=self.num_previous_dialogues)
        for dialogue in message_history:
            message = {"role": dialogue.role, "content": dialogue.content}
            messages.append(message)

        return messages
