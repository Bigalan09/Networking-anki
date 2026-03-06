# Subnet Calculations — /16 through /30

## What are the key facts for a /16 subnet?
- Subnet mask: `255.255.0.0`
- Block size: 65536 addresses
- Usable hosts: **65534**
- Host bits: 16

## What are the key facts for a /17 subnet?
- Subnet mask: `255.255.128.0`
- Block size: 32768 addresses
- Usable hosts: **32766**
- Host bits: 15

## What are the key facts for a /18 subnet?
- Subnet mask: `255.255.192.0`
- Block size: 16384 addresses
- Usable hosts: **16382**
- Host bits: 14

## What are the key facts for a /19 subnet?
- Subnet mask: `255.255.224.0`
- Block size: 8192 addresses
- Usable hosts: **8190**
- Host bits: 13

## What are the key facts for a /20 subnet?
- Subnet mask: `255.255.240.0`
- Block size: 4096 addresses
- Usable hosts: **4094**
- Host bits: 12

## What are the key facts for a /21 subnet?
- Subnet mask: `255.255.248.0`
- Block size: 2048 addresses
- Usable hosts: **2046**
- Host bits: 11

## What are the key facts for a /22 subnet?
- Subnet mask: `255.255.252.0`
- Block size: 1024 addresses
- Usable hosts: **1022**
- Host bits: 10

## What are the key facts for a /23 subnet?
- Subnet mask: `255.255.254.0`
- Block size: 512 addresses
- Usable hosts: **510**
- Host bits: 9

## What are the key facts for a /24 subnet?
- Subnet mask: `255.255.255.0`
- Block size: 256 addresses
- Usable hosts: **254**
- Host bits: 8

## What are the key facts for a /25 subnet?
- Subnet mask: `255.255.255.128`
- Block size: 128 addresses
- Usable hosts: **126**
- Host bits: 7

## What are the key facts for a /26 subnet?
- Subnet mask: `255.255.255.192`
- Block size: 64 addresses
- Usable hosts: **62**
- Host bits: 6

## What are the key facts for a /27 subnet?
- Subnet mask: `255.255.255.224`
- Block size: 32 addresses
- Usable hosts: **30**
- Host bits: 5

## What are the key facts for a /28 subnet?
- Subnet mask: `255.255.255.240`
- Block size: 16 addresses
- Usable hosts: **14**
- Host bits: 4

## What are the key facts for a /29 subnet?
- Subnet mask: `255.255.255.248`
- Block size: 8 addresses
- Usable hosts: **6**
- Host bits: 3

## What are the key facts for a /30 subnet?
- Subnet mask: `255.255.255.252`
- Block size: 4 addresses
- Usable hosts: **2**
- Host bits: 2

## What is the network address for 10.5.200.100/20?
- /20 block size in third octet: 16
- 200 ÷ 16 = 12 remainder 8 → block starts at 192
- Network: `10.5.192.0/20`
- Broadcast: `10.5.207.255`

## What is the network address for 172.31.127.50/18?
- /18 block size in third octet: 64
- 127 ÷ 64 = 1 remainder 63 → block starts at 64
- Network: `172.31.64.0/18`
- Broadcast: `172.31.127.255`

## How many /27 subnets are in a /22 network?
- /22 has 1024 addresses; /27 has 32 addresses
- 1024 ÷ 32 = **32** subnets

## How many /29 subnets are in a /24 network?
- /24 has 256 addresses; /29 has 8 addresses
- 256 ÷ 8 = **32** subnets

## How many /26 subnets are in a /20 network?
- /20 has 4096 addresses; /26 has 64 addresses
- 4096 ÷ 64 = **64** subnets

## What is the third usable host in 192.168.100.64/26?
- Network: `192.168.100.64`
- First usable: `192.168.100.65`
- Second usable: `192.168.100.66`
- Third usable: **`192.168.100.67`**

## What subnet does 172.16.50.175 belong to with mask /19?
- /19 block size in third octet: 32
- 50 ÷ 32 = 1 remainder 18 → block starts at 32
- Network: `172.16.32.0/19`
- Broadcast: `172.16.63.255`

## What is the broadcast address for 10.0.0.0/21?
- /21 block size in third octet: 8
- Network: `10.0.0.0`, Broadcast: **`10.0.7.255`**
