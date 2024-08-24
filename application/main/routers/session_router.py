from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from application.main.services.chat_session_service import get_chat_session_service, ChatSessionService
from application.initializer import LoggerInstance

from ._router_models import NewSessionBody, UpdateSysMsgBody

router = APIRouter(prefix='/user_session')
logger = LoggerInstance().get_logger(__name__)


@router.post("/new")
async def conversational_chat(
        req_body: NewSessionBody,
        db: Session = Depends(get_db_session),
        service: ChatSessionService = Depends(get_chat_session_service)
):
    session_id = service.create_new_session_id(db)
    logger.debug("Session ID = %s has been connected", session_id)
    service.persist_session(db, session_id, model=req_body.model, user_id=req_body.user_id)
    return {"session_id": session_id}


@router.post("/set-system-message")
async def set_system_message(
        req_body: UpdateSysMsgBody,
        db: Session = Depends(get_db_session),
        service: ChatSessionService = Depends(get_chat_session_service)
):
    service.set_system_message(db, req_body.session_id, system_message=req_body.system_message)
    return {"result": "ok"}
