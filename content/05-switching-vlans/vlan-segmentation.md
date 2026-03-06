# VLAN Segmentation

## What is a VLAN?
A **Virtual Local Area Network** — a logical grouping of network devices that behave as if they are on the same physical LAN, regardless of their physical location. VLANs are implemented at Layer 2 (switch level).

## Why use VLANs?
- **Security**: Isolate sensitive traffic (e.g., PCI, management plane)
- **Segmentation**: Separate departments (HR, Finance, Engineering)
- **Broadcast control**: Reduce broadcast domains
- **Flexibility**: Group devices regardless of physical location
- **Performance**: Limit unnecessary traffic

## What is the default VLAN on most switches?
**VLAN 1** — all ports belong to VLAN 1 by default. Best practice: never use VLAN 1 for user traffic; assign dedicated VLANs and leave VLAN 1 empty.

## What is the VLAN ID range?
- **Normal range**: 1–1005 (stored in NVRAM, supported by older VTP)
- **Extended range**: 1006–4094 (requires VTP transparent mode or VTPv3)
- Reserved: 1002–1005 (legacy FDDI/Token Ring VLANs)

## How does a switch know which VLAN a frame belongs to?
- **Access ports**: Untagged frames are assigned to the port's configured VLAN
- **Trunk ports**: Tagged frames (802.1Q) carry the VLAN ID in the frame header

## What is 802.1Q VLAN tagging?
An IEEE standard that inserts a **4-byte tag** into Ethernet frames between the source MAC and EtherType:
- 16-bit **Tag Protocol Identifier (TPID)**: `0x8100`
- 3-bit **Priority Code Point (PCP)**: QoS
- 1-bit **Drop Eligible Indicator (DEI)**
- 12-bit **VLAN Identifier (VID)**: 1–4094

## What is the native VLAN?
On a trunk port, the **native VLAN** is the VLAN whose traffic is sent **untagged**. Both ends of a trunk must agree on the native VLAN. Mismatches cause VLAN hopping vulnerabilities. Best practice: Set native VLAN to an unused VLAN ID.

## What is a VLAN hopping attack?
A Layer 2 attack where an attacker gains access to traffic on VLANs they shouldn't have access to. Two methods:
1. **Switch spoofing**: Attacker's device negotiates a trunk link (DTP exploit)
2. **Double tagging**: Sends frames with two 802.1Q tags; outer tag stripped at first switch, inner tag carries traffic to victim VLAN (works if attacker is on native VLAN)

## How do you prevent VLAN hopping?
1. Disable DTP on all non-trunk ports (`switchport nonegotiate`)
2. Set all user-facing ports as explicit access ports
3. Change native VLAN to an unused VLAN
4. Disable unused ports and assign them to a quarantine VLAN

## What is VTP (VLAN Trunking Protocol)?
A **Cisco proprietary** protocol that propagates VLAN database changes across a switched network. Modes:
- **Server**: Can create/modify/delete VLANs, propagates changes
- **Client**: Receives VLAN database from server, cannot change
- **Transparent**: Does not participate, forwards VTP messages

**Caution**: A switch with a higher revision number can overwrite the VLAN database of all switches in the domain.

## What is Private VLAN (PVLAN)?
A VLAN feature that provides **port-level isolation within a VLAN**:
- **Promiscuous port**: Can communicate with all ports (typically the router/gateway)
- **Isolated port**: Can only communicate with promiscuous ports
- **Community port**: Can communicate within its community and with promiscuous ports

Used in hosting/DMZ environments to isolate tenants.

## How many VLANs can you have on an 802.1Q trunk?
Up to **4094** VLANs (12-bit VLAN ID: 2¹² = 4096, minus 0 and 4095 which are reserved).
