# Mental Subnetting

## What is the "magic number" method for quick subnetting?
The **magic number** (block size) = 256 − subnet mask octet value.

Example: mask `255.255.255.224` → magic number = 256 − 224 = **32**. Subnets increment by 32: .0, .32, .64, .96...

## What is the magic number for a /25 mask?
256 − 128 = **128**. Subnets: .0 and .128.

## What is the magic number for a /26 mask?
256 − 192 = **64**. Subnets: .0, .64, .128, .192.

## What is the magic number for a /27 mask?
256 − 224 = **32**. Subnets: .0, .32, .64, .96, .128, .160, .192, .224.

## What is the magic number for a /28 mask?
256 − 240 = **16**. Subnets: .0, .16, .32, .48, .64, .80, .96, .112, .128, .144, .160, .176, .192, .208, .224, .240.

## What is the magic number for a /29 mask?
256 − 248 = **8**. Subnets: .0, .8, .16, .24, .32, .40... .248.

## What is the magic number for a /30 mask?
256 − 252 = **4**. Subnets: .0, .4, .8, .12... .252.

## Quick quiz: Which subnet does 192.168.1.100 belong to with /27?
- Magic number = 32
- 100 ÷ 32 = 3 remainder 4 → block starts at 96
- Subnet: **192.168.1.96/27** (broadcast: .127)

## Quick quiz: Which subnet does 10.10.10.200 belong to with /28?
- Magic number = 16
- 200 ÷ 16 = 12 remainder 8 → block starts at 192
- Subnet: **10.10.10.192/28** (broadcast: .207)

## Quick quiz: Which subnet does 172.20.5.45 belong to with /29?
- Magic number = 8
- 45 ÷ 8 = 5 remainder 5 → block starts at 40
- Subnet: **172.20.5.40/29** (broadcast: .47)

## Quick quiz: Is 192.168.50.130 in the same /26 as 192.168.50.100?
- Magic number = 64. Subnets: .0, .64, .128, .192
- .130 is in the .128 subnet; .100 is in the .64 subnet
- **No**, they are in different subnets.

## What is the last usable host in 10.0.0.0/29?
- Block size = 8; Broadcast = 10.0.0.7
- Last usable: **10.0.0.6**

## What is the last usable host in 192.168.1.192/26?
- Block size = 64; Broadcast = 192.168.1.255
- Last usable: **192.168.1.254**

## How many /30 subnets can fit in 192.168.1.0/24?
- /24 = 256 addresses; /30 block size = 4
- 256 ÷ 4 = **64** subnets

## A /22 starts at 10.4.0.0. What is the last address?
- /22 block size = 1024 addresses across 4 Class C blocks
- Last address: **10.4.3.255**

## A /20 starts at 172.16.48.0. What is the last address?
- /20 block size = 4096 addresses (16 × 256)
- 48 + 15 = 63 → Last address: **172.16.63.255**

## How do you quickly find if an IP is in a subnet without bitwise math?
1. Identify the block size (magic number)
2. Find the subnet start: the highest multiple of block size ≤ the host octet
3. Broadcast = subnet start + block size − 1
4. If the IP octet is between start and broadcast inclusive → same subnet

## How many bits need to be borrowed from a /24 to get at least 10 subnets?
- Need 2ⁿ ≥ 10 → n = 4 (2⁴ = 16 ≥ 10)
- Borrow 4 bits → **/28**

## How many bits need to be borrowed from a /24 to accommodate 50 hosts per subnet?
- Need 2ⁿ − 2 ≥ 50 → n = 6 (2⁶ − 2 = 62 ≥ 50)
- Keep 6 host bits → **/26**

## What is the VLSM approach for designing subnets?
1. Sort subnets **largest to smallest** by host requirement
2. Allocate the smallest prefix that satisfies each requirement
3. Assign non-overlapping address blocks, starting from the beginning of the address space
4. Document each subnet's network, broadcast, and usable range

## Power of 2 cheat sheet
| Power | Value  |
|-------|--------|
| 2⁰    | 1      |
| 2¹    | 2      |
| 2²    | 4      |
| 2³    | 8      |
| 2⁴    | 16     |
| 2⁵    | 32     |
| 2⁶    | 64     |
| 2⁷    | 128    |
| 2⁸    | 256    |
| 2⁹    | 512    |
| 2¹⁰   | 1024   |
| 2¹¹   | 2048   |
| 2¹²   | 4096   |
| 2¹⁶   | 65536  |
