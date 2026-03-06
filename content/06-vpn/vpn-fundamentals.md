# VPN Fundamentals

## What is a VPN?
A **Virtual Private Network** — a technology that creates a **secure, encrypted tunnel** over an untrusted network (like the internet), allowing private communication between endpoints as if they were on the same private network.

## What are the main use cases for VPNs?
- **Remote access**: Employees connect to corporate networks from home/travel
- **Site-to-site**: Connect branch offices to headquarters over the internet
- **Privacy**: Hide internet traffic from ISP/surveillance
- **Bypassing geo-restrictions**: Appear to be in a different geographic location
- **Securing public Wi-Fi**: Encrypt traffic on untrusted networks

## What are the main VPN protocols?
- **WireGuard**: Modern, fast, simple (kernel-level, ~4000 lines of code)
- **IPsec**: Industry-standard, complex, widely supported
- **OpenVPN**: Open-source, SSL/TLS-based, highly configurable
- **L2TP/IPsec**: Layer 2 Tunneling Protocol over IPsec
- **SSTP**: Microsoft's SSL-based VPN
- **IKEv2**: Fast, supports MOBIKE for mobile roaming

## What is a tunnel mode vs transport mode in IPsec?
- **Tunnel mode**: Encrypts the **entire original IP packet** (header + payload) and adds a new IP header. Used for site-to-site VPNs.
- **Transport mode**: Encrypts only the **payload** (data), leaving the original IP header intact. Used for host-to-host communication.

## What is IKE (Internet Key Exchange)?
The protocol used by IPsec to **negotiate security associations** (authenticate peers and establish encryption keys). IKEv2 is the current version — faster, more secure, supports MOBIKE for IP address changes.

## What is a Security Association (SA) in IPsec?
A **unidirectional agreement** on the cryptographic parameters (algorithm, keys, duration) for a VPN connection. IPsec requires two SAs per connection (one each direction), identified by an **SPI** (Security Parameter Index).

## What are ESP and AH in IPsec?
- **ESP** (Encapsulating Security Payload, protocol 50): Provides **encryption, integrity, and authentication**. The most commonly used.
- **AH** (Authentication Header, protocol 51): Provides **integrity and authentication only** — no encryption. Incompatible with NAT.

## What is a split tunnel VPN?
Only traffic destined for specified networks goes through the VPN tunnel; all other traffic goes directly to the internet. Reduces VPN load but exposes non-tunneled traffic.

## What is a full tunnel VPN?
**All traffic** from the client is routed through the VPN. Provides maximum privacy and security (ISP cannot see any traffic), but increases latency and VPN load.

## What is a site-to-site VPN?
A VPN that **permanently connects two networks** (e.g., head office and branch). Both network gateways maintain the VPN tunnel. Individual hosts don't need VPN software.

## What is a remote access VPN?
A VPN where individual **clients connect to a central VPN server** to access private resources. The client runs VPN software (WireGuard, OpenVPN, Cisco AnyConnect).

## What ports do common VPN protocols use?
- **WireGuard**: UDP 51820 (default, configurable)
- **OpenVPN**: UDP/TCP 1194 (default)
- **IPsec IKE**: UDP 500 and UDP 4500 (NAT-T)
- **L2TP**: UDP 1701
- **SSTP**: TCP 443
- **IKEv2**: UDP 500 and UDP 4500

## What is NAT traversal (NAT-T) in VPNs?
A method to **encapsulate IPsec traffic in UDP** (port 4500) to pass through NAT devices. Standard IPsec uses protocols (ESP, AH) that NAT cannot translate because they lack port numbers.

## What is a VPN concentrator?
A dedicated device (hardware or software) that **terminates many VPN connections** at a central point. Handles encryption/decryption at scale. Examples: Cisco ASA, Palo Alto, AWS VPN Gateway.
