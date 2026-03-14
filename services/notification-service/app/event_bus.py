import json
import logging
import threading
from typing import Any, Callable

import pika
from pika.exceptions import AMQPError

from .metrics import record_event_consumed
from .settings_data import settings

logger = logging.getLogger(__name__)


def start_notification_consumer(on_message: Callable[[str, dict[str, Any]], None]) -> None:
    def consume() -> None:
        try:
            parameters = pika.URLParameters(settings.rabbitmq_url)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(exchange=settings.rabbitmq_exchange, exchange_type="topic", durable=True)
            channel.queue_declare(queue=settings.notification_queue_name, durable=True)
            channel.queue_bind(
                exchange=settings.rabbitmq_exchange,
                queue=settings.notification_queue_name,
                routing_key="incident.*",
            )
            channel.queue_bind(
                exchange=settings.rabbitmq_exchange,
                queue=settings.notification_queue_name,
                routing_key="task.*",
            )

            def callback(ch, method, _properties, body: bytes) -> None:
                payload = json.loads(body.decode("utf-8"))
                try:
                    on_message(method.routing_key, payload)
                except Exception:
                    record_event_consumed(method.routing_key, "error")
                    raise
                else:
                    record_event_consumed(method.routing_key, "success")
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=settings.notification_queue_name, on_message_callback=callback)
            channel.start_consuming()
        except AMQPError:
            logger.exception("Notification consumer failed to start")

    thread = threading.Thread(target=consume, daemon=True, name="notification-consumer")
    thread.start()
