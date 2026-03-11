from qdrant_client import QdrantClient, models

from .settings_data import settings


class QdrantRepository:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.qdrant_collection_name

    def ensure_collection(self) -> None:
        if self.client.collection_exists(self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=settings.embedding_size, distance=models.Distance.COSINE),
        )

    def upsert_points(self, points: list[models.PointStruct]) -> None:
        if not points:
            return
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, vector: list[float], limit: int, incident_type: str | None = None):
        query_filter = None
        if incident_type:
            query_filter = models.Filter(
                must=[models.FieldCondition(key="incident_type", match=models.MatchValue(value=incident_type))]
            )

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            query_filter=query_filter,
        )


repository = QdrantRepository()
