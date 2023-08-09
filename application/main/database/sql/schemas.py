from pydantic import BaseModel
from typing import List


################# START: Model for chat dialogue function #################
class ChatDialogueBase(BaseModel):
    session_id: str
    content: str


class ChatDialogueCreate(ChatDialogueBase):
    role: str


class ChatDialogue(ChatDialogueCreate):
    sequence: int

    class Config:
        orm_mode = True

################# END: Model for chat dialogue function #################


################# START: Model for document QA function #################
# ----- Base model ------
class DocumentBase(BaseModel):
    session_id: str
    doc_content: str


class DocumentEmbeddingsBase(BaseModel):
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
        orm_mode = True


class DocumentEmbeddings(DocumentEmbeddingsCreate):
    id: int

    class Config:
        orm_mode = True


################# START: Model for document QA function #################