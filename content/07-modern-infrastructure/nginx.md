# Nginx

## What is Nginx?
Nginx (pronounced "engine-x") is a high-performance **web server, reverse proxy, load balancer, and HTTP cache**. Known for its event-driven, non-blocking architecture that handles thousands of concurrent connections efficiently.

## What is the Nginx configuration structure?
```
/etc/nginx/
├── nginx.conf          # Main config
├── conf.d/             # Additional configs (included from nginx.conf)
└── sites-enabled/      # Symlinks to sites-available/ (Debian/Ubuntu)
```

Main config context hierarchy: `main` → `events` → `http` → `server` → `location`

## What is an Nginx server block?
The equivalent of an Apache VirtualHost — defines how Nginx handles requests for a particular domain:
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/html;
    index index.html;
}
```

## How do you configure Nginx as a reverse proxy?
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## How do you configure HTTPS/TLS in Nginx?
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    location / {
        proxy_pass http://backend;
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## How do you configure Nginx load balancing?
```nginx
upstream backend {
    least_conn;            # Algorithm: round_robin (default), least_conn, ip_hash
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

## What is an Nginx location block and how does matching work?
Location blocks match URI patterns. Priority order:
1. `=` exact match (highest priority)
2. `^~` prefix match (no regex)
3. `~` case-sensitive regex
4. `~*` case-insensitive regex
5. `/` prefix match (catch-all, lowest priority)

## What are important Nginx performance directives?
```nginx
worker_processes auto;        # Match CPU cores
worker_connections 1024;      # Connections per worker
keepalive_timeout 65;         # Keep connections alive
gzip on;                      # Enable compression
gzip_types text/plain application/json;
client_max_body_size 10m;     # Max upload size
```

## How do you reload Nginx configuration without downtime?
```bash
nginx -t           # Test config syntax
nginx -s reload    # Graceful reload
# or
systemctl reload nginx
```

## What is the Nginx access log format?
Default combined log format:
```
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
```

## What is `proxy_buffering` in Nginx?
When enabled (default), Nginx **buffers the backend response** in memory/disk before sending to the client. Reduces backend connection hold time. Disable for streaming or Server-Sent Events:
```nginx
proxy_buffering off;
```

## What is the difference between Nginx open source and Nginx Plus?
- **Nginx open source**: Free, community-supported
- **Nginx Plus**: Commercial version with active health checks, JWT authentication, advanced monitoring dashboard, dynamic reconfiguration API, session persistence

## How do you serve a static website with Nginx?
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```
