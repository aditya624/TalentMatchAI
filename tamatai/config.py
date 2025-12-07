from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class GroqConfig(BaseModel):
    api_key: str = os.getenv("GROQ_API_KEY", "")
    retry_count: int = int(os.getenv("GROQ_RETRY_COUNT", "2"))

class LangfuseConfig(BaseModel):
    system_prompt_name: str = os.getenv("LANGFUSE_SYSTEM_PROMPT_NAME", "match")
    system_prompt_version: str = os.getenv("LANGFUSE_SYSTEM_PROMPT_VERSION", None)

class OpenAIConfig(BaseModel):
    api_key: str = os.getenv("OPENAI_API_KEY", "")

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "orion")
    version: str = os.getenv("VERSION", "0.1.4")
    env: str = os.getenv("SERVICE_ENV", "local")
    token: str = os.getenv("TOKEN", "kajsdasdkjhsdf")
    request_timeout_s: int = int(os.getenv("REQUEST_TIMEOUT_S", "350"))
    
    groq: GroqConfig = GroqConfig()
    langfuse: LangfuseConfig = LangfuseConfig()
    openai: OpenAIConfig = OpenAIConfig()

settings = Settings()
