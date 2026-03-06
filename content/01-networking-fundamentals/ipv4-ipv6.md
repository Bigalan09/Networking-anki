# IPv4 and IPv6

## What is IPv4?
IPv4 (Internet Protocol version 4) is the fourth version of the Internet Protocol. It uses **32-bit addresses**, expressed as four decimal octets separated by dots (e.g., `192.168.1.1`). It supports approximately **4.3 billion** unique addresses.

## How many bits are in an IPv4 address?
**32 bits**, divided into 4 octets of 8 bits each (e.g., `10.0.0.1`).

## What are the IPv4 address classes?
- **Class A**: `0.0.0.0` – `127.255.255.255` (first bit: 0, default mask /8)
- **Class B**: `128.0.0.0` – `191.255.255.255` (first bits: 10, default mask /16)
- **Class C**: `192.0.0.0` – `223.255.255.255` (first bits: 110, default mask /24)
- **Class D**: `224.0.0.0` – `239.255.255.255` (multicast)
- **Class E**: `240.0.0.0` – `255.255.255.255` (reserved/experimental)

## What are the private IPv4 address ranges?
- **Class A private**: `10.0.0.0/8` (10.0.0.0 – 10.255.255.255)
- **Class B private**: `172.16.0.0/12` (172.16.0.0 – 172.31.255.255)
- **Class C private**: `192.168.0.0/16` (192.168.0.0 – 192.168.255.255)

These are defined in **RFC 1918** and are not routable on the public internet.

## What is the loopback address in IPv4?
`127.0.0.1` (the entire `127.0.0.0/8` range is loopback). Packets sent to this address never leave the host.

## What is the link-local address range in IPv4?
`169.254.0.0/16` (APIPA – Automatic Private IP Addressing). A device assigns itself an address in this range when it cannot obtain one via DHCP.

## What is IPv6?
IPv6 (Internet Protocol version 6) is the most recent version of the Internet Protocol. It uses **128-bit addresses**, expressed as eight groups of four hexadecimal digits separated by colons (e.g., `2001:0db8:85a3:0000:0000:8a2e:0370:7334`). It supports approximately **3.4 × 10³⁸** unique addresses.

## How many bits are in an IPv6 address?
**128 bits**, written as eight 16-bit groups in hexadecimal, separated by colons.

## What are the IPv6 address shortening rules?
1. **Leading zeros** in each group can be omitted: `0042` → `42`
2. **One consecutive group** of all-zero fields can be replaced by `::` (only once per address): `2001:db8:0:0:0:0:0:1` → `2001:db8::1`

## What is the IPv6 loopback address?
`::1` (equivalent to `127.0.0.1` in IPv4)

## What is the IPv6 link-local address prefix?
`fe80::/10` — automatically configured on every IPv6-enabled interface. Not routable beyond the local link.

## What are the main types of IPv6 addresses?
- **Unicast**: One-to-one communication (global unicast `2000::/3`, link-local `fe80::/10`, unique local `fc00::/7`)
- **Multicast**: One-to-many (`ff00::/8`)
- **Anycast**: One-to-nearest (same address assigned to multiple interfaces; routed to the nearest one)
- (Note: IPv6 has **no broadcast** — multicast replaces it)

## What replaced broadcast in IPv6?
**Multicast** replaced broadcast. IPv6 devices join multicast groups instead of receiving all-subnet broadcasts.

## What is a global unicast address in IPv6?
Addresses in the range `2000::/3` (starts with binary `001`). These are publicly routable IPv6 addresses equivalent to public IPv4 addresses.

## What is a unique local address (ULA) in IPv6?
Addresses in the range `fc00::/7` (typically `fd00::/8`). These are the IPv6 equivalent of RFC 1918 private addresses — not globally routable.

## What is EUI-64 in IPv6?
A method to auto-generate the 64-bit interface ID portion of an IPv6 address from a 48-bit MAC address by inserting `ff:fe` in the middle and flipping the 7th bit of the first byte.

## What is SLAAC in IPv6?
**Stateless Address Autoconfiguration** — a mechanism by which an IPv6 host automatically configures its own address using a network prefix (from Router Advertisements) combined with its interface identifier. No DHCP server required.

## How does IPv6 handle fragmentation differently from IPv4?
In IPv6, **only the source host** fragments packets (not intermediate routers). Routers drop oversized packets and send back an ICMPv6 "Packet Too Big" message. IPv6 uses **Path MTU Discovery** to find the correct MTU.

## What is the IPv6 transition mechanism "dual stack"?
**Dual stack** means a device runs both IPv4 and IPv6 simultaneously, using whichever is available/preferred for a given destination.

## What is 6to4 tunneling?
A transition mechanism that allows IPv6 packets to be transmitted over an IPv4 network by encapsulating them within IPv4 packets. Uses the `2002::/16` prefix.

## What is the well-known IPv6 documentation prefix?
`2001:db8::/32` — reserved for use in documentation and examples (RFC 3849). Should never appear in production routing tables.

## What does NDP stand for and what does it do in IPv6?
**Neighbor Discovery Protocol** — replaces ARP in IPv6. It handles address resolution (finding MAC addresses), router discovery, prefix discovery, and duplicate address detection (DAD).
