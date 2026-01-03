from fastapi import APIRouter

from models.message import ChatMessage
from services.agent_service.agent_core import call_agent

router = APIRouter(tags=["agent"])


@router.post("/inference")
async def agent_inference(message: ChatMessage):
    return await call_agent(message.session_id, message.content)
