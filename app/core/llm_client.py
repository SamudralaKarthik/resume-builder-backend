# app/core/llm_client.py
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .config import get_settings
from langsmith import traceable

settings = get_settings()

llm = ChatOpenAI(
    model=settings.openai_model,   # IMPORTANT FIX
    api_key=(settings.openai_api_key or "").strip(),
)

@traceable(name="llm_call_resume_builder")
def call_llm(system_prompt: str, user_prompt: str) -> str:
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = llm.invoke(messages)
    print(response)
    return response.content
