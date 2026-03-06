# Gateways

## What is a default gateway?
The default gateway is the IP address of the **router interface** on the local subnet that a host uses to send traffic destined for **any network it doesn't know a specific route to**. It is the "exit point" from the local subnet.

## Why does a host need a default gateway?
Hosts can communicate directly with other devices on the **same subnet** without a gateway. For destinations on **different subnets or the internet**, the host forwards the packet to its default gateway, which routes it onward.

## What happens if a host has no default gateway configured?
The host can only communicate with devices on its **own subnet**. Any attempt to reach a different subnet or the internet will fail.

## How does a host determine if the destination is on the local subnet or remote?
The host performs a **bitwise AND** of the destination IP and its own subnet mask. If the result equals the host's own network address, the destination is local. Otherwise, it is remote and the packet is sent to the default gateway.

## What is a gateway of last resort?
Another term for the **default route** (0.0.0.0/0) on a router. When no more specific route matches a destination, packets are forwarded to this gateway.

## What is the difference between a gateway and a router?
- **Router**: A Layer 3 device that forwards packets between networks based on routing tables.
- **Gateway**: The term for the router (or interface) that a specific host uses as its exit point. All routers can act as gateways, but a "gateway" specifically refers to the next-hop router from a host's perspective.

## What is a proxy ARP?
A technique where a router responds to ARP requests on behalf of a host on a different subnet. The router sends its own MAC address in response, causing the requesting host to send traffic to the router. This allows communication without requiring a configured default gateway (though it's generally not recommended).

## What is a multi-homed host?
A host with **multiple network interfaces** connected to different subnets. It may have multiple gateways or use routing to direct traffic out the appropriate interface.

## What is FHRP (First Hop Redundancy Protocol)?
Protocols that provide **default gateway redundancy** so that if the primary gateway fails, traffic automatically fails over to a backup. Examples:
- **HSRP** (Hot Standby Router Protocol) — Cisco proprietary
- **VRRP** (Virtual Router Redundancy Protocol) — open standard
- **GLBP** (Gateway Load Balancing Protocol) — Cisco proprietary, supports load balancing

## How does HSRP work?
Multiple routers share a **virtual IP and MAC address**. One router is the **active** router; others are **standby**. Hosts point their default gateway to the virtual IP. If the active router fails, a standby router takes over within seconds.

## What is the default gateway for a host at 192.168.10.50/24 if the router's interface is 192.168.10.1?
The default gateway is `192.168.10.1`.

## What is an application gateway?
A **Layer 7** device (like a firewall or proxy) that acts as an intermediary for specific application protocols (HTTP, FTP, SMTP). It understands application-layer data, unlike a standard network gateway which operates at Layer 3.

## What is NAT and how does it relate to gateways?
**Network Address Translation (NAT)** translates private IP addresses to public ones (and vice versa). The gateway/router typically performs NAT, allowing many hosts with private addresses to share a single public IP address for internet access.
