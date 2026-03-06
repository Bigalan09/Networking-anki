# Grafana

## What is Grafana?
Grafana is an **open-source analytics and visualization platform** for metrics, logs, and traces. It queries data from various sources (Prometheus, Loki, Elasticsearch, InfluxDB, etc.) and displays it in **dashboards**.

## What are Grafana's core components?
- **Dashboards**: Collections of panels
- **Panels**: Individual visualizations (graph, stat, table, heatmap, etc.)
- **Data sources**: Connections to data backends (Prometheus, Loki, etc.)
- **Alerts**: Notification rules based on metric thresholds
- **Variables**: Dynamic dashboard values (drop-down selectors)
- **Annotations**: Mark events on graphs (deploys, incidents)

## What data sources does Grafana support?
Built-in support includes:
- **Prometheus** (metrics)
- **Loki** (logs)
- **Tempo** (traces)
- **InfluxDB** (metrics)
- **Elasticsearch/OpenSearch** (logs/metrics)
- **MySQL, PostgreSQL** (direct DB queries)
- **CloudWatch** (AWS metrics)
- **Azure Monitor**
- **Jaeger, Zipkin** (traces)
- Many more via community plugins

## What is a Grafana dashboard?
A collection of **panels** arranged in a grid layout. Dashboards are stored as JSON and can be:
- Exported and imported
- Version-controlled in Git
- Shared via links (with or without authentication)
- Published to grafana.com dashboard library

## What is Grafana's alerting?
Grafana can evaluate **alert rules** against data sources and trigger notifications:
1. Define an alert rule (metric condition + threshold)
2. Configure a **contact point** (Slack, PagerDuty, email, etc.)
3. Create **notification policies** (route alerts to contact points)
4. Optionally use **silences** and **mutes**

## What is Grafana Loki?
A **log aggregation system** inspired by Prometheus. Unlike Elasticsearch, it only indexes **log labels** (not the full text), making it highly cost-effective. Query language: **LogQL**.

## What is LogQL?
Grafana Loki's **query language** for querying logs:
```logql
# Filter logs by labels
{job="nginx", env="prod"} |= "error"

# Rate of error logs
rate({job="nginx"} |= "error" [5m])

# Parse JSON logs
{job="api"} | json | duration > 1000ms
```

## How do you correlate metrics, logs, and traces in Grafana?
Grafana supports **Explore** mode with data source links:
- Click a metric spike → jump to logs for that time period
- Click a trace span → see the associated logs
- Configured via **data source correlations** in Grafana UI

## What is a Grafana variable?
A **dynamic value** that can be selected from a drop-down in a dashboard. Used to filter data:
```
Variable: $env
Values: dev, staging, prod
Used in query: http_requests_total{env="$env"}
```

## What is Grafana provisioning?
Configuring Grafana **via files** instead of the UI, enabling GitOps for dashboards and data sources:
```
/etc/grafana/provisioning/
├── datasources/prometheus.yaml
├── dashboards/default.yaml
└── alerting/rules.yaml
```

## What is Grafana Cloud?
Grafana's **managed SaaS platform** offering Grafana, Prometheus-compatible metrics (Mimir), Loki (logs), and Tempo (traces) as a hosted service. Free tier available.

## What are Grafana's main panel types?
- **Time series**: Line/bar chart for metrics over time
- **Stat**: Single value with optional thresholds
- **Gauge**: Visual gauge for current values
- **Bar chart**: Compare values across categories
- **Table**: Tabular data
- **Heatmap**: Distribution/density visualization
- **Logs**: Display log streams from Loki
- **Traces**: Flame graph for distributed traces

## What is the difference between Grafana and Prometheus?
- **Prometheus**: Collects, stores, and queries metrics; generates alerts
- **Grafana**: Visualizes metrics from various sources including Prometheus; does not collect data itself
They are **complementary**: Prometheus for data collection/storage, Grafana for visualization.
