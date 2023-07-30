from pydantic import BaseModel


class ChatDialogueBase(BaseModel):
    session_id: str
    content: str


class ChatDialogueCreate(ChatDialogueBase):
    role: str


class ChatDialogue(ChatDialogueCreate):
    sequence: int

    class Config:
        orm_mode = True
