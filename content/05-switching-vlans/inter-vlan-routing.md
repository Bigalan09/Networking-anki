# Inter-VLAN Routing

## What is inter-VLAN routing?
The process of forwarding traffic **between VLANs** using a Layer 3 device (router or Layer 3 switch). Since VLANs are separate broadcast domains, a Layer 3 device must route traffic between them.

## What are the three methods of inter-VLAN routing?
1. **Router on a stick (ROAS)**: Single physical link between switch and router, using subinterfaces for each VLAN
2. **Layer 3 switch (SVI)**: Switch performs routing internally using Switched Virtual Interfaces (SVIs)
3. **Separate router interfaces**: One physical interface per VLAN (legacy, wasteful, rarely used)

## What is a router on a stick (ROAS)?
A single physical link (trunk) between a router and a switch, with the router configured with **subinterfaces** — one per VLAN. Each subinterface is configured with the VLAN's gateway IP:

```
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0

interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

## What is an SVI (Switched Virtual Interface)?
A **virtual Layer 3 interface** on a Layer 3 switch, configured for a specific VLAN. It acts as the **default gateway** for all hosts in that VLAN:

```
interface Vlan10
 ip address 192.168.10.1 255.255.255.0
 no shutdown

interface Vlan20
 ip address 192.168.20.1 255.255.255.0
 no shutdown

ip routing   ! Enable Layer 3 routing on the switch
```

## What is the advantage of Layer 3 switching over router on a stick?
- **Wire-speed routing**: Inter-VLAN routing is done in hardware (ASIC), not software
- **No bandwidth bottleneck**: Each VLAN connects at full port speed, not sharing one trunk link
- **Lower latency**: Hardware-based forwarding
- **Simpler cabling**: No need for a separate router

## How does traffic flow between VLAN 10 and VLAN 20 on a Layer 3 switch?
1. Host in VLAN 10 sends frame to its gateway (SVI Vlan10 MAC)
2. Layer 3 switch receives frame, looks up destination IP in routing table
3. Routes to VLAN 20 subnet → forwards out SVI Vlan20
4. Frames the packet with the destination host's MAC (from ARP table)
5. Switches frame to the destination port in VLAN 20

## What must be enabled on a Cisco Layer 3 switch for routing?
```
ip routing
```
Without this command, the switch operates as a Layer 2 switch only and cannot route between VLANs.

## What is a routed port on a Layer 3 switch?
A switch port configured as a **Layer 3 interface** (not a VLAN access port):
```
interface GigabitEthernet1/0/1
 no switchport
 ip address 10.0.0.1 255.255.255.252
```
Acts like a router interface. Used for uplinks to routers or WAN connections.

## What is the difference between an SVI and a routed port?
- **SVI**: Virtual interface representing a VLAN; many physical ports can be in the VLAN
- **Routed port**: A single physical port operating at Layer 3; only that port is on that "subnet"

## How do you verify inter-VLAN routing is working?
```bash
# On a host in VLAN 10 (gateway 192.168.10.1):
ping 192.168.20.5  # Ping host in VLAN 20

# On the switch:
show ip route      # Verify routing table has both VLAN subnets
show arp           # Verify ARP entries for gateway
```

## What is a common inter-VLAN routing misconfiguration?
1. **`ip routing` not enabled** on Layer 3 switch
2. **SVI is down**: The physical VLAN has no active access ports → SVI stays down
3. **Incorrect gateway**: Host configured with wrong gateway IP
4. **VLAN not in allowed list** on the trunk port
5. **Missing SVI**: SVI not created for the destination VLAN
