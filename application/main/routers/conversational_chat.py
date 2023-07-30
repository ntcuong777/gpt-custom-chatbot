from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from application.main.database.sql.schemas import ChatDialogueCreate
from application.main.services.conversational_chat_service import get_conversational_chat_service, ConversationalChatService
from application.initializer import LoggerInstance

router = APIRouter(prefix='/conversational')
logger = LoggerInstance().get_logger(__name__)

@router.get("/{model}")
def conversational_chat(
        model: str,
        user_dialogue: ChatDialogueCreate, 
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
    ):

    assistant_response = service.get_assistant_response(db, model, user_dialogue)
    return assistant_response