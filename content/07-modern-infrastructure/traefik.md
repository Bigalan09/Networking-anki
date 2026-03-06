# Traefik

## What is Traefik?
Traefik is a **modern, cloud-native reverse proxy and load balancer** designed for dynamic environments (Docker, Kubernetes, Consul). It automatically discovers services and generates routing configurations without manual updates.

## What are Traefik's core concepts?
- **Entrypoints**: Network ports Traefik listens on (e.g., port 80, 443)
- **Routers**: Match incoming requests and route to services (rules based on Host, Path, Headers)
- **Middlewares**: Transform requests/responses (auth, rate limiting, headers, redirects)
- **Services**: Load balancers for your actual backend servers
- **Providers**: Configuration sources (Docker, Kubernetes, file, etc.)

## What is a Traefik provider?
A **source from which Traefik discovers routes**:
- **Docker**: Reads container labels
- **Kubernetes**: Reads Ingress and IngressRoute resources
- **File**: Static YAML/TOML configuration files
- **Consul/etcd**: Service mesh/service discovery

## How does Traefik auto-discover Docker containers?
Traefik watches the Docker socket for container events. Containers expose themselves via **labels**:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.web.rule=Host(`example.com`)"
  - "traefik.http.routers.web.entrypoints=websecure"
  - "traefik.http.services.web.loadbalancer.server.port=3000"
```

## How does Traefik handle TLS/HTTPS?
Traefik integrates with **Let's Encrypt** (via ACME) to automatically obtain and renew TLS certificates:
```yaml
# traefik.yml
certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /acme.json
      httpChallenge:
        entryPoint: web
```

## What is the Traefik dashboard?
A built-in **web UI** (default: port 8080) showing active routers, services, and middlewares. Should be protected with authentication in production:
```yaml
api:
  dashboard: true
  insecure: false   # Require TLS + auth in production
```

## What are Traefik middlewares?
Components that **modify requests or responses** between the router and the service:
- `redirectScheme`: HTTP → HTTPS redirect
- `basicAuth` / `digestAuth`: HTTP authentication
- `rateLimit`: Request rate limiting
- `headers`: Add/modify HTTP headers
- `stripPrefix`: Remove path prefix
- `compress`: Gzip compression
- `forwardAuth`: Delegate auth to an external service

## What is a Traefik IngressRoute (CRD)?
A Kubernetes Custom Resource Definition specific to Traefik (vs standard Ingress). Provides access to all Traefik features (middlewares, TCP routing, etc.) not available in standard Ingress:
```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: web
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`example.com`)
      kind: Rule
      services:
        - name: web-service
          port: 80
  tls:
    certResolver: letsencrypt
```

## What is Traefik's `rule` syntax?
Router rules use a **DSL** to match requests:
- `Host(`example.com`)` — matches by hostname
- `Path(`/api`)` — matches exact path
- `PathPrefix(`/api`)` — matches path prefix
- `Method(`GET`)` — matches HTTP method
- `Headers(`X-Auth`, `token`)` — matches header value
- Combined: `Host(`example.com`) && PathPrefix(`/api`)`

## How does Traefik compare to Nginx as a reverse proxy?
| Feature              | Traefik           | Nginx             |
|----------------------|-------------------|-------------------|
| Dynamic config       | Auto-discovery    | Manual reload     |
| Let's Encrypt        | Built-in          | Certbot plugin    |
| Dashboard            | Built-in          | Third-party       |
| Kubernetes native    | Yes (CRDs)        | nginx-ingress     |
| Performance          | Good              | Excellent         |
| Learning curve       | Lower for cloud   | Higher initially  |

## What are Traefik access logs?
Traefik can log all HTTP requests to a file or stdout:
```yaml
accessLog:
  filePath: "/var/log/traefik/access.log"
  format: json
```
