from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    incident_created_topic: str = Field(default="incident.created")


settings = Settings()
