from typing import List
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
