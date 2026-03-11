import hashlib
import math
import re

from .settings_data import settings

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


class SimpleEmbeddingService:
    def __init__(self, size: int) -> None:
        self.size = size

    def embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.size
        tokens = TOKEN_PATTERN.findall(text.lower())

        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            bucket = int(digest[:8], 16) % self.size
            sign = 1.0 if int(digest[8:10], 16) % 2 == 0 else -1.0
            vector[bucket] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]


embedding_service = SimpleEmbeddingService(settings.embedding_size)
