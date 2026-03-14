import json
import logging
import threading
from typing import Any, Callable

import pika
from pika.exceptions import AMQPError

from .metrics import record_event_consumed, record_event_publish
from .settings_data import settings

logger = logging.getLogger(__name__)


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
        logger.exception("Failed to publish event", extra={"routing_key": routing_key})
        record_event_publish(routing_key, "error")
        return False


def start_incident_consumer(on_message: Callable[[dict[str, Any]], None]) -> None:
    def consume() -> None:
        try:
            parameters = pika.URLParameters(settings.rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
            channel.queue_declare(queue=settings.incident_queue_name, durable=True)
            channel.queue_bind(
                exchange=settings.rabbitmq_exchange,
                queue=settings.incident_queue_name,
                routing_key="incident.created",
            )

            def callback(ch, _method, _properties, body: bytes) -> None:
                payload = json.loads(body.decode("utf-8"))
                try:
                    on_message(payload)
                except Exception:
                    record_event_consumed("incident.created", "error")
                    raise
                else:
                    record_event_consumed("incident.created", "success")
                    ch.basic_ack(delivery_tag=_method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=settings.incident_queue_name, on_message_callback=callback)
            channel.start_consuming()
        except AMQPError:
            logger.exception("Incident consumer failed to start")

    thread = threading.Thread(target=consume, daemon=True, name="coordination-incident-consumer")
    thread.start()
