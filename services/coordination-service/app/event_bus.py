import json
import logging
import threading
import time
from typing import Any, Callable

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from .metrics import record_event_consumed, record_event_publish
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


def start_incident_consumer(on_message: Callable[[dict[str, Any]], None]) -> None:
    def consume() -> None:
        while True:
            consumer: KafkaConsumer | None = None
            try:
                consumer = KafkaConsumer(
                    settings.incident_created_topic,
                    bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
                    group_id=settings.coordination_consumer_group,
                    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
                    key_deserializer=lambda value: value.decode("utf-8") if value else None,
                    enable_auto_commit=True,
                    auto_offset_reset="earliest",
                )
                for message in consumer:
                    try:
                        on_message(message.value)
                    except Exception:
                        record_event_consumed(message.topic, "error")
                        logger.exception("Kafka consumer handler failed", extra={"topic": message.topic})
                    else:
                        record_event_consumed(message.topic, "success")
            except KafkaError:
                logger.exception("Incident Kafka consumer failed")
                time.sleep(5)
            finally:
                if consumer is not None:
                    consumer.close()

    thread = threading.Thread(target=consume, daemon=True, name="coordination-incident-consumer")
    thread.start()
