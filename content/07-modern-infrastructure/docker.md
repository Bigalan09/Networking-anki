# Docker Networking

## What is Docker networking?
Docker provides a **software-defined networking** layer for containers. Each container gets a virtual network interface (usually `eth0`) connected to a Docker network. Docker manages IP assignment, DNS, and routing between containers.

## What are the Docker network driver types?
- **bridge**: Default; containers connect to a virtual bridge (`docker0`); can communicate with each other and the host via NAT
- **host**: Container shares the host's network namespace (no isolation)
- **overlay**: Multi-host networking for Docker Swarm/Kubernetes
- **macvlan**: Assigns a MAC address from the host network, making the container appear as a physical device
- **ipvlan**: Like macvlan but shares MAC addresses; good for environments that limit MAC addresses
- **none**: No networking

## What is the default Docker bridge network?
The `bridge` network created automatically by Docker. All containers started without specifying a network connect to it. Default subnet is typically `172.17.0.0/16`. Containers on the default bridge cannot resolve each other by name.

## What is a user-defined bridge network?
A custom Docker network created with `docker network create`. Provides:
- **Automatic DNS**: Containers can reach each other by **container name**
- **Better isolation**: Only containers on the same network communicate
- **Configurable subnet/gateway**

```bash
docker network create --subnet=192.168.100.0/24 my-network
docker run --network my-network --name web nginx
docker run --network my-network --name app myapp
# 'app' can ping 'web' by name
```

## How does Docker DNS work in user-defined networks?
Docker runs a built-in DNS resolver at `127.0.0.11`. Containers in user-defined networks can resolve other containers by their **container name** or **service name** (in Docker Compose).

## What is Docker host networking?
`--network host` — the container shares the **host's network stack** directly. The container sees all the host's interfaces and ports. No network isolation. Not available on Docker Desktop (Mac/Windows).

## What is port mapping in Docker?
Publishing container ports to the host: `-p <host-port>:<container-port>`.
```bash
docker run -p 8080:80 nginx
# Host port 8080 → container port 80
```
Docker creates iptables rules to forward traffic from the host port to the container.

## What are Docker's built-in DNS addresses?
- **127.0.0.11**: Docker's embedded DNS resolver (inside containers on user-defined networks)
- The resolver forwards external queries to the host's configured DNS

## What is a Docker overlay network?
A **multi-host network** used in Docker Swarm that spans multiple Docker hosts using **VXLAN** encapsulation. Containers on different hosts can communicate as if on the same Layer 2 network.

## What is VXLAN and how does Docker use it?
**Virtual Extensible LAN** — a tunneling protocol that encapsulates Layer 2 frames in UDP packets (port 4789). Docker Swarm overlay networks use VXLAN to create virtual Layer 2 networks across multiple physical hosts.

## What is the difference between `docker0` and a container's `eth0`?
- **`docker0`**: A virtual bridge on the **host** that acts as the gateway for containers on the default bridge network
- **`eth0`** (in container): The container's virtual network interface connected to the bridge via a veth pair

## What is a veth pair in Docker?
A **virtual Ethernet pair** — two connected virtual interfaces. One end (`vethXXXX`) is visible on the host; the other (`eth0`) is inside the container. Traffic in one end comes out the other.

## How do you inspect Docker network configuration?
```bash
docker network ls                    # List networks
docker network inspect bridge        # Inspect a network
docker inspect <container> | grep -A20 Networks  # Container networking
```
