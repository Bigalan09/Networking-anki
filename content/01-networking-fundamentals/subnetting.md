# Subnetting

## What is subnetting?
Subnetting is the process of dividing a single IP network into smaller logical sub-networks (subnets). It improves network organization, security, and efficiency by reducing broadcast domains.

## What is a subnet mask?
A 32-bit number that divides an IP address into the **network portion** and the **host portion**. Written in dotted-decimal (e.g., `255.255.255.0`) or CIDR prefix notation (e.g., `/24`).

## What is the subnet mask for a /24 network?
`255.255.255.0` — 24 bits for network, 8 bits for hosts.

## How do you calculate the number of usable hosts in a subnet?
**2ⁿ − 2**, where n is the number of **host bits**. The two subtracted addresses are the **network address** (all host bits = 0) and the **broadcast address** (all host bits = 1).

## What are the network address and broadcast address?
- **Network address**: The first address in the subnet (all host bits set to 0). Identifies the subnet itself.
- **Broadcast address**: The last address in the subnet (all host bits set to 1). Used to send packets to all hosts on the subnet.

## How do you find the network address of a host?
Perform a **bitwise AND** of the host's IP address and its subnet mask. The result is the network address.

## How do you find the broadcast address of a subnet?
Set all the **host bits** to 1 in the network address. Alternatively: Network address + (2ⁿ − 1), where n = number of host bits.

## What is a /30 subnet used for?
A `/30` subnet provides **2 usable host addresses** (2² − 2 = 2). It is commonly used for **point-to-point links** between two routers.

## How many usable hosts are in a /29 subnet?
**6 usable hosts** (2³ − 2 = 6). A /29 has 3 host bits.

## How many usable hosts are in a /28 subnet?
**14 usable hosts** (2⁴ − 2 = 14). A /28 has 4 host bits.

## How many usable hosts are in a /27 subnet?
**30 usable hosts** (2⁵ − 2 = 30). A /27 has 5 host bits.

## How many usable hosts are in a /26 subnet?
**62 usable hosts** (2⁶ − 2 = 62). A /26 has 6 host bits.

## How many usable hosts are in a /25 subnet?
**126 usable hosts** (2⁷ − 2 = 126). A /25 has 7 host bits.

## How many usable hosts are in a /24 subnet?
**254 usable hosts** (2⁸ − 2 = 254). A /24 has 8 host bits.

## How many usable hosts are in a /23 subnet?
**510 usable hosts** (2⁹ − 2 = 510). A /23 has 9 host bits.

## How many usable hosts are in a /22 subnet?
**1022 usable hosts** (2¹⁰ − 2 = 1022). A /22 has 10 host bits.

## How many usable hosts are in a /21 subnet?
**2046 usable hosts** (2¹¹ − 2 = 2046). A /21 has 11 host bits.

## How many usable hosts are in a /20 subnet?
**4094 usable hosts** (2¹² − 2 = 4094). A /20 has 12 host bits.

## How many usable hosts are in a /16 subnet?
**65534 usable hosts** (2¹⁶ − 2 = 65534). A /16 has 16 host bits.

## What is the "block size" method for subnetting?
The block size (or subnet size) = 2ⁿ where n = host bits. Subnets start at multiples of the block size within the relevant octet.

For /27 (block size = 32): subnets are .0, .32, .64, .96, .128, .160, .192, .224

## How many /24 subnets fit in a /16?
**256** subnets (2⁸ = 256, since /24 − /16 = 8 bits borrowed).

## How many /27 subnets fit in a /24?
**8** subnets (2³ = 8, since /27 − /24 = 3 bits borrowed).

## What is variable-length subnet masking (VLSM)?
VLSM allows different subnets within the same network to use **different** prefix lengths, enabling more efficient use of IP address space by sizing subnets to actual needs.

## What is the subnet for IP address 192.168.10.130/26?
- Block size for /26 = 64
- Subnets: .0, .64, .128, .192
- 130 falls in the **.128 subnet**
- Network: `192.168.10.128`
- Broadcast: `192.168.10.191`
- Usable hosts: `192.168.10.129` – `192.168.10.190`

## What is the subnet for IP address 10.0.5.200/27?
- Block size for /27 = 32
- Subnets in the 5.x range: .160, .192, .224
- 200 falls in the **.192 subnet**
- Network: `10.0.5.192`
- Broadcast: `10.0.5.223`
- Usable hosts: `10.0.5.193` – `10.0.5.222`

## What does "borrowing bits" mean in subnetting?
Taking bits from the **host portion** and using them as additional **network bits** to create more subnets. Each bit borrowed doubles the number of subnets but halves the number of hosts per subnet.
