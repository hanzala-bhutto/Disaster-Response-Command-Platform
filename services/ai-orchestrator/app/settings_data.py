from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    incident_service_url: str = Field(default="http://localhost:8001")
    coordination_service_url: str = Field(default="http://localhost:8002")
    notification_service_url: str = Field(default="http://localhost:8003")
    rag_service_url: str = Field(default="http://localhost:8004")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    llm_api_key: str | None = Field(default=None)
    llm_model: str | None = Field(default=None)
    llm_timeout_seconds: float = Field(default=30.0)


settings = Settings()
