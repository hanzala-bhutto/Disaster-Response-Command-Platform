import json
import logging
from typing import Any

from kafka import KafkaProducer
from kafka.errors import KafkaError

from .metrics import record_event_publish
from .settings_data import settings

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self) -> None:
        self._producer: KafkaProducer | None = None

    def _get_producer(self) -> KafkaProducer:
        if self._producer is None:
            self._producer = KafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
                value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                key_serializer=lambda value: value.encode("utf-8") if value else None,
                acks="all",
            )
        return self._producer

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        key = payload.get("event_type", topic)
        future = self._get_producer().send(topic, key=key, value=payload)
        future.get(timeout=10)
        self._get_producer().flush()


publisher = EventPublisher()


def safe_publish(topic: str, payload: dict[str, Any]) -> bool:
    try:
        publisher.publish(topic, payload)
        record_event_publish(topic, "success")
        return True
    except KafkaError:
        logger.exception("Failed to publish Kafka event", extra={"topic": topic})
        record_event_publish(topic, "error")
        return False
