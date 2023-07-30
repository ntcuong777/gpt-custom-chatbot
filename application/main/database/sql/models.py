from sqlalchemy import Column, Integer, String

from application.main.database.sql.sqlite import Base


class ChatDialogue(Base):
    __tablename__ = "chat_history"

    session_id = Column(String, primary_key=True, index=True)
    sequence = Column(Integer, nullable=False, unique=False, index=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)

