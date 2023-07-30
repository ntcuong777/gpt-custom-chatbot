from pydantic import BaseModel


class ChatDialogueBase(BaseModel):
    session_id: str
    content: str
    role: str


class ChatDialogueCreate(ChatDialogueBase):
    pass


class ChatDialogue(ChatDialogueBase):
    sequence: int

    class Config:
        orm_mode = True
