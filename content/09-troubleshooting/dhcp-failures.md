# DHCP Troubleshooting

## Scenario: A host gets 169.254.x.x and cannot access the network. What is the cause?
The host received an **APIPA (Automatic Private IP Addressing)** address, meaning it **failed to get a DHCP lease**. It could not find a DHCP server.

Causes: DHCP server down, no DHCP relay agent (host on different subnet), DHCP pool exhausted, host NIC issue.

## What are the steps to troubleshoot a DHCP failure?

1. **Check DHCP server**: Is it running? (`systemctl status isc-dhcp-server`)
2. **Check IP pool**: Is the pool exhausted? (`show ip dhcp binding` on router)
3. **Check DHCP relay**: If server is on a different subnet, is `ip helper-address` configured on the router?
4. **Check firewall**: Is UDP 67/68 allowed?
5. **Check cable/VLAN**: Physical connectivity, correct VLAN assignment
6. **Test with `dhclient`**: `sudo dhclient -v eth0` (shows full DORA exchange)
7. **Capture with tcpdump**: `tcpdump -i eth0 port 67 or port 68`

## What is a DHCP relay agent and why is it needed?
DHCP uses **broadcast** for Discover messages. Routers don't forward broadcasts between subnets. A **DHCP relay agent** (configured with `ip helper-address <dhcp-server-ip>` on Cisco) converts the broadcast to a **unicast** forwarded to the DHCP server.

## What is DHCP pool exhaustion and how do you fix it?
When all IP addresses in the DHCP pool are leased out. Symptoms: new clients can't get addresses; existing clients may lose leases.

Fixes:
- Expand the IP pool (use larger subnet)
- Shorten lease times to reclaim addresses faster
- Check for stale leases from old/disconnected devices
- Check for DHCP starvation attack (MAC spoofing)

## What is a DHCP starvation attack?
An attacker sends many DHCP Discover packets with **different spoofed MAC addresses**, exhausting the IP pool so legitimate clients can't get addresses.

Mitigation: **DHCP snooping** (inspects DHCP messages, limits requests per port).

## What is DHCP snooping?
A Layer 2 security feature on switches that:
- Allows DHCP responses only from **trusted ports** (ports connected to legitimate DHCP servers)
- Limits the number of DHCP requests per second per port
- Builds a binding table (MAC, IP, VLAN, port) used by Dynamic ARP Inspection

## What is a rogue DHCP server?
An unauthorized DHCP server on the network that issues incorrect IP configurations (wrong gateway, DNS pointing to attacker). **DHCP snooping** prevents rogue servers by blocking DHCP offers on untrusted ports.

## A client gets an IP but can't access the internet. How do you troubleshoot?
1. `ip route` — verify default gateway is set
2. `ping <gateway>` — verify gateway is reachable
3. `ping 8.8.8.8` — verify internet routing works
4. `ping google.com` — verify DNS works
5. `nslookup google.com` — isolate DNS issue
6. Check DHCP-provided DNS servers: `cat /etc/resolv.conf` or check lease info

## What are DHCP lease files and where are they?
- **ISC DHCP client**: `/var/lib/dhcp/dhclient.leases`
- **systemd-networkd**: `networkctl status`
- **Windows**: `ipconfig /all` shows lease info

## How do you force a DHCP lease renewal?
```bash
# Linux
sudo dhclient -r eth0   # Release
sudo dhclient eth0      # Renew

# Windows
ipconfig /release
ipconfig /renew
```

## What does "DHCP NAK" mean?
A **DHCP Negative Acknowledgment** — the server rejects the client's DHCP Request (e.g., the requested IP is no longer available or assigned to another host). The client restarts the DORA process.

## Scenario: After moving a VM to a new VLAN, it can't get a DHCP address. What do you check?
1. Is the DHCP scope for the new VLAN subnet configured on the DHCP server?
2. Is a DHCP relay agent configured for the new VLAN (pointing to the DHCP server)?
3. Is the switch port in the correct VLAN? (`show interfaces switchport`)
4. Is the firewall allowing DHCP traffic between VLANs?
