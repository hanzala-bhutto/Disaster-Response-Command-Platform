# Kafka Messaging Guide

## Why Kafka
Kafka is a distributed event log.

That means events are written to topics and stored durably for a configurable retention period instead of being treated as short-lived broker messages.

Kafka is a strong fit when the platform needs:
- durable event history
- replay of old events
- multiple independent consumers for the same event stream
- higher throughput event processing
- partition-based scaling
- tighter alignment with analytics and streaming patterns later

For this platform, Kafka is useful because the same `incident.created` event may later be consumed by:
- coordination logic
- notifications
- analytics
- audit pipelines
- future automation workflows

With Kafka, those consumers can each have their own consumer group and progress independently.

## How Kafka works in this platform

### Topics
The platform currently uses two topics:
- `incident.created`
- `task.created`

In Kubernetes, these topics are created explicitly by a bootstrap job instead of relying on broker auto-creation.

Current topic settings:
- partitions: `3`
- replication factor: `3`

A producer writes JSON payloads into a topic.

### Consumer groups
A consumer group tracks how far a service has read in a topic.

In this platform:
- the coordination service uses its own consumer group for `incident.created`
- the notification service uses its own consumer group for both topics

That means both services can read the same event stream without interfering with each other.

### Offsets
Kafka stores each record at an offset inside a partition.

A consumer commits offsets as it reads.

That is how Kafka knows what a consumer group has already processed.

### Retention
Kafka keeps events for a retention window.

That is different from a queue model where the message disappears after consumption.

Retention makes replay possible.

## When to use Kafka
Kafka is a good choice when:
- several services need the same event stream
- event replay matters
- throughput is expected to grow
- event history is useful for debugging or analytics
- you want partition-based scale-out later

Kafka is usually not the best first choice when:
- the system is very small
- you only need simple request/reaction workflows
- replay is not important
- operational simplicity is the top priority

## Why move from RabbitMQ here
RabbitMQ is excellent for queueing and routing, but Kafka is a better fit once the platform starts behaving like an event platform instead of a small background-job system.

The move makes sense here because the project already has:
- multiple services consuming operational events
- observability around event throughput
- AI and analytics use cases that benefit from durable streams
- Kubernetes deployment where a broker can be run as part of the platform stack

## Tradeoffs
Kafka brings benefits, but also more operational complexity.

Compared with RabbitMQ, Kafka usually means:
- more infrastructure tuning
- more focus on partitions and offsets
- more emphasis on ordering rules
- stronger scaling and replay capabilities

## Current implementation notes
The local Kubernetes stack runs Kafka in KRaft mode with three brokers.

That keeps the local deployment aligned with Kafka's distributed broker model while still avoiding ZooKeeper.

The base stack also provisions topics with a Kubernetes Job so the topic layout is deterministic.

A later production-style setup would typically add:
- multiple brokers
- explicit topic configuration
- replication factor greater than 1
- retention tuning
- stronger security and ACLs
