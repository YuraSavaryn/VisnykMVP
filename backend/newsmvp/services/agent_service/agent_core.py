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
    if isinstance(final_message.content, list):
        first_item = final_message.content[0]
        if isinstance(first_item, dict) and "text" in first_item:
            return first_item["text"]
        return str(first_item)
    return final_message.content
