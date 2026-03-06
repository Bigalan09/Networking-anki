# Subnet Routers and Exit Nodes

## What is a Tailscale subnet router?
A device in your tailnet configured to **advertise routes** for non-Tailscale subnets, making those subnets accessible to all other devices in the tailnet without installing Tailscale on every host.

## Why use a subnet router?
- Give Tailscale access to **IoT devices**, printers, or servers that can't run Tailscale
- Provide access to **entire on-prem or cloud subnets** through a single gateway
- Connect legacy devices and embedded systems to your tailnet

## How do you set up a subnet router?
```bash
# On the router device, enable IP forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Advertise the subnet
sudo tailscale up --advertise-routes=192.168.1.0/24,10.0.0.0/8

# Approve in admin console (Security review required)
# Or use --accept-routes on clients:
sudo tailscale up --accept-routes
```

## What does "approve routes" mean in Tailscale?
For security, advertised subnet routes must be **explicitly approved** by a tailnet admin in the Tailscale admin console. This prevents a compromised device from advertising arbitrary routes.

## What is an exit node in Tailscale?
A tailnet device configured to **route all internet traffic** from other devices through it. Effectively makes other devices appear to be at the exit node's location — similar to a traditional VPN.

## How do you set up a Tailscale exit node?
```bash
# On the exit node
sudo tailscale up --advertise-exit-node

# Enable IP forwarding (required)
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
sysctl -p

# Approve in admin console

# On the client device, use the exit node:
sudo tailscale up --exit-node=<exit-node-ip>
sudo tailscale up --exit-node=<exit-node-ip> --exit-node-allow-lan-access
```

## What is the difference between a subnet router and an exit node?

| Feature        | Subnet Router               | Exit Node                    |
|----------------|-----------------------------|------------------------------|
| Routes         | Specific subnets            | All traffic (0.0.0.0/0)      |
| Use case       | Access private networks     | Full traffic routing/privacy |
| Impact         | Partial traffic redirected  | All internet traffic through it |

## What is `--exit-node-allow-lan-access`?
A flag that allows a client using an exit node to still **access its local LAN** directly (e.g., local printer, home router) instead of routing all local traffic through the exit node.

## Can a device be both a subnet router and an exit node?
**Yes** — a single Tailscale device can advertise both subnet routes and act as an exit node simultaneously.

## What is a "failover" subnet router in Tailscale?
Tailscale supports **high availability subnet routers** where multiple devices advertise the same route. Tailscale automatically routes traffic to a healthy router if one fails. Enabled by advertise the same route from multiple devices.

## What are the firewall considerations for a subnet router?
The subnet router needs:
1. **IP forwarding enabled** (`net.ipv4.ip_forward=1`)
2. **Firewall rules** allowing forwarded traffic between the Tailscale interface and the LAN interface
3. Masquerading/NAT if the LAN devices don't have routes back to the Tailscale network
