from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbitmq_url: str = Field(default="amqp://guest:guest@localhost:5672/%2F")
    rabbitmq_exchange: str = Field(default="disaster_events")
    incident_queue_name: str = Field(default="coordination.incident.created")


settings = Settings()
