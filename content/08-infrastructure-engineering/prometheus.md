# Prometheus

## What is Prometheus?
Prometheus is an **open-source monitoring and alerting toolkit** (CNCF project) designed for reliability and scalability. It:
- Collects metrics via **HTTP scraping** (pull model)
- Stores time-series data in a local TSDB
- Provides **PromQL** query language
- Integrates with **Alertmanager** for alerts
- **Does not** handle log aggregation or distributed tracing

## What is a metric in Prometheus?
A **named time-series** with associated labels and numeric values:
- Name: `http_requests_total`
- Labels: `{method="GET", status="200", endpoint="/api"}`
- Value: `12453`
- Timestamp: `1704067200`

## What are the four Prometheus metric types?
1. **Counter**: Monotonically increasing value (requests, errors, bytes)
2. **Gauge**: Value that can go up or down (memory usage, active connections)
3. **Histogram**: Samples observations, counts in configurable buckets (request duration)
4. **Summary**: Similar to histogram, calculates quantiles on the client side

## What is PromQL?
**Prometheus Query Language** — a powerful, functional query language for querying metrics:
```promql
# HTTP request rate over 5 minutes
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Memory usage above 80%
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.8
```

## What is a Prometheus exporter?
A component that **exposes metrics** from a system or application in Prometheus format (text/plain):
- **node_exporter**: Linux host metrics (CPU, memory, disk, network)
- **blackbox_exporter**: External probes (HTTP, HTTPS, DNS, TCP)
- **postgres_exporter**: PostgreSQL metrics
- **redis_exporter**: Redis metrics
- **kube-state-metrics**: Kubernetes object state

## What is scraping in Prometheus?
Prometheus **periodically pulls (scrapes) metrics** from HTTP endpoints (default every 15 seconds). The target must expose a `/metrics` endpoint in the Prometheus text format.

## What is a scrape config?
The configuration telling Prometheus which targets to scrape:
```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets: ['10.0.0.1:9100', '10.0.0.2:9100']
    scrape_interval: 30s
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
```

## What is the Prometheus data model?
Metrics are stored as **time series** identified by metric name and a set of key-value **labels**:
```
metric_name{label1="value1", label2="value2"} value timestamp
```

## What is Alertmanager?
A component that **handles alerts** from Prometheus:
- Receives alerts from Prometheus
- **Deduplicates** similar alerts
- **Groups** related alerts
- **Routes** to notification channels (Slack, PagerDuty, email)
- **Silences** known maintenance windows
- **Inhibits** alerts when higher-priority alerts fire

## What is a recording rule?
A Prometheus rule that **pre-computes expensive PromQL expressions** and stores results as new time series:
```yaml
groups:
  - name: http_rates
    rules:
      - record: job:http_requests:rate5m
        expr: rate(http_requests_total[5m])
```
Improves dashboard performance for complex queries.

## What is `rate()` vs `irate()` in PromQL?
- `rate()`: Average per-second rate over the interval (smoothed, good for alerting)
- `irate()`: Instantaneous rate based on the last two data points (more responsive, good for graphing spikes)

## What is service discovery in Prometheus?
Dynamic target discovery instead of static configs:
- **Kubernetes**: Automatically discovers pods/services/nodes
- **EC2, GCE, Azure**: Cloud instance discovery
- **Consul, DNS**: Service mesh discovery

## What is the `up` metric?
A special metric Prometheus creates per scrape target. Value is `1` if the target was scraped successfully, `0` if it failed. Use `up == 0` alerts to detect exporter failures.

## What is remote_write in Prometheus?
Forwarding scraped metrics to **remote storage** backends (Thanos, Cortex, VictoriaMetrics, Grafana Cloud) for long-term retention and high availability:
```yaml
remote_write:
  - url: https://prometheus-remote.example.com/api/v1/write
```
