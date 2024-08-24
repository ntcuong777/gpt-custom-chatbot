from typing import List

from aiohttp.web_routedef import static
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from sqlalchemy.exc import MultipleResultsFound

from application.main.database.sql import models, schemas


class ChatDialogueCrud:
    @staticmethod
    def fetch_all_dialogues_given_session_id(db: Session, session_id: str, max_results: int = 100) -> List[models.ChatDialogue]:
        query = select(models.ChatDialogue).where(models.ChatDialogue.session_id == session_id)\
            .order_by(models.ChatDialogue.sequence.desc()).limit(max_results)
        return db.scalars(query).all()

    @staticmethod
    def count_dialogues_given_session_id(db: Session, session_id: str) -> int:
        query = select(func.count()).select_from(models.ChatDialogue).where(models.ChatDialogue.session_id == session_id)
        return db.execute(query).scalar_one()

    @staticmethod
    def create_chat_dialogue(db: Session, dialogue: schemas.ChatDialogueCreate) -> models.ChatDialogue:
        new_sequence = ChatDialogueCrud.count_dialogues_given_session_id(db, dialogue.session_id) + 1
        db_chat_dialogue = models.ChatDialogue(session_id=dialogue.session_id, sequence=new_sequence, role=dialogue.role, content=dialogue.content)
        db.add(db_chat_dialogue)
        db.commit()
        db.refresh(db_chat_dialogue)
        return db_chat_dialogue


class DocumentCrud:
    @staticmethod
    def fetch_single_document_given_session_id(db: Session, session_id: str) -> models.Document:
        query = select(models.Document).where(models.Document.session_id == session_id)
        results = db.scalars(query).all()
        if len(results) > 0:
            raise MultipleResultsFound()
        else:
            return results[0]

    @staticmethod
    def fetch_single_document_given_session_id_eagerly_fetch_embeddings(db: Session, session_id: str) -> models.Document:
        query = select(models.Document).where(models.Document.session_id == session_id)\
            .options(joinedload(models.Document.embeddings))
        results = db.scalars(query).all()
        if len(results) > 0:
            raise MultipleResultsFound()
        else:
            return results[0]

    @staticmethod
    def create_document_without_embeddings(db: Session, session_id: str, doc_content: str) -> models.Document:
        doc = models.Document(session_id=session_id, doc_content=doc_content)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc


class ChatSessionCrud:
    @staticmethod
    def fetch_single_session_given_id(db: Session, session_id: str) -> models.ChatSession | None:
        query = select(models.ChatSession).where(models.ChatSession.session_id == session_id)
        results = db.scalars(query).all()
        if len(results) > 1:
            raise MultipleResultsFound()
        elif len(results) > 0:
            return results[0]
        else:
            return None

    @staticmethod
    def create_chat_session(db: Session, chat_session: schemas.ChatSessionCreate) -> models.ChatSession:
        chat_session = models.ChatSession(session_id=chat_session.session_id, user_id=chat_session.user_id, model=chat_session.model)
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        return chat_session

    @staticmethod
    def delete_stale_chat_sessions(db: Session, days: int):
        query = select(models.ChatSession).where(models.ChatSession.created_at < func.now() - func.interval(days, "day"))
        stale_sessions = db.scalars(query).all()
        for session in stale_sessions:
            db.delete(session)
        db.commit()
        return

    @staticmethod
    def delete_empty_chat_sessions(db: Session):
        query = select(models.ChatSession).join(models.ChatDialogue).group_by(models.ChatSession.session_id).having(func.count(models.ChatDialogue.id) == 0)
        empty_sessions = db.scalars(query).all()
        for session in empty_sessions:
            db.delete(session)
        db.commit()
        return

    @staticmethod
    def update_chat_session_system_message(db: Session, session_id: str, system_message: str) -> models.ChatSession:
        chat_session = ChatSessionCrud.fetch_single_session_given_id(db, session_id)
        chat_session.system_message = system_message
        db.commit()
        db.refresh(chat_session)
        return chat_session
