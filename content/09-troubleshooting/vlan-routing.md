# VLAN Routing Troubleshooting

## Scenario: Two hosts on different VLANs cannot communicate. What do you check?
1. **Layer 3 device**: Is there a router or Layer 3 switch connecting the VLANs?
2. **SVI/Subinterface**: Is the inter-VLAN routing interface configured with the correct IP and up/up?
3. **Default gateway**: Are both hosts pointing to the correct gateway IP for their VLAN?
4. **Routing enabled**: On L3 switch, is `ip routing` enabled?
5. **VLAN membership**: Are the hosts in the correct VLANs?
6. **Trunk port**: Is the link between the access switch and L3 switch a trunk carrying both VLANs?
7. **ACL/Firewall**: Is there an access list blocking traffic between the subnets?

## Scenario: After creating a new VLAN, hosts in that VLAN have no connectivity. Step-by-step debug.

1. `show vlan brief` — verify the VLAN exists and ports are assigned
2. `show interfaces trunk` — verify the VLAN is in the allowed list on trunk ports
3. `show interfaces vlan <id>` — verify SVI is up/up and has correct IP
4. `ip routing` — verify routing is enabled (L3 switch)
5. `show ip route` — verify routes for all VLAN subnets exist
6. Test: ping from the SVI IP to a host in the VLAN

## What does "VLAN not in allowed list" on a trunk mean?
The trunk port is configured to only carry specific VLANs (`switchport trunk allowed vlan`). If a VLAN is not in the allowed list, frames tagged with that VLAN ID are **dropped** on that trunk link.

Fix: `switchport trunk allowed vlan add <vlan-id>`

## Scenario: VLAN traffic is leaking between segments. What are possible causes?
1. **Native VLAN mismatch**: Traffic on the native VLAN (untagged) may traverse unexpected paths
2. **VLAN hopping**: Double-tagging or DTP exploitation
3. **Misconfigured ACL**: Firewall rule accidentally allowing cross-VLAN traffic
4. **Layer 3 switch routing**: Routing enabled where it shouldn't be

## What is an SVI and what does "SVI not up" mean?
A **Switched Virtual Interface** is a virtual Layer 3 interface for a VLAN. The SVI is only operational (up/up) if:
- The VLAN exists in the VLAN database
- At least **one access port** in the VLAN is in the up/up state

If the VLAN has no active ports, the SVI stays down. This breaks inter-VLAN routing for that VLAN.

## Scenario: Inter-VLAN routing works for some VLANs but not others. What do you check?
- Is the SVI for the failing VLAN up? (`show interfaces vlan X`)
- Is the VLAN in the routing table? (`show ip route`)
- Is the VLAN allowed on all trunk ports in the path?
- Are hosts in the failing VLAN configured with the correct gateway?

## How do you test Layer 2 VLAN connectivity?
```bash
# From a host, ping the gateway
ping 192.168.10.1

# On the switch, check ARP table
show arp

# On the switch, check MAC address table
show mac address-table vlan 10

# Check if the port is in the correct VLAN
show interfaces GigEth0/1 switchport
```

## What is a VLAN database mismatch between switches?
When two switches have different VLAN databases (one has VLAN 20, the other doesn't). On the switch missing the VLAN, frames tagged with that VLAN arrive on a trunk but are **dropped** because the VLAN doesn't exist locally.

Fix: Ensure VLAN database is consistent across all switches. Use VTP cautiously or manually add VLANs.

## Scenario: A host can ping the gateway but cannot reach other VLANs beyond the first hop.
1. Check routing table on the router/L3 switch: `show ip route` — are all subnets present?
2. Check if ARP is resolving for destination hosts (or further router hops)
3. Check for ACLs on inter-VLAN interfaces blocking traffic
4. Traceroute to identify where traffic stops: `traceroute <destination>`
5. Check if return traffic is routed correctly (asymmetric routing issue)
