from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_collection_name: str = Field(default="disaster_knowledge")
    embedding_size: int = Field(default=128)
    chunk_size_words: int = Field(default=120)
    chunk_overlap_words: int = Field(default=30)


settings = Settings()
