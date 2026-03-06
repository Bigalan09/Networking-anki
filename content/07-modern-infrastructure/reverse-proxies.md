# Reverse Proxies

## What is a reverse proxy?
A server that sits in front of web servers and **forwards client requests to the appropriate backend server**. The client communicates with the reverse proxy, not directly with backend servers.

## What is the difference between a forward proxy and a reverse proxy?
- **Forward proxy**: Sits in front of **clients**, forwards their requests to the internet (hides clients, used for filtering/caching/anonymity)
- **Reverse proxy**: Sits in front of **servers**, receives client requests and routes them to backends (hides servers, used for load balancing/TLS/caching)

## What are the main use cases for a reverse proxy?
- **Load balancing**: Distribute traffic across multiple backend servers
- **TLS termination**: Handle SSL/TLS encryption/decryption centrally
- **Caching**: Cache static content to reduce backend load
- **Compression**: Compress responses (gzip/brotli)
- **Authentication**: Centralize auth (OAuth, basic auth)
- **Rate limiting**: Throttle requests
- **Security**: Hide backend topology, WAF functionality
- **Virtual hosting**: Route multiple domains to different backends

## What is TLS termination at a reverse proxy?
The reverse proxy handles the **TLS handshake and encryption/decryption**. Backend servers receive **plain HTTP** traffic (or optionally re-encrypted HTTPS). Simplifies certificate management and offloads crypto from backends.

## What is TLS passthrough?
The reverse proxy **forwards encrypted TLS traffic** to the backend without decrypting it. The backend handles TLS. Used when the backend must see the original TLS connection (e.g., for mutual TLS).

## What HTTP headers does a reverse proxy add for backend visibility?
- **`X-Forwarded-For`**: Original client IP
- **`X-Forwarded-Proto`**: Original protocol (http/https)
- **`X-Forwarded-Host`**: Original Host header
- **`X-Real-IP`**: Client's real IP
- Modern standard: **`Forwarded`** header (RFC 7239)

## What is an upstream in reverse proxy terminology?
The **backend server(s)** that the reverse proxy forwards requests to. In Nginx, upstreams are defined in an `upstream` block; in Traefik, they are called **services**.

## What is health checking in a reverse proxy?
The reverse proxy **periodically tests backend servers** to verify they are healthy. Unhealthy backends are removed from the rotation until they recover. Types:
- **Passive**: Based on actual request failures
- **Active**: Explicit health check requests (e.g., HTTP GET `/healthz`)

## What is connection draining?
When removing a backend from rotation, **allowing in-flight requests to complete** before the backend is shut down. Prevents abruptly terminating active user sessions.

## What is a reverse proxy vs a load balancer?
These often overlap. Technically:
- **Reverse proxy**: Focuses on proxying requests, SSL, caching, routing
- **Load balancer**: Focuses on distributing traffic across backends
Modern reverse proxies (Nginx, Traefik, HAProxy) perform both functions.

## What load balancing algorithms do reverse proxies support?
- **Round Robin**: Requests distributed sequentially
- **Least Connections**: Route to server with fewest active connections
- **IP Hash**: Route based on client IP hash (session persistence)
- **Weighted Round Robin**: Servers get different traffic percentages
- **Random**: Random server selection
- **Consistent Hash**: Distribute based on a hash of request attributes

## What is a reverse proxy vs API gateway?
- **Reverse proxy**: General-purpose HTTP/TCP proxying
- **API gateway**: A specialized reverse proxy for APIs with additional features: authentication, rate limiting, request transformation, API key management, analytics
