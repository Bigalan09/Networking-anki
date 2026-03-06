# UDP — User Datagram Protocol

## What is UDP?
**User Datagram Protocol** — a connectionless, unreliable transport-layer protocol (Layer 4). It sends data without establishing a connection, with no guarantee of delivery, ordering, or duplicate protection.

## What are the key characteristics of UDP?
- **Connectionless**: No handshake; data is sent immediately
- **Unreliable**: No acknowledgments or retransmission
- **Unordered**: Packets may arrive out of order
- **Low overhead**: Smaller header (8 bytes vs TCP's 20+ bytes)
- **Fast**: No connection setup latency
- **No flow or congestion control**

## When should UDP be used instead of TCP?
- When **speed matters more than reliability** (gaming, video streaming, VoIP)
- When the application handles retransmission itself
- When data is time-sensitive and stale retransmissions are worse than loss
- For **DNS lookups**, **DHCP**, **SNMP**, **TFTP**, **NTP**
- For **multicast/broadcast** traffic

## What is the UDP header structure?
8 bytes total:
- **Source Port** (2 bytes)
- **Destination Port** (2 bytes)
- **Length** (2 bytes) — including header and data
- **Checksum** (2 bytes) — optional in IPv4, mandatory in IPv6

## What protocols use UDP?
- **DNS**: Port 53 (also uses TCP for zone transfers/large responses)
- **DHCP**: Ports 67 (server) / 68 (client)
- **SNMP**: Port 161/162
- **TFTP**: Port 69
- **NTP**: Port 123
- **QUIC/HTTP3**: Based on UDP
- **VoIP (RTP)**: Typically UDP
- **Gaming protocols**: Often UDP

## What is QUIC?
**Quick UDP Internet Connections** — a transport protocol built on top of UDP, developed by Google. Used as the foundation for **HTTP/3**. It provides:
- Multiplexed streams without head-of-line blocking
- Built-in TLS 1.3 encryption
- Connection migration (survives IP changes)
- 0-RTT connection resumption

## What port does DNS use and when does it switch between UDP and TCP?
DNS uses **UDP port 53** for standard queries (response ≤ 512 bytes). Switches to **TCP port 53** for:
- Responses larger than 512 bytes (or 4096 bytes with EDNS0)
- Zone transfers (AXFR/IXFR)
- DNSSEC responses

## How does UDP handle packet loss?
It doesn't — that responsibility lies with the **application layer**. Applications that use UDP must implement their own error handling if needed (e.g., application-level ACKs, sequence numbers).

## Compare TCP vs UDP:

| Feature        | TCP              | UDP             |
|----------------|------------------|-----------------|
| Connection     | Required         | Not required    |
| Reliability    | Guaranteed       | Best-effort     |
| Ordering       | Guaranteed       | Not guaranteed  |
| Speed          | Slower (overhead)| Faster          |
| Header size    | 20–60 bytes      | 8 bytes         |
| Use cases      | HTTP, SSH, FTP   | DNS, VoIP, gaming |

## What is UDP flooding?
A DoS attack that overwhelms a target with large amounts of UDP packets, exhausting network bandwidth and/or server processing capacity.
