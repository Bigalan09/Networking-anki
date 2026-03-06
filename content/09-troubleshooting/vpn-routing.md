# VPN Routing Troubleshooting

## Scenario: WireGuard tunnel is up but traffic isn't flowing. What do you check?
1. **AllowedIPs**: Are the destination IPs in the peer's `AllowedIPs`?
2. **IP forwarding**: `cat /proc/sys/net/ipv4/ip_forward` — must be 1 on a VPN server
3. **Firewall**: Is traffic allowed through the WireGuard interface and forwarded?
4. **Routing table**: `ip route` — is there a route for the destination via the WireGuard interface?
5. **Peer status**: `wg show` — check handshake time; if never, peers can't reach each other
6. **NAT/Masquerade**: If routing to a LAN, is NAT configured for the WireGuard subnet?

## How do you check WireGuard peer status?
```bash
sudo wg show
# Output shows:
# - Peer public key
# - Endpoint (IP:port) — "none" if not yet connected
# - Allowed IPs
# - Latest handshake — timestamp (critical! shows if tunnel is active)
# - Transfer — bytes sent/received
# - Persistent keepalive interval
```

If `latest handshake` is blank or very old, the peers haven't exchanged keys recently.

## Scenario: WireGuard peers can't establish a handshake. What do you check?
1. **Endpoint reachable**: Can peer A reach peer B's endpoint IP:port? (`nc -zu <ip> 51820`)
2. **Firewall**: Is UDP port 51820 (or custom port) open on both sides?
3. **Correct public key**: Verify the public key configured for each peer is correct
4. **NAT traversal**: Add `PersistentKeepalive = 25` to maintain NAT mappings
5. **Both sides configured**: Both peers must have each other's public key and AllowedIPs

## Scenario: Tailscale is showing devices as connected but they can't ping each other. What do you check?
1. **ACL policy**: Check the admin console ACLs — is traffic between these devices allowed?
2. **Subnet routing**: If accessing a non-Tailscale device, is the subnet router running and route approved?
3. **`--accept-routes`**: On the client, is `sudo tailscale up --accept-routes` set?
4. `tailscale ping <device>` — shows if direct or via DERP relay
5. `tailscale status` — shows connected peers and their IPs
6. Check firewall on destination — is the Tailscale IP (100.x.y.z) allowed?

## Scenario: VPN clients can reach the VPN server but not resources behind it. What do you check?
1. **IP forwarding**: Enabled on the VPN server? (`sysctl net.ipv4.ip_forward`)
2. **Routing**: Does the VPN server have routes to the target network?
3. **NAT/Masquerade**: Is the VPN server masquerading traffic so return traffic comes back?
4. **Return route**: Do servers behind the VPN have a route back to the VPN client subnet?
5. **Firewall FORWARD chain**: Is the VPN server allowing forwarded traffic?

## What iptables rules are needed for a WireGuard VPN server?
```bash
# Allow forwarding between WireGuard and LAN
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A FORWARD -o wg0 -j ACCEPT

# NAT so return traffic comes back through the VPN
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE

# To persist across reboots:
# PostUp/PreDown in WireGuard config:
PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PreDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

## Scenario: Split tunnel VPN: some traffic goes through VPN but not the expected traffic. What do you check?
1. Check `AllowedIPs` (WireGuard) — only IPs listed here are routed through the tunnel
2. Check routing table: `ip route show table main` — what routes are set?
3. Verify the VPN client's routing policy matches expectations
4. Test: `traceroute 8.8.8.8` — does internet traffic exit locally or through VPN?

## Scenario: VPN connection drops frequently. What are the causes?
1. **NAT timeout**: NAT mappings expire; use `PersistentKeepalive` (WireGuard) or keepalive timers
2. **MTU issues**: VPN encapsulation adds overhead; reduce MTU on VPN interface (e.g., 1420 for WireGuard)
3. **Network instability**: Packet loss on the underlying connection
4. **IP changes**: Client IP changed (mobile/roaming); WireGuard handles this; IPsec needs MOBIKE

## What is the VPN MTU issue and how do you fix it?
VPN encapsulation adds overhead:
- WireGuard: 60 bytes overhead → set MTU to 1420 (Ethernet 1500 − 80 bytes)
- IPsec ESP: ~50 bytes overhead → MTU 1450

```bash
# In WireGuard config [Interface]:
MTU = 1420

# Test for fragmentation:
ping -M do -s 1400 <vpn-peer-ip>  # If fails, MTU too high
```

## Scenario: Tailscale exit node is configured but only some traffic goes through it. What do you check?
1. Is `--exit-node=<ip>` set on the client?
2. `tailscale status` — shows current exit node
3. Is `--exit-node-allow-lan-access` needed for local resources?
4. Does the exit node have `--advertise-exit-node` set?
5. Is the exit node approved in the admin console?
