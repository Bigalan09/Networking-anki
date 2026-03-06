# Monitoring and Logging

## What is the difference between monitoring and logging?
- **Monitoring**: Collecting and analyzing **metrics** (numeric measurements) over time to track system health and trigger alerts
- **Logging**: Recording **discrete events** as text/structured data for debugging, auditing, and analysis

## What are the key components of a monitoring stack?
1. **Data collection**: Agents or exporters gather metrics (node_exporter, Prometheus)
2. **Time-series database**: Stores metrics (Prometheus, InfluxDB, VictoriaMetrics)
3. **Visualization**: Dashboards (Grafana)
4. **Alerting**: Notification on threshold violations (Alertmanager, PagerDuty)

## What is a logging stack (ELK/EFK)?
**Elasticsearch, Logstash/Fluentd, Kibana**:
- **Elasticsearch**: Stores and indexes logs
- **Logstash/Fluentd**: Collects and transforms logs
- **Kibana**: Visualizes and searches logs

Modern alternative: **Grafana Loki** (lighter, label-based indexing)

## What are log levels and what do they mean?
| Level    | When to Use |
|----------|-------------|
| DEBUG    | Detailed developer info (disabled in production) |
| INFO     | Normal operational messages |
| WARN     | Potentially harmful situation, not an error |
| ERROR    | Error event, application can continue |
| FATAL/CRITICAL | Severe error, application may abort |

## What is log rotation?
The automatic management of log files — archiving old logs and creating new ones to prevent disk exhaustion. Configured with `logrotate` on Linux:
```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    missingok
    notifempty
    sharedscripts
    postrotate
        nginx -s reopen
    endscript
}
```

## What is centralized logging and why is it important?
Aggregating logs from all services/hosts to a **single location**. Benefits:
- Correlate events across systems
- Easier searching and analysis
- Retain logs even if a host is destroyed (ephemeral containers)
- Single security audit point

## What is the `journald` logging system?
**systemd-journald** — the system journal that collects log messages from all systemd services, kernel, and applications. Binary format with structured metadata.
```bash
journalctl -u nginx           # Logs for nginx service
journalctl -f                 # Follow (like tail -f)
journalctl --since "1 hour ago"
journalctl -p err             # Error level and above
```

## What is syslog?
A standard protocol (RFC 5424) for sending log messages over a network. Listens on **UDP/TCP port 514** (unencrypted) or **TCP port 6514** (TLS). Traditional Linux logging daemon (rsyslog, syslog-ng).

## What are key metrics to monitor for a web service?
- **Request rate** (requests/second)
- **Error rate** (5xx percentage)
- **Latency** (p50, p95, p99 response time)
- **Saturation** (active connections, queue depth)
- **Resource usage** (CPU, memory, disk I/O)
- **Availability** (uptime, health check results)

## What is an alert fatigue?
When too many low-quality alerts trigger, causing operators to **ignore or silence alerts**, including critical ones. Caused by poorly tuned thresholds, noisy alerts, and alerting on symptoms that don't require human action.

Prevention: Alert on **symptoms** (user impact), not causes; set appropriate thresholds; require runbooks.

## What is a runbook?
A documented set of procedures for responding to a specific alert or incident. Should include:
- What the alert means
- Common causes
- Diagnostic steps
- Remediation steps
- Escalation path

## What is blackbox monitoring?
Testing a service from the **outside** (like a user would), checking availability and response correctness:
- HTTP(S) probes (check response code, content)
- TCP connectivity probes
- DNS resolution checks

Tool: Prometheus **blackbox_exporter**
