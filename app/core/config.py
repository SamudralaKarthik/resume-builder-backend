# app/core/config.py
from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"  # You can change to gpt-4.1 or llama later

@lru_cache
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
    )
