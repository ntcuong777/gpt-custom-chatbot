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

    # def before_save(self, *args, **kwargs):
    #     pass
    #
    # def after_save(self, *args, **kwargs):
    #     pass
    #
    # def save(self, commit=True):
    #     self.before_save()
    #     db.session.add(self)
    #     if commit:
    #         try:
    #             db.session.commit()
    #         except Exception as e:
    #             db.session.rollback()
    #             raise e
    #
    #     self.after_save()
    #
    # def before_update(self, *args, **kwargs):
    #     pass
    #
    # def after_update(self, *args, **kwargs):
    #     pass
    #
    # def update(self, *args, **kwargs):
    #     self.before_update(*args, **kwargs)
    #     db.session.commit()
    #     self.after_update(*args, **kwargs)
    #
    # def delete(self, commit=True):
    #     db.session.delete(self)
    #     if commit:
    #         db.session.commit()
    #
    # @classmethod
    # def eager(cls, *args):
    #     cols = [orm.joinedload(arg) for arg in args]
    #     return cls.query.options(*cols)
    #
    # @classmethod
    # def before_bulk_create(cls, iterable, *args, **kwargs):
    #     pass
    #
    # @classmethod
    # def after_bulk_create(cls, model_objs, *args, **kwargs):
    #     pass
    #
    # @classmethod
    # def bulk_create(cls, iterable, *args, **kwargs):
    #     cls.before_bulk_create(iterable, *args, **kwargs)
    #     model_objs = []
    #     for data in iterable:
    #         if not isinstance(data, cls):
    #             data = cls(**data)
    #         model_objs.append(data)
    #
    #     db.session.bulk_save_objects(model_objs)
    #     if kwargs.get('commit', True) is True:
    #         db.session.commit()
    #     cls.after_bulk_create(model_objs, *args, **kwargs)
    #     return model_objs
    #
    # @classmethod
    # def bulk_create_or_none(cls, iterable, *args, **kwargs):
    #     try:
    #         return cls.bulk_create(iterable, *args, **kwargs)
    #     except exc.IntegrityError as e:
    #         db.session.rollback()
    #         return None


class ChatDialogue(BaseDbModel):
    __tablename__ = "chat_dialogue"

    session_id: Mapped[str] = Column(String, index=True)
    sequence: Mapped[int] = Column(Integer, index=True)
    role: Mapped[str] = Column(String, nullable=False)
    content: Mapped[str] = Column(String, nullable=False)


class Document(BaseDbModel):
    __tablename__ = "document"

    session_id: Mapped[str] = Column(String, primary_key=True, index=True)
    doc_content: Mapped[str] = Column(UnicodeText, nullable=False)

    embeddings: Mapped[List["DocumentEmbeddings"]] = relationship("DocumentEmbeddings", back_populates="document")


class DocumentEmbeddings(BaseDbModel):
    __tablename__ = "document_embeddings"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    doc_part: Mapped[str] = Column(UnicodeText, nullable=False)
    doc_part_idx: Mapped[int] = Column(Integer, nullable=False)
    embedding_vector: Mapped[str] = Column(UnicodeText, nullable=False)

    document_id: Mapped[int] = Column(Integer, ForeignKey("document.id"))
    document: Mapped[Document] = relationship("Document", back_populates="embeddings")
