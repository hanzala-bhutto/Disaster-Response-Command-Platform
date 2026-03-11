from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    incident_service_url: str = Field(default="http://localhost:8001")
    coordination_service_url: str = Field(default="http://localhost:8002")
    notification_service_url: str = Field(default="http://localhost:8003")
    rag_service_url: str = Field(default="http://localhost:8004")


settings = Settings()
