from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from application.main.database.sql.sqlite import get_db_session
from application.main.database.sql.schemas import DocumentCreate, DocumentBase
from application.main.services.document_question_answering_service import get_document_question_answering_service, DocumentQuestionAnsweringService
from application.initializer import LoggerInstance

router = APIRouter(prefix='/doc_qa')
logger = LoggerInstance().get_logger(__name__)


@router.post("/")
async def save_doc(
        doc: DocumentCreate,
        db: Session = Depends(get_db_session),
        service: DocumentQuestionAnsweringService = Depends(get_document_question_answering_service)
):
    session_id = doc.session_id
    doc_content = doc.doc_content
    service.save_doc(db, session_id=session_id, doc_content=doc_content)
    return "ok"


@router.get("/{model}/{session_id}")
async def question_answering(
        model: str,
        session_id: str,
        question: str,
        db: Session = Depends(get_db_session),
        service: DocumentQuestionAnsweringService = Depends(get_document_question_answering_service)
):
    return {"assistant_response": "Not implemented yet"}
    assistant_response = service.get_assistant_response(db, model, session_id, question)
    return {"assistant_response": assistant_response}
