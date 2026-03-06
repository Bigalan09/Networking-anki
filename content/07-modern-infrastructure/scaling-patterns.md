# Scaling Patterns

## What is horizontal scaling (scale out)?
Adding **more instances** of a service to handle increased load. Each instance is identical. Works well for stateless services. Examples: adding more web servers, more API pods.

## What is vertical scaling (scale up)?
Increasing the **resources (CPU, RAM, disk) of an existing instance**. Has physical/cost limits. Simpler but creates a single point of failure. Examples: larger VM, more RAM on a database server.

## What is a stateless application?
An application that **does not store session state** on the instance itself. Any request can be served by any instance. Enables easy horizontal scaling. State stored externally (database, cache, object store).

## What is a stateful application?
An application where **state is tied to a specific instance** (e.g., sessions in memory, local files). Harder to scale horizontally. Requires session affinity, shared storage, or externalization of state.

## What is session affinity (sticky sessions)?
A load balancer feature that routes **all requests from the same client to the same backend**. Needed for stateful apps. Implemented via cookies or IP hash. Reduces scalability benefits.

## What is a CDN and how does it improve scaling?
**Content Delivery Network** — a distributed network of edge servers that **cache static content** close to users. Reduces load on origin servers and improves response times globally. Examples: Cloudflare, AWS CloudFront, Fastly.

## What is caching in the context of scaling?
Storing **frequently accessed data in a fast-access layer** (e.g., Redis, Memcached) instead of querying the database every time. Dramatically reduces database load. Cache invalidation is the key challenge.

## What is a message queue and how does it help scaling?
A **buffer between producers and consumers** (e.g., RabbitMQ, Kafka, SQS). Decouples services, allows async processing, and prevents backend overload during traffic spikes. Consumers scale independently.

## What is auto-scaling?
Automatically **adjusting the number of instances** based on metrics (CPU, memory, request rate, queue depth). Cloud providers (AWS, GCP, Azure) offer auto-scaling groups/policies.

## What is the difference between active-active and active-passive?
- **Active-active**: Multiple instances **all serve traffic** simultaneously. Better throughput and resilience.
- **Active-passive**: One instance serves traffic; others are **standby**. Faster failover but resources idle during normal operation.

## What is database read scaling?
Adding **read replicas** to distribute database read traffic. Write traffic still goes to the primary. Common with PostgreSQL, MySQL streaming replication.

## What is database sharding?
**Partitioning data across multiple database instances** based on a shard key (e.g., user ID % N). Each shard holds a subset of data. Allows horizontal scaling of writes. Adds complexity (cross-shard queries).

## What is a circuit breaker pattern?
A resilience pattern that **stops calling a failing service** after a threshold of failures, giving it time to recover. States: **Closed** (normal), **Open** (failing, reject calls), **Half-open** (test with limited calls).

## What is rate limiting?
Controlling the **number of requests a client can make** in a time period. Protects backends from overload and abuse. Implemented at API gateway, reverse proxy, or application layer.

## What is the difference between concurrency and parallelism in scaling?
- **Concurrency**: Multiple tasks **in progress** at the same time (may share CPU via context switching)
- **Parallelism**: Multiple tasks **executing simultaneously** on multiple CPU cores
