# DNS Resolvers

## What is a DNS resolver?
A **DNS resolver** (also called a recursive resolver or recursive nameserver) is the first point of contact in the DNS lookup process. It:
1. Receives a DNS query from a client
2. Checks its cache
3. If not cached, performs a **recursive query** by contacting root, TLD, and authoritative nameservers
4. Returns the answer to the client and caches it

## What is a recursive DNS query?
A query where the resolver takes full responsibility for resolving the domain. The client asks once and the resolver does all the work, contacting multiple nameservers as needed before returning a final answer.

## What is an iterative DNS query?
A query where the server responds with the best answer it has (possibly a referral to another nameserver), and the **client or resolver** is responsible for following up with the referred server. Root servers respond iteratively.

## What is the DNS resolution process step-by-step?
1. Client checks its **local DNS cache** (and OS hosts file)
2. Query sent to **recursive resolver** (configured via DHCP or manually)
3. Resolver checks its **cache**
4. Resolver queries a **root nameserver** (.)
5. Root refers resolver to the **TLD nameserver** (.com, .org, etc.)
6. TLD refers resolver to the **authoritative nameserver** for the domain
7. Authoritative server responds with the **IP address**
8. Resolver caches and returns the result to the client

## What is a stub resolver?
A minimal DNS client built into an operating system that simply forwards queries to a configured recursive resolver. It does not perform recursive resolution itself.

## What is a forwarder in DNS?
A DNS server configured to **forward queries it cannot resolve locally** to another DNS server (instead of performing full recursion). Common in corporate environments where internal servers forward external queries to an ISP or public resolver.

## What are popular public DNS resolvers?
- **Google**: `8.8.8.8` and `8.8.4.4`
- **Cloudflare**: `1.1.1.1` and `1.0.0.1`
- **Quad9**: `9.9.9.9` (security-focused, blocks malicious domains)
- **OpenDNS**: `208.67.222.222` and `208.67.220.220`

## What is DNS over HTTPS (DoH)?
A protocol that encrypts DNS queries inside HTTPS (port 443), preventing ISPs and network eavesdroppers from seeing DNS queries. Implemented in browsers (Firefox, Chrome) and OS-level resolvers.

## What is DNS over TLS (DoT)?
Encrypts DNS queries using TLS on **port 853**. Unlike DoH, it uses a dedicated port, making it easier to manage/filter at the network level. Provides confidentiality and integrity for DNS traffic.

## What is DNSSEC?
**DNS Security Extensions** — a suite of extensions that adds cryptographic signatures to DNS records to verify authenticity. Protects against DNS spoofing/cache poisoning. Uses records like **RRSIG**, **DNSKEY**, **DS**, and **NSEC**.

## What does the `/etc/resolv.conf` file contain on Linux?
The DNS resolver configuration:
```
nameserver 8.8.8.8     # Primary DNS server
nameserver 8.8.4.4     # Secondary DNS server
search example.com     # Domain search list
```

## What is the systemd-resolved service?
A Linux system service that provides network name resolution. It acts as a **local stub resolver** on `127.0.0.53:53` and forwards queries to configured upstream resolvers. Configured in `/etc/systemd/resolved.conf`.
