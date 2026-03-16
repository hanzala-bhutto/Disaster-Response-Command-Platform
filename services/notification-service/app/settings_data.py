from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    incident_created_topic: str = Field(default="incident.created")
    task_created_topic: str = Field(default="task.created")
    notification_consumer_group: str = Field(default="notification-service")


settings = Settings()
