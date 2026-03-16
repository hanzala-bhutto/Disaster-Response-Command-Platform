import json
import logging
import threading
import time
from typing import Any, Callable

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from .metrics import record_event_consumed
from .settings_data import settings

logger = logging.getLogger(__name__)


def start_notification_consumer(on_message: Callable[[str, dict[str, Any]], None]) -> None:
    def consume() -> None:
        while True:
            consumer: KafkaConsumer | None = None
            try:
                consumer = KafkaConsumer(
                    settings.incident_created_topic,
                    settings.task_created_topic,
                    bootstrap_servers=settings.kafka_bootstrap_servers.split(","),
                    group_id=settings.notification_consumer_group,
                    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
                    key_deserializer=lambda value: value.decode("utf-8") if value else None,
                    enable_auto_commit=True,
                    auto_offset_reset="earliest",
                )
                for message in consumer:
                    try:
                        on_message(message.topic, message.value)
                    except Exception:
                        record_event_consumed(message.topic, "error")
                        logger.exception("Kafka notification handler failed", extra={"topic": message.topic})
                    else:
                        record_event_consumed(message.topic, "success")
            except KafkaError:
                logger.exception("Notification Kafka consumer failed")
                time.sleep(5)
            finally:
                if consumer is not None:
                    consumer.close()

    thread = threading.Thread(target=consume, daemon=True, name="notification-consumer")
    thread.start()
