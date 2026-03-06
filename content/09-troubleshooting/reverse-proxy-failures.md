# Reverse Proxy Troubleshooting

## Scenario: Nginx returns 502 Bad Gateway. What does this mean and how do you fix it?
**502 Bad Gateway** means Nginx received an **invalid response from the upstream backend** (or couldn't connect).

Causes:
1. **Backend is down**: Is the application running? (`systemctl status myapp`, `docker ps`)
2. **Wrong upstream address**: Check `proxy_pass` URL — correct IP/port?
3. **Backend not listening**: `ss -tlnp | grep <port>`
4. **Firewall blocking**: Is the backend port accessible from Nginx?
5. **Backend crashing**: Check application logs

## Scenario: Nginx returns 504 Gateway Timeout. What does this mean?
The backend server is up but **didn't respond within the timeout period**.

Causes:
- Backend processing a slow request (database query, external API)
- Backend is overloaded
- Network congestion

Fix: Increase timeout settings or optimize the backend:
```nginx
proxy_read_timeout 120s;
proxy_connect_timeout 10s;
proxy_send_timeout 60s;
```

## Scenario: The backend application receives `127.0.0.1` as the client IP instead of the real client IP. What is the fix?
The reverse proxy must send the original client IP in a header:
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

The application must then read from `X-Real-IP` or `X-Forwarded-For` instead of the socket's remote address.

## Scenario: HTTPS works at the reverse proxy but the application redirects to HTTP. What is the fix?
The app doesn't know the original request was HTTPS. Pass the proto header:
```nginx
proxy_set_header X-Forwarded-Proto $scheme;
```
The app should trust this header and use it for generating URLs and redirects.

## Scenario: Traefik shows a router but the service is not reachable. What do you check?
1. `docker inspect <container>` — verify the `traefik.enable=true` label
2. Check Traefik dashboard (port 8080) — is the router and service listed as healthy?
3. `docker logs traefik` — look for configuration errors
4. Verify the `Host` rule matches the incoming request exactly
5. Check that the container port matches the `loadbalancer.server.port` label
6. Verify the container and Traefik are on the same Docker network

## Scenario: Let's Encrypt TLS certificates are not being issued by Traefik. What do you check?
1. Is port 80 open and accessible from the internet (HTTP challenge)?
2. Does the domain point to the server's public IP? (`dig example.com`)
3. Check Traefik logs: `docker logs traefik | grep -i acme`
4. Verify `acme.json` has correct permissions: `chmod 600 acme.json`
5. Check rate limits (5 certs per domain per week from Let's Encrypt)
6. Use staging CA for testing: `caServer: https://acme-staging-v02.api.letsencrypt.org/directory`

## Scenario: WebSocket connections fail through Nginx. What do you add?
WebSockets require specific proxy headers:
```nginx
location /ws {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
}
```

## Scenario: Large file uploads fail at the reverse proxy with 413 error. What is the fix?
Nginx's default max body size is 1MB. For file uploads:
```nginx
client_max_body_size 100m;
```

## Scenario: Reverse proxy works for most requests but /api returns 404. What might be wrong?
The `/api` path may be getting stripped or modified by the proxy. Check:
1. **Path rewriting**: Is Nginx stripping the prefix? (`rewrite` or `proxy_pass` with trailing slash)
2. Traefik: Is `stripPrefix` middleware applied?
```nginx
# This strips /api from the path:
location /api/ {
    proxy_pass http://backend/;  # trailing slash removes /api/
}
# This preserves /api:
location /api/ {
    proxy_pass http://backend;   # no trailing slash
}
```

## How do you test reverse proxy configuration without downtime?
```bash
# Nginx
nginx -t              # Test configuration syntax
nginx -s reload       # Graceful reload (no dropped connections)

# Traefik
# Traefik reloads automatically on config file change
# Check the dashboard for errors
```
