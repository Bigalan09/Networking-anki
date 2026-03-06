# Network and Broadcast Addresses

## What is the network address of a subnet?
The **first address** in a subnet, where all host bits are set to **0**. It identifies the subnet itself and **cannot be assigned to a host**.

Example: In `192.168.1.0/24`, the network address is `192.168.1.0`.

## What is the broadcast address of a subnet?
The **last address** in a subnet, where all host bits are set to **1**. Packets sent to this address are delivered to **all hosts** on the subnet. It **cannot be assigned to a host**.

Example: In `192.168.1.0/24`, the broadcast address is `192.168.1.255`.

## What is a directed broadcast?
A packet sent to the broadcast address of a specific remote subnet (e.g., `10.1.2.255` for `10.1.2.0/24`). Most routers block directed broadcasts by default to prevent smurf attacks.

## What is a limited broadcast?
The address `255.255.255.255`. Packets sent to this address are broadcast to all hosts on the **local network segment** and are **never forwarded** by routers.

## What is a broadcast domain?
A network segment in which a broadcast packet sent by any node reaches all other nodes. Routers separate broadcast domains; switches extend them.

## How does a router reduce broadcast traffic?
Routers do not forward broadcast packets between interfaces. Each router interface (and the subnet it connects to) is a separate broadcast domain.

## What is a collision domain?
A network segment where simultaneous data transmissions cause collisions (relevant in half-duplex, hub-based networks). Switches create a separate collision domain per port. Routers also separate collision domains.

## What is the difference between a broadcast domain and a collision domain?
- **Collision domain**: Layer 1/2 — segment where collisions can occur. Each switch port is its own collision domain.
- **Broadcast domain**: Layer 2/3 — segment where broadcasts are forwarded. Separated by routers (or VLANs).

## Given network 10.20.30.0/27, what is the broadcast address?
Block size = 32. Network = `10.20.30.0`, Broadcast = `10.20.30.31`.

## Given network 192.168.5.64/26, what are the usable host ranges?
- Network: `192.168.5.64`
- Broadcast: `192.168.5.127`
- Usable hosts: `192.168.5.65` – `192.168.5.126` (62 hosts)

## What happens when a device sends a packet to its subnet broadcast address?
The packet is delivered to all hosts in the subnet. Routers do not forward it beyond the subnet. Used for protocols like ARP and DHCP discovery.

## Does IPv6 have a broadcast address?
**No.** IPv6 eliminates broadcast entirely. Broadcast functionality is replaced by **multicast** (e.g., the all-nodes multicast address `ff02::1`) and **anycast**.

## What address does ARP use to discover a MAC address?
ARP sends a broadcast frame to `FF:FF:FF:FF:FF:FF` (Layer 2 broadcast) with the destination IP, asking "who has this IP?"

## What is the subnet address for host 172.16.45.200/20?
- /20 mask = `255.255.240.0`, block size in third octet = 16
- 45 ÷ 16 = 2 remainder 13 → block starts at 32
- Network: `172.16.32.0/20`
- Broadcast: `172.16.47.255`
