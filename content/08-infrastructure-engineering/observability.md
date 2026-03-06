# Observability

## What is observability?
The ability to understand the **internal state of a system** from its external outputs. A system is observable if you can determine what is happening inside it based on the data it produces.

## What are the three pillars of observability?
1. **Metrics**: Numerical measurements over time (CPU usage, request rate, error rate)
2. **Logs**: Timestamped records of discrete events
3. **Traces**: End-to-end records of requests as they traverse distributed systems

## What is the difference between monitoring and observability?
- **Monitoring**: Alerting on **known failures** based on predefined metrics/thresholds. Answers "is X working?"
- **Observability**: Understanding **unknown failures** by exploring system data. Answers "why is X broken?"

## What are the four golden signals of monitoring (Google SRE)?
1. **Latency**: Time to service a request
2. **Traffic**: Demand on the system (requests/second)
3. **Errors**: Rate of failed requests
4. **Saturation**: How full the service is (CPU, queue depth, connections)

## What is the USE method?
A methodology for **resource analysis** (Brendan Gregg):
- **Utilization**: Average time the resource is busy
- **Saturation**: Extra work the resource can't service (queue)
- **Errors**: Error events

Apply to every resource: CPUs, memory, disks, network interfaces.

## What is the RED method?
A methodology for **service analysis**:
- **Rate**: Requests per second
- **Errors**: Failed requests per second
- **Duration**: Distribution of response times (latency)

## What is distributed tracing?
A technique to **follow a request through multiple services** in a distributed system, recording timing and metadata at each hop. Enables root-cause analysis of latency and failures.

Tools: Jaeger, Zipkin, AWS X-Ray, Honeycomb, Datadog APM

## What is a trace span?
The **basic unit of distributed tracing** — represents a single operation within a trace. Contains:
- Operation name
- Start time and duration
- Trace ID and Span ID
- Parent Span ID (for nesting)
- Tags and logs

## What is OpenTelemetry?
An **open-source observability framework** (CNCF project) that provides:
- Standardized APIs and SDKs for metrics, logs, and traces
- Vendor-neutral instrumentation
- Exporters to various backends (Prometheus, Jaeger, Datadog, etc.)

## What is cardinality in observability?
The **number of unique values** a label/dimension can take. High cardinality (e.g., unique user IDs as labels) causes memory and performance issues in metrics systems. Low-cardinality labels (environment, region, service) are recommended.

## What is structured logging?
Logging in a **machine-readable format** (JSON) instead of plain text. Enables searching, filtering, and aggregation by specific fields:
```json
{"level": "error", "timestamp": "2024-01-01T12:00:00Z", "service": "api", "user_id": "12345", "message": "database timeout", "duration_ms": 5000}
```

## What is an SLI (Service Level Indicator)?
A **quantitative measure of service behavior** — a metric that indicates the health of a service:
- Availability (% of requests that succeed)
- Latency (% of requests under 200ms)
- Error rate (% of requests returning 5xx)

## What is an SLO (Service Level Objective)?
A **target value for an SLI** that represents the desired service reliability:
- "99.9% of requests succeed" (three nines availability)
- "95% of requests complete in < 200ms"

## What is an SLA (Service Level Agreement)?
A **contractual commitment** between a service provider and customer about expected service levels. Typically includes financial penalties for missing SLOs. SLAs are usually weaker than internal SLOs.

## What is an error budget?
The **allowed amount of unreliability** derived from an SLO:
- 99.9% availability SLO = 0.1% error budget = ~43.8 minutes/month
- If budget is exhausted, new features pause; reliability work takes priority
