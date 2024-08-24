import secrets

from sqlalchemy.orm import Session

from application.main.database.sql.schemas import ChatSessionCreate
from application.main.database.sql import models
from application.main.database.sql import crud
from application.initializer import LoggerInstance

from .base_service import BaseService

logger = LoggerInstance().get_logger(__name__)


class ChatSessionService(BaseService):
    @staticmethod
    def _new_session_id():
        """
        Creates a cryptographically-secure, URL-safe string
        """
        return secrets.token_urlsafe(256)

    def create_new_session_id(self, db: Session) -> str:
        session_id = self._new_session_id()
        logger.debug("Session ID = %s has been connected", session_id)
        return session_id

    def persist_session(self, db: Session, session_id: str, model: str, user_id: str = "anonymous") -> models.ChatSession:
        chat_session = ChatSessionCreate(session_id=session_id, user_id=user_id, model=model)
        return crud.ChatSessionCrud.create_chat_session(db, chat_session)


# Dependency
def get_chat_session_service():
    # Initialize service with corresponding strategy
    return ChatSessionService()
