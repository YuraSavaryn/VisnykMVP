from pydantic import BaseModel


class ChatMessage(BaseModel):
    session_id: int
    content: str
