from typing import Any

from pydantic import BaseModel


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    request_id: str
    message: str
    intent: str
    action: str
    result: dict[str, Any]
    response: str


class AgentChatRequest(BaseModel):
    message: str
    user_id: str = "demo-user"
    session_id: str | None = None


class AgentChatResponse(BaseModel):
    session_id: str
    response: str
