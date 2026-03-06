# Tailscale

## What is Tailscale?
Tailscale is a **mesh VPN service** built on WireGuard that makes it easy to create a secure, private network (a "tailnet") between devices. It handles key management, NAT traversal, and routing automatically using a **control plane** hosted by Tailscale.

## How does Tailscale differ from traditional WireGuard?
| Feature               | Raw WireGuard      | Tailscale           |
|-----------------------|--------------------|---------------------|
| Key management        | Manual             | Automatic           |
| NAT traversal         | Manual             | Automatic (DERP)    |
| Device discovery      | Manual config      | Tailscale control plane |
| ACLs                  | AllowedIPs only    | Policy-based ACLs   |
| Authentication        | Keys only          | SSO/Identity providers |
| Setup complexity      | High               | Very low            |

## What is a tailnet?
The **private mesh network** created by Tailscale, containing all your authenticated devices. Every device in your tailnet gets a stable **100.x.y.z** IP address (from the CGNAT range `100.64.0.0/10`).

## What IP range does Tailscale use?
Tailscale assigns addresses from the **`100.64.0.0/10`** CGNAT range (specifically `100.64.0.0` – `100.127.255.255`). These are stable and don't change as devices roam.

## What is DERP in Tailscale?
**Designated Encrypted Relay for Packets** — fallback relay servers operated by Tailscale when direct peer-to-peer connections cannot be established (due to strict NAT or firewalls). Traffic is still encrypted end-to-end with WireGuard.

## How does Tailscale establish direct peer-to-peer connections?
Using techniques similar to **WebRTC ICE**:
1. Direct connection attempt (LAN)
2. STUN-like hole-punching through NAT
3. Fallback to DERP relay if direct connection fails

## What is MagicDNS in Tailscale?
An automatic DNS feature that gives each device a **hostname** in your tailnet (e.g., `my-laptop.tail1234.ts.net`) and makes them resolvable across all devices without manual DNS configuration.

## How do you install and authenticate Tailscale on Linux?
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up             # Authenticate via browser
sudo tailscale up --authkey=<key>  # Headless/automated
tailscale status              # Show connected devices
tailscale ip                  # Show your Tailscale IP
```

## What are Tailscale ACLs (Access Control Lists)?
JSON-based policies that define **which devices can communicate with which**. Defined in the Tailscale admin console:
```json
{
  "acls": [
    {"action": "accept", "src": ["group:dev"], "dst": ["tag:prod:22"]},
    {"action": "accept", "src": ["*"], "dst": ["*:*"]}
  ]
}
```

## What are Tailscale tags?
**Labels applied to devices** for use in ACL policies. Tags allow policy-based access control rather than per-device rules. Devices can be tagged via admin console or `--advertise-tags` flag.

## What is the Tailscale admin console?
The web interface at `https://login.tailscale.com/admin` where you manage devices, users, ACLs, and DNS settings for your tailnet.

## What authentication providers does Tailscale support?
- Google
- Microsoft (Azure AD)
- GitHub
- Okta
- OneLogin
- Email (magic link)
- Any OIDC/SAML provider (enterprise plans)

## What is `tailscale ping`?
A diagnostic command to test connectivity to a Tailscale peer:
```bash
tailscale ping 100.64.0.1    # Shows RTT and whether direct or via DERP
```

## Is Tailscale open source?
The Tailscale **client** is open source. The **control plane** (coordination server) is operated by Tailscale Inc. as a service. **Headscale** is an open-source, self-hosted alternative to the Tailscale control plane.
