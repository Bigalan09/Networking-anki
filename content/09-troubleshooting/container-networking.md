# Container Networking Troubleshooting

## Scenario: A Docker container cannot reach the internet. What do you check?
1. **DNS resolution**: `docker exec <container> nslookup google.com`
2. **Ping**: `docker exec <container> ping 8.8.8.8` (bypass DNS)
3. **IP forwarding on host**: `cat /proc/sys/net/ipv4/ip_forward` (must be 1)
4. **iptables**: `iptables -t nat -L POSTROUTING` — verify MASQUERADE rule exists for docker0
5. **Docker network**: `docker network inspect bridge` — check subnet, gateway
6. **Host internet**: Can the Docker host itself reach the internet?

## Scenario: Two Docker containers cannot communicate by name. What is the cause?
Docker's default `bridge` network does **not support DNS-based container name resolution**. You need a **user-defined bridge network**:
```bash
docker network create mynet
docker run --network mynet --name app myapp
docker run --network mynet --name db postgres
# Now 'app' can reach 'db' by name
```

## Scenario: A Kubernetes pod can't reach a Service by ClusterIP. What do you check?
1. **Service exists**: `kubectl get service my-service`
2. **Endpoints populated**: `kubectl get endpoints my-service` — must have pod IPs
3. **kube-proxy running**: `kubectl get pods -n kube-system | grep kube-proxy`
4. **iptables rules**: `iptables -t nat -L | grep my-service-cluster-ip`
5. **NetworkPolicy**: Is there a NetworkPolicy blocking the traffic?
6. **Pod labels**: Do the pod labels match the Service's selector?

## Scenario: Kubernetes pods can't resolve Service DNS names. What do you check?
1. **CoreDNS running**: `kubectl get pods -n kube-system -l k8s-app=kube-dns`
2. **Test DNS from pod**: `kubectl exec -it <pod> -- nslookup kubernetes.default`
3. **Check CoreDNS config**: `kubectl get configmap coredns -n kube-system -o yaml`
4. **DNS policy on pod**: Is `dnsPolicy` set correctly in pod spec? (default: `ClusterFirst`)
5. **ndots setting**: `/etc/resolv.conf` in the pod; high `ndots` causes slow resolution

## Scenario: A container can ping another container's IP but not its hostname. What is the issue?
DNS is not resolving. Either:
- Containers are on the **default bridge** (no built-in DNS)
- The container's `/etc/resolv.conf` doesn't point to the Docker DNS resolver (`127.0.0.11`)
- DNS server is unreachable

Check: `docker exec <container> cat /etc/resolv.conf`

## Scenario: A NodePort service is unreachable from outside the cluster. What do you check?
1. **Firewall**: Is the NodePort (30000-32767) open on the node's security group/firewall?
2. **kube-proxy**: Is it running on the node? (`kubectl get pods -n kube-system | grep kube-proxy`)
3. **Node accessibility**: Can you reach the node itself on any other port?
4. **Correct port**: `kubectl get service my-service` — verify the NodePort
5. **externalTrafficPolicy**: `Local` mode requires pods on the specific node you're hitting

## How do you debug network connectivity from inside a Kubernetes pod?
```bash
# Run a debug pod
kubectl run debug --image=nicolaka/netshoot --rm -it -- bash

# Inside the debug pod:
nslookup my-service.namespace.svc.cluster.local
curl http://my-service
ping 10.96.0.1   # ClusterIP
traceroute 10.0.0.5
```

## Scenario: Docker Compose services can't reach each other. What do you check?
1. **Same network**: All services in docker-compose.yml share a default network — they should be able to reach each other by service name
2. **Service name**: Use the service name (not container name) for DNS
3. **Port vs expose**: Ports don't need to be published (mapped to host) for inter-container communication; use `expose`
4. `docker-compose ps` — verify all containers are up
5. `docker network inspect <compose-project>_default` — check all containers are connected

## What is the Pod CIDR and why might it overlap with your network?
Kubernetes assigns Pod IPs from the **Pod CIDR** (e.g., `10.244.0.0/16`). If this overlaps with your LAN or corporate network, routing conflicts occur. Pods may be unreachable or traffic is sent to the wrong destination.

Fix: Configure a non-overlapping Pod CIDR when initializing the cluster.

## Scenario: Container traffic is being blocked by the host firewall (iptables/nftables). How do you diagnose?
```bash
# Check iptables rules affecting docker
iptables -L -n -v | grep DOCKER
iptables -t nat -L -n -v

# Check if FORWARD chain is blocking
iptables -L FORWARD -n -v

# Trace a specific packet (iptables-trace)
iptables -t raw -A PREROUTING -p icmp -j TRACE
dmesg | grep TRACE
```
