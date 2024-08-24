import json

from typing import AsyncIterator

from aiohttp.web_response import Response
from fastapi.routing import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from application.main.database.sql.schemas import ChatDialogueBase, ChatDialogue
from application.main.services.conversational_chat_service import get_conversational_chat_service, ConversationalChatService
from application.initializer import LoggerInstance

from ._chat_commons import ModelRequestBody

router = APIRouter(prefix='/conversational')
logger = LoggerInstance().get_logger(__name__)


@router.post("/")
async def conversational_chat(
        user_dialogue: ChatDialogueBase,
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
):
    session_id = user_dialogue.session_id
    user_content = user_dialogue.content
    dialogue = service.save_user_dialouge(db, session_id=session_id, user_input=user_content)
    return ChatDialogue(session_id=dialogue.session_id, sequence=dialogue.sequence, role=dialogue.role, content=dialogue.content)


@router.post("/{session_id}")
async def conversational_chat(
        session_id: str,
        req_body: ModelRequestBody,
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
):
    model = req_body.model  # TODO: include params
    service.save_user_dialouge(db, session_id=session_id, user_input=req_body.user_query)
    assistant_response = service.get_assistant_response(db, session_id, model=model)
    return {"assistant_response": assistant_response}


@router.post("/{session_id}/stream")
async def stream_conversational_chat(
        session_id: str,
        req_body: ModelRequestBody,
        db: Session = Depends(get_db_session),
        service: ConversationalChatService = Depends(get_conversational_chat_service)
):
    model = req_body.model  # TODO: include params
    service.save_user_dialouge(db, session_id=session_id, user_input=req_body.user_query)

    async def iter_response() -> AsyncIterator[bytes | str]:
        async for chunk in service.aget_assistant_response(db, session_id, model=model):
            resp_chunk = json.dumps({"assistant_response": chunk}, ensure_ascii=False)
            yield resp_chunk

    return StreamingResponse(iter_response(), media_type='text/event-stream')
