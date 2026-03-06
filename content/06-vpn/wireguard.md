# WireGuard

## What is WireGuard?
WireGuard is a **modern, high-performance VPN protocol** designed to be simpler, faster, and more secure than IPsec or OpenVPN. It operates at the **kernel level** (integrated into Linux kernel 5.6+) and has approximately 4,000 lines of code (vs OpenVPN's 100,000+).

## What are WireGuard's key features?
- **Simplicity**: Minimal codebase, easy to audit
- **Performance**: Kernel-level implementation, ChaCha20 encryption
- **Cryptography**: Modern algorithms — ChaCha20, Poly1305, Curve25519, BLAKE2
- **Roaming**: Peers can change IPs; WireGuard reconnects automatically
- **Stateless**: No persistent connections; peers are identified by public key

## What cryptographic algorithms does WireGuard use?
- **ChaCha20** (encryption)
- **Poly1305** (message authentication, AEAD)
- **Curve25519** (key exchange, ECDH)
- **BLAKE2s** (hashing)
- **SipHash24** (hash table keys)
- **HKDF** (key derivation)

## What transport protocol and port does WireGuard use?
**UDP**, default port **51820** (configurable). WireGuard does not support TCP.

## What is WireGuard's authentication model?
Based on **asymmetric key pairs** (like SSH). Each peer has a **private key** and **public key**. Peers exchange public keys out-of-band and configure them in the WireGuard config. No certificates or CA infrastructure needed.

## What is a WireGuard interface configuration?
```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <private-key>

[Peer]
PublicKey = <peer-public-key>
AllowedIPs = 10.0.0.2/32
Endpoint = 203.0.113.50:51820
PersistentKeepalive = 25
```

## What does AllowedIPs mean in WireGuard?
A **combined routing and access control list**. Outbound: traffic destined for these IPs is sent through the tunnel to this peer. Inbound: only packets with a source IP matching these IPs are accepted from this peer.

## How do you generate a WireGuard key pair?
```bash
# Generate private key
wg genkey > private.key

# Derive public key from private key
wg pubkey < private.key > public.key

# One-liner
wg genkey | tee private.key | wg pubkey > public.key
```

## How do you bring up and manage WireGuard interfaces?
```bash
# Using wg-quick (recommended)
wg-quick up wg0        # Bring up interface from /etc/wireguard/wg0.conf
wg-quick down wg0      # Bring down interface

# Enable on boot (systemd)
systemctl enable --now wg-quick@wg0

# Show WireGuard status
wg show
```

## What is PersistentKeepalive in WireGuard?
A keepalive packet sent every N seconds to maintain the connection through NAT. Required when the WireGuard peer is **behind NAT** and needs to keep a mapping in the NAT table. Typically set to **25 seconds**.

## What is the difference between WireGuard and OpenVPN performance?
WireGuard is generally **significantly faster** than OpenVPN:
- Uses ChaCha20 (optimized for modern CPUs without AES-NI)
- Kernel-level implementation avoids user-space overhead
- Simpler handshake (1.5 RTT vs OpenVPN's TLS overhead)
- Benchmarks often show 3-4x throughput improvement

## Can WireGuard work through restrictive firewalls?
WireGuard uses **UDP only**, which some firewalls block. Workarounds:
- Use UDP port 53 or 443 (often allowed)
- Use a wrapper like **udp2raw** to tunnel over TCP/ICMP
- Consider **Tailscale** which handles NAT traversal automatically

## What Linux kernel version includes WireGuard natively?
**Linux kernel 5.6** (released March 2020). Prior to this, WireGuard required an out-of-tree kernel module or DKMS package.

## What is a pre-shared key (PSK) in WireGuard?
An **optional additional symmetric key** shared between two peers for extra security (post-quantum resistance). Added to the peer configuration with `PresharedKey`.

## How does WireGuard handle roaming (IP changes)?
When a WireGuard peer's IP changes, WireGuard **automatically updates** the endpoint address of the peer when it receives a valid authenticated packet from a new IP. No reconnection required.
