from typing import List
from sqlalchemy import Column, Integer, String, UnicodeText
from sqlalchemy.orm import relationship, Mapped

from application.main.database.sql.sqlite import Base


class ChatDialogue(Base):
    __tablename__ = "chat_dialogue"

    session_id: Mapped[str] = Column(String, primary_key=True, index=True)
    sequence: Mapped[int] = Column(Integer, primary_key=True, index=True)
    role: Mapped[str] = Column(String, nullable=False)
    content: Mapped[str] = Column(String, nullable=False)


class Document(Base):
    __tablename__ = "document"

    session_id: Mapped[str] = Column(String, primary_key=True, index=True)
    doc_content: Mapped[str] = Column(UnicodeText, nullable=False)

    embeddings: Mapped[List["DocumentEmbeddings"]] = relationship("DocumentEmbeddings", back_populates="document")


class DocumentEmbeddings(Base):
    __tablename__ = "document_embeddings"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    doc_part: Mapped[str] = Column(UnicodeText, nullable=False)
    doc_part_idx: Mapped[int] = Column(Integer, nullable=False)
    embedding_vector: Mapped[str] = Column(UnicodeText, nullable=False)

    document: Mapped[Document] = relationship("Document", back_populates="embeddings")
