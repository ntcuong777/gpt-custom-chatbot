from sqlalchemy.orm import Session
from sqlalchemy import select, func

from application.main.database.sql import models, schemas


def fetch_all_dialogues_given_session_id(db: Session, session_id: str, max_results: int = 100):
    query = select(models.ChatDialogue).where(models.ChatDialogue.session_id == session_id)\
        .order_by(models.ChatDialogue.sequence.desc()).limit(max_results)
    return db.scalars(query).all()


def count_dialogues_given_session_id(db: Session, session_id: str):
    query = select(func.count()).select_from(models.ChatDialogue).where(models.ChatDialogue.session_id == session_id)
    return db.execute(query).scalar_one()


def create_chat_dialogue(db: Session, dialogue: schemas.ChatDialogueCreate):
    new_sequence = count_dialogues_given_session_id(db, dialogue.session_id) + 1
    db_chat_dialogue = models.ChatDialogue(session_id=dialogue.session_id, sequence=new_sequence, role=dialogue.role, content=dialogue.content)
    db.add(db_chat_dialogue)
    db.commit()
    db.refresh(db_chat_dialogue)
    return db_chat_dialogue
