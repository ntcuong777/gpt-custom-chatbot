from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from application.main.database.sql.schemas import ChatDialogueBase, ChatDialogue
from application.main.services.conversational_chat_service import get_conversational_chat_service, ConversationalChatService
from application.initializer import LoggerInstance

router = APIRouter(prefix='/conversational')
logger = LoggerInstance().get_logger(__name__)

@router.post("/")
def conversational_chat(
        user_dialogue: ChatDialogueBase, 
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
):
    session_id = user_dialogue.session_id
    user_content = user_dialogue.content
    logger.debug("Session ID = %s, user input = %s", session_id, user_content)

    dialogue = service.save_user_dialouge(db, session_id=session_id, user_input=user_content)
    return ChatDialogue(session_id=dialogue.session_id, sequence=dialogue.sequence, role=dialogue.role, content=dialogue.content)


@router.get("/{model}/{session_id}")
def conversational_chat(
        model: str,
        session_id: str,
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
):
    assistant_response = service.get_assistant_response(db, model, session_id)
    logger.debug("Session ID = %s, assistant response = %s", session_id, assistant_response)

    return {"assistant_response": assistant_response}