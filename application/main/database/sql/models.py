from sqlalchemy import Column, Integer, String

from application.main.database.sql.sqlite import Base


class ChatDialogue(Base):
    __tablename__ = "chat_dialogue"

    session_id = Column(String, primary_key=True, index=True)
    sequence = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

