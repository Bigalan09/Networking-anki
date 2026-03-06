# Authoritative DNS Servers

## What is an authoritative DNS server?
A nameserver that **holds the actual DNS records** for a domain and provides definitive answers (without querying elsewhere). It is the final authority for a zone.

## What is the difference between authoritative and recursive DNS?
- **Authoritative**: Holds and serves actual zone records. Only answers queries about zones it hosts.
- **Recursive (resolver)**: Does not hold zone data. Takes queries from clients and recurses through the DNS hierarchy to find answers.

## What are the two types of authoritative nameservers?
- **Primary (master)**: Holds the original, writeable zone file. DNS changes are made here.
- **Secondary (slave)**: Holds a read-only copy of the zone, synchronized from the primary via **zone transfer** (AXFR/IXFR).

## What is a DNS zone?
A DNS zone is a **contiguous portion of the DNS namespace** administered by a specific organization or manager. A zone file contains DNS records for that zone (A, MX, CNAME, etc.).

## What are NS records?
**Name Server records** — specify the authoritative nameservers for a domain. Example:
```
example.com.  IN  NS  ns1.example.com.
example.com.  IN  NS  ns2.example.com.
```

## What is the SOA record?
**Start of Authority** — the first record in a zone file, containing:
- **MNAME**: Primary nameserver
- **RNAME**: Responsible person's email (dots instead of @)
- **Serial**: Version number (increment on changes)
- **Refresh**: How often secondaries check for updates
- **Retry**: How often secondaries retry if refresh fails
- **Expire**: When secondary stops responding if no refresh
- **Minimum TTL**: Negative caching TTL

## What is a zone transfer?
The process of replicating a zone file from a primary to secondary nameserver:
- **AXFR**: Full zone transfer (all records)
- **IXFR**: Incremental zone transfer (only changes since last serial)
Uses **TCP port 53**.

## What are root nameservers?
The 13 logical root nameserver entities (named `a.root-servers.net` through `m.root-servers.net`) that respond to queries for the DNS root zone. They refer resolvers to the appropriate **TLD nameservers**. Operated by various organizations. Replicated globally via **anycast** (hundreds of physical servers).

## What is a TLD nameserver?
A nameserver responsible for a **Top Level Domain** (.com, .net, .org, .uk, etc.). When queried, it refers resolvers to the **authoritative nameserver** for the specific domain under that TLD.

## What is a glue record?
An **A record in the parent zone** that provides the IP address of a nameserver when the nameserver is within the domain it's authoritative for. Prevents a circular dependency.

Example: `ns1.example.com` is the nameserver for `example.com`. The parent TLD zone includes a glue A record: `ns1.example.com. A 203.0.113.1`.

## What is negative caching in DNS?
Caching the **non-existence** of a DNS record. When a resolver gets an NXDOMAIN (domain doesn't exist) or NOERROR with no records response, it caches that negative result for the duration of the **Minimum TTL** in the SOA record.

## What is DNS delegation?
The process of assigning authority for a **subdomain** to different nameservers. The parent zone contains **NS records** pointing to the nameservers of the delegated zone.

Example: `ops.example.com` is delegated to `ns1.ops.example.com`.

## What is a hidden primary (stealth primary)?
A primary DNS server that is **not listed in the zone's NS records** and is not publicly accessible. Secondary servers listed in NS records replicate from it. Protects the primary from direct attack and zone enumeration.
