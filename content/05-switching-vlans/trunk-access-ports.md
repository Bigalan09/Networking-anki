# Trunk and Access Ports

## What is an access port?
A switch port configured to carry traffic for **only one VLAN**. Frames on access ports are **untagged** — the switch adds and strips VLAN tags internally. Used for end devices (computers, printers, phones).

## What is a trunk port?
A switch port configured to carry traffic for **multiple VLANs simultaneously**. Frames are **802.1Q tagged** with the VLAN ID, allowing a single physical link to transport multiple VLANs between switches, routers, or hypervisors.

## When would you use an access port?
- Connecting end-user devices (PCs, printers)
- Connecting servers that don't need VLAN awareness
- Connecting IP phones (typically in a voice VLAN)
- Any device that only needs to be on one VLAN

## When would you use a trunk port?
- Between two switches
- Between a switch and a router (for inter-VLAN routing)
- Between a switch and a hypervisor (VM traffic across VLANs)
- Between a switch and a wireless access point (multiple SSIDs mapped to VLANs)

## How do you configure an access port on Cisco IOS?
```
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
```

## How do you configure a trunk port on Cisco IOS?
```
interface GigabitEthernet0/2
 switchport mode trunk
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99
```

## What is DTP (Dynamic Trunking Protocol)?
A **Cisco proprietary** protocol that automatically negotiates trunk links between switches. Port modes:
- **auto**: Passive — will become a trunk if the other side initiates
- **desirable**: Active — will try to negotiate a trunk
- **trunk**: Forces trunk regardless
- **access**: Forces access regardless
- **nonegotiate**: Disables DTP (security best practice)

## Why should you disable DTP on user-facing ports?
To prevent **VLAN hopping attacks** where an attacker's device negotiates a trunk link with the switch, gaining access to all VLANs. Set user ports to `switchport mode access` and `switchport nonegotiate`.

## What is an allowed VLAN list on a trunk?
The set of VLANs permitted to traverse a trunk port. By default, all VLANs (1–4094) are allowed. Best practice: restrict to only the VLANs needed on that trunk.

## What happens to frames for a VLAN not in the allowed list on a trunk?
They are **dropped** and not forwarded on that trunk port.

## What is a voice VLAN?
A special VLAN configuration on an access port to support **IP phones**:
```
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10      # data VLAN for PC
 switchport voice vlan 20       # voice VLAN for phone
```
The phone sends tagged voice traffic (VLAN 20) and passes untagged PC traffic (VLAN 10).

## What is the difference between a trunk port and a hybrid port?
- **Trunk**: Carries multiple VLANs, all traffic tagged except native VLAN
- **Hybrid**: (Huawei/some vendors) Can carry both tagged and untagged VLANs on the same port, with explicit control over which VLANs are tagged/untagged

## What is a LACP/LAGG trunk?
**Link Aggregation** — combining multiple physical ports into a single logical trunk (bond/LAG) for bandwidth and redundancy. Uses **802.3ad LACP** (Link Aggregation Control Protocol). Different from a VLAN trunk — though both can coexist.

## How do you verify trunk configuration on Cisco IOS?
```
show interfaces trunk           # Shows trunk ports, VLANs allowed, active
show interfaces GigEth0/1 trunk # Specific port
show vlan brief                 # Shows VLANs and assigned ports
```
