# Kubernetes Networking

## What are the four fundamental Kubernetes networking requirements?
1. Every **Pod** gets its own unique IP address
2. All **Pods** can communicate with all other Pods without NAT
3. All **Nodes** can communicate with all Pods without NAT
4. The IP a Pod sees for itself is the same IP others use to reach it

## What is a Kubernetes Pod network?
A flat Layer 3 network where **every Pod gets a unique IP** from a cluster-wide CIDR. Pods communicate directly without NAT. Implemented by a **CNI plugin**.

## What is a CNI plugin?
**Container Network Interface** — a standard interface for container networking. Kubernetes delegates Pod networking to CNI plugins:
- **Flannel**: Simple VXLAN overlay, easy to set up
- **Calico**: BGP-based, supports NetworkPolicy, high performance
- **Cilium**: eBPF-based, L7 policies, observability
- **Weave**: Mesh overlay, encryption
- **Canal**: Flannel + Calico NetworkPolicy

## What is a Kubernetes Service?
A stable **virtual IP (ClusterIP)** and DNS name that load-balances traffic to a set of Pods. Even as Pods come and go, the Service IP remains constant.

Service types:
- **ClusterIP**: Internal only (default)
- **NodePort**: Exposed on every node's IP at a static port
- **LoadBalancer**: Provisions a cloud load balancer
- **ExternalName**: DNS CNAME to an external name

## What is a ClusterIP?
The default Service type — a **virtual IP accessible only within the cluster**. `kube-proxy` uses iptables/ipvs to route traffic to backend Pods.

## What is kube-proxy?
A **network proxy** running on each node that maintains iptables (or IPVS) rules to implement Services. Forwards traffic from Service ClusterIPs to the actual Pod IPs.

## What is a NodePort service?
Exposes a Service on a **static port (30000–32767) on every node's IP**. Traffic to `<NodeIP>:<NodePort>` is forwarded to the Service's backend Pods.

## What is a LoadBalancer service?
Provisions an **external load balancer** (cloud provider's LB) that forwards traffic to NodePort → Pods. Gives the Service an external IP.

## What is a Kubernetes Ingress?
An API object that manages **external HTTP/HTTPS access** to Services. An **Ingress Controller** (e.g., nginx-ingress, Traefik) reads Ingress objects and configures routing rules.

## What is a NetworkPolicy?
A Kubernetes resource that controls **which Pods can communicate with each other** (and with external endpoints). Acts as a Pod-level firewall. Requires a CNI plugin that supports NetworkPolicy (Calico, Cilium, etc.).

## What is the DNS name format for Kubernetes Services?
`<service-name>.<namespace>.svc.cluster.local`

Example: `my-api.production.svc.cluster.local`

## What is CoreDNS in Kubernetes?
The default **DNS server for Kubernetes clusters** (replaced kube-dns). Runs as a Deployment in the `kube-system` namespace. Resolves `cluster.local` names to Service/Pod IPs.

## What is a headless Service?
A Service with `clusterIP: None`. Instead of a ClusterIP, DNS returns the **individual Pod IPs** directly. Used for StatefulSets where clients need to connect to specific Pods (e.g., databases).

## What is the Pod CIDR and Service CIDR?
- **Pod CIDR**: The IP range from which Pod IPs are allocated (e.g., `10.244.0.0/16`)
- **Service CIDR**: The IP range for ClusterIPs (e.g., `10.96.0.0/12`)
- These must not overlap with each other or the node network

## What does `kubectl get endpoints` show?
The actual **Pod IP:port pairs** behind each Service. Useful for debugging when a Service doesn't respond — check if endpoints are populated.
