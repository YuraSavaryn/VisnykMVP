from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from .agent_config import model, SYSTEM_PROMPT
from .tools import tools

load_dotenv()

memory = MemorySaver()

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory,
)


async def call_agent(thread_id: int, query: str) -> str:
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 10}

    resp = agent.invoke({"messages": [("user", query)]}, config=config)

    final_message = resp["messages"][-1]
    return final_message.content[0]["text"]
