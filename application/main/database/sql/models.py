from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey, DateTime, orm, exc
from sqlalchemy.orm import relationship, Mapped

from application.main.database.sql.sqlite import Base

from snowflake import SnowflakeGenerator


class IdGenerator:
    # singleton instance
    _instance = None

    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls.instance = super(IdGenerator, cls).__new__(cls)
            cls._instance.snowflake = SnowflakeGenerator(18)
        return cls._instance

    def __iter__(self):
        return iter(self.snowflake)

    def __next__(self):
        return next(self.snowflake)


class BaseDbModel(Base):
    __abstract__ = True
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, default=IdGenerator())
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class ChatSession(BaseDbModel):
    __tablename__ = "chat_sessions"

    session_id: Mapped[str] = Column(String, index=True, nullable=False, unique=True)
    user_id: Mapped[str] = Column(String, index=True, default="anonymous")
    model: Mapped[str] = Column(String, nullable=False)


class ChatDialogue(BaseDbModel):
    __tablename__ = "chat_dialogues"

    session_id: Mapped[str] = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    sequence: Mapped[int] = Column(Integer, index=True, nullable=False)
    role: Mapped[str] = Column(String, nullable=False)
    content: Mapped[str] = Column(String, nullable=False)


class Document(BaseDbModel):
    __tablename__ = "documents"

    session_id: Mapped[str] = Column(String, ForeignKey("chat_sessions.id", ondelete="CASCADE"), index=True, nullable=False)
    doc_content: Mapped[str] = Column(UnicodeText, nullable=False)

    embeddings: Mapped[List["DocumentEmbeddings"]] = relationship("DocumentEmbeddings", back_populates="document")


class DocumentEmbeddings(BaseDbModel):
    __tablename__ = "document_embeddings"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    doc_part: Mapped[str] = Column(UnicodeText, nullable=False)
    doc_part_idx: Mapped[int] = Column(Integer, nullable=False, index=True)
    embedding_vector: Mapped[str] = Column(UnicodeText, nullable=False)

    document_id: Mapped[int] = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    document: Mapped[Document] = relationship("Document", back_populates="embeddings", cascade="all, delete")
