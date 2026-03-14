import json
from typing import Any

import pika
from pika.exceptions import AMQPError

from .metrics import record_event_publish
from .settings_data import settings


class EventPublisher:
    def publish(self, routing_key: str, payload: dict[str, Any]) -> None:
        parameters = pika.URLParameters(settings.rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
        channel.basic_publish(
            exchange=settings.rabbitmq_exchange,
            routing_key=routing_key,
            body=json.dumps(payload).encode("utf-8"),
            properties=pika.BasicProperties(content_type="application/json", delivery_mode=2),
        )
        connection.close()


publisher = EventPublisher()


def safe_publish(routing_key: str, payload: dict[str, Any]) -> bool:
    try:
        publisher.publish(routing_key, payload)
        record_event_publish(routing_key, "success")
        return True
    except AMQPError:
        record_event_publish(routing_key, "error")
        return False
