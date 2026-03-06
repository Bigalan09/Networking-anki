# Service Identification

## What is ICMP and what is it used for?
**Internet Control Message Protocol** — a Layer 3 protocol used for:
- **ping**: Tests connectivity (ICMP Echo Request / Echo Reply)
- **traceroute**: Maps network path (ICMP Time Exceeded messages)
- **Error reporting**: Destination unreachable, TTL exceeded, etc.

## What does TTL (Time to Live) do?
TTL is a field in the IP header that **decrements by 1** at each router hop. When TTL reaches 0, the router discards the packet and sends an ICMP "Time Exceeded" message back to the sender. Prevents packets from looping forever.

## What is ARP and how does it work?
**Address Resolution Protocol** — resolves an IP address to a MAC address on the local network:
1. Host broadcasts: "Who has IP `x.x.x.x`? Tell `my-MAC`"
2. The host with that IP replies with its MAC address
3. The requesting host caches the IP→MAC mapping in its ARP table

## What is a gratuitous ARP?
An ARP response sent **without a request**, announcing a host's own IP-to-MAC mapping. Used for:
- Duplicate IP detection
- Updating ARP caches after failover (HSRP/VRRP)
- ARP spoofing attacks

## What is DHCP and how does the DORA process work?
**Dynamic Host Configuration Protocol** — automatically assigns IP addresses. Process:
1. **Discover**: Client broadcasts to find a DHCP server
2. **Offer**: Server offers an IP address
3. **Request**: Client requests the offered address
4. **Acknowledge**: Server confirms the lease

## What ports does DHCP use?
- UDP **port 67** (server)
- UDP **port 68** (client)

## What is SNMP used for?
**Simple Network Management Protocol** — used to **monitor and manage** network devices (routers, switches, servers). An NMS (Network Management System) polls devices for metrics. Versions: SNMPv1, SNMPv2c, SNMPv3 (secure, encrypted).

## What is NTP used for?
**Network Time Protocol** — synchronizes clocks across network devices. Uses **UDP port 123**. Critical for certificate validation, log correlation, and Kerberos authentication.

## What is BGP and what does it do?
**Border Gateway Protocol** — the routing protocol of the internet. An **exterior gateway protocol** (EGP) that exchanges routing information between autonomous systems (AS). Uses **TCP port 179**. Path-vector protocol that selects routes based on policies and attributes.

## What is OSPF?
**Open Shortest Path First** — an interior gateway protocol (IGP) that uses **Dijkstra's algorithm** to find the shortest path. Link-state protocol; each router has a complete map of the network topology. Uses IP protocol 89 (not TCP/UDP).

## What is the difference between TCP/80 and TCP/8080?
- **Port 80**: Standard HTTP port, requires root/admin to bind
- **Port 8080**: Common alternative HTTP port, used by development servers and proxies; no root required to bind

## What protocol uses IP protocol number 6?
**TCP** uses IP protocol number 6. (**UDP = 17**, **ICMP = 1**, **OSPF = 89**, **GRE = 47**, **ESP = 50**, **AH = 51**)

## What is GRE tunneling?
**Generic Routing Encapsulation** — IP protocol 47. Encapsulates one packet inside another, creating a virtual point-to-point link. Used in VPNs and to carry multicast/broadcast traffic over unicast-only networks.

## What is LLDP?
**Link Layer Discovery Protocol** — a Layer 2 protocol (IEEE 802.1AB) used by network devices to advertise their identity and capabilities to directly connected neighbors. Cisco's proprietary equivalent is **CDP** (Cisco Discovery Protocol).

## What is STP and why is it needed?
**Spanning Tree Protocol** — prevents **Layer 2 loops** in switched networks with redundant paths. Selects a root bridge and blocks redundant paths to create a loop-free tree topology.

## What is 802.1Q?
The IEEE standard for **VLAN tagging** in Ethernet frames. Adds a 4-byte tag (including 12-bit VLAN ID supporting VLANs 1–4094) between the source MAC and EtherType fields.
