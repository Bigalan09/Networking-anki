# CIDR

## What does CIDR stand for?
**Classless Inter-Domain Routing** (pronounced "cider"). Introduced in 1993 (RFC 1519) to replace the rigid classful addressing system (A/B/C) and slow the exhaustion of IPv4 addresses.

## What is CIDR notation?
A compact way to express an IP address and its subnet mask together using a forward slash followed by the prefix length. Example: `192.168.1.0/24` means the first 24 bits are the network portion.

## What does /16 mean in CIDR notation?
The first **16 bits** of the address identify the network. The remaining 16 bits identify hosts. Equivalent to subnet mask `255.255.0.0`.

## What is a CIDR block?
A contiguous range of IP addresses defined by a starting address and a prefix length. Example: `10.0.0.0/8` represents all addresses from `10.0.0.0` to `10.255.255.255`.

## How many IP addresses are in a /32?
**1** address (2⁰ = 1). Used to represent a single host (e.g., a specific server or loopback).

## How many IP addresses are in a /31?
**2** addresses (2¹ = 2). RFC 3021 allows /31 for **point-to-point links** with no wasted network/broadcast addresses.

## How many IP addresses are in a /30?
**4** total (2² = 4): 1 network + 2 usable hosts + 1 broadcast.

## How many IP addresses are in a /24?
**256** total (2⁸ = 256): 254 usable hosts.

## How many IP addresses are in a /22?
**1024** total (2¹⁰ = 1024): 1022 usable hosts.

## How many IP addresses are in a /20?
**4096** total (2¹² = 4096): 4094 usable hosts.

## How many IP addresses are in a /16?
**65536** total (2¹⁶ = 65536): 65534 usable hosts.

## How many IP addresses are in a /8?
**16,777,216** total (2²⁴ = 16,777,216): 16,777,214 usable hosts.

## What is route aggregation (supernetting)?
Combining multiple smaller CIDR blocks into a single larger one to reduce routing table size. Example: `192.168.0.0/24` + `192.168.1.0/24` can be aggregated as `192.168.0.0/23`.

## What are the CIDR prefix lengths and their subnet masks?

| Prefix | Subnet Mask       | Hosts  |
|--------|-------------------|--------|
| /8     | 255.0.0.0         | 16,777,214 |
| /16    | 255.255.0.0       | 65,534 |
| /20    | 255.255.240.0     | 4,094  |
| /24    | 255.255.255.0     | 254    |
| /25    | 255.255.255.128   | 126    |
| /26    | 255.255.255.192   | 62     |
| /27    | 255.255.255.224   | 30     |
| /28    | 255.255.255.240   | 14     |
| /29    | 255.255.255.248   | 6      |
| /30    | 255.255.255.252   | 2      |

## What is the difference between classful and classless routing?
- **Classful**: Routing protocols (RIPv1, IGRP) do not carry subnet mask information; they assume the default class mask. Networks must be contiguous with no VLSM.
- **Classless**: Routing protocols (RIPv2, OSPF, BGP, EIGRP) include prefix length in routing updates, supporting VLSM and CIDR.

## How do you determine if two IP addresses are in the same CIDR block?
Perform a **bitwise AND** of each address with the subnet mask. If the results are equal, they are in the same subnet.

Example: Is `10.1.2.50` in `10.1.2.0/28`?
- Mask = `255.255.255.240`
- `10.1.2.50 AND 255.255.255.240` = `10.1.2.48` ≠ `10.1.2.0`
- **No** — 50 is in the .48 subnet, not the .0 subnet.

## What prefix length covers exactly two /25 subnets?
A **/24** — a /24 contains exactly two /25 subnets.

## What is the summary route for 172.16.0.0/24 through 172.16.3.0/24?
`172.16.0.0/22` — the four /24 networks share the first 22 bits.
