from pydantic import BaseModel
from typing import List


class BaseDbModel(BaseModel):
    pass


class ChatSessionBase(BaseDbModel):
    session_id: str
    user_id: str = "anonymous"
    model: str


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSession(ChatSessionBase):
    class Config:
        from_attributes = True


################# START: Model for chat dialogue function #################
class ChatDialogueBase(BaseDbModel):
    session_id: str
    content: str
    role: str


class ChatDialogueCreate(ChatDialogueBase):
    pass


class ChatDialogue(ChatDialogueCreate):
    sequence: int

    class Config:
        from_attributes = True

################# END: Model for chat dialogue function #################


################# START: Model for document QA function #################
# ----- Base model ------
class DocumentBase(BaseDbModel):
    session_id: str
    doc_content: str


class DocumentEmbeddingsBase(BaseDbModel):
    doc_part: str
    doc_part_idx: int
    embedding_vector: str
    document: DocumentBase


# ----- Models for creation ------
class DocumentCreate(DocumentBase):
    pass


class DocumentEmbeddingsCreate(DocumentBase):
    pass


# ----- Models for reading ------
class Document(DocumentCreate):
    embeddings: List[DocumentEmbeddingsBase]

    class Config:
        from_attributes = True


class DocumentEmbeddings(DocumentEmbeddingsCreate):
    class Config:
        from_attributes = True


################# START: Model for document QA function #################