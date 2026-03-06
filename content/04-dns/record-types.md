# DNS Record Types

## What is an A record?
Maps a **hostname to an IPv4 address**.
```
www.example.com.  300  IN  A  203.0.113.10
```
Multiple A records for the same name enable basic **round-robin load balancing**.

## What is an AAAA record?
Maps a **hostname to an IPv6 address** (quad-A record).
```
www.example.com.  300  IN  AAAA  2001:db8::1
```

## What is a CNAME record?
**Canonical Name** — an alias that points one hostname to another hostname. The target (right-hand side) must ultimately resolve to an A or AAAA record.
```
blog.example.com.  300  IN  CNAME  www.example.com.
```
**Cannot** be used at the zone apex (root of the domain) with other records.

## What is an MX record?
**Mail Exchanger** — specifies the mail servers responsible for accepting email for the domain. Includes a **priority** value (lower = preferred):
```
example.com.  300  IN  MX  10  mail1.example.com.
example.com.  300  IN  MX  20  mail2.example.com.
```

## What is a TXT record?
Holds **arbitrary text data**. Used for:
- **SPF**: Email authentication
- **DKIM**: Email signing key
- **DMARC**: Email policy
- **Domain verification** (Google Search Console, etc.)
```
example.com.  300  IN  TXT  "v=spf1 ip4:203.0.113.0/24 -all"
```

## What is an NS record?
**Name Server** — identifies the authoritative nameservers for a domain or zone:
```
example.com.  86400  IN  NS  ns1.example.com.
example.com.  86400  IN  NS  ns2.example.com.
```

## What is a PTR record?
**Pointer record** — maps an **IP address to a hostname** (reverse DNS lookup). Stored in the `in-addr.arpa` domain for IPv4 or `ip6.arpa` for IPv6:
```
10.113.0.203.in-addr.arpa.  300  IN  PTR  www.example.com.
```

## What is an SOA record?
**Start of Authority** — the first record in a zone, containing administrative information including the primary nameserver, responsible party email, serial number, and cache timing parameters.

## What is an SRV record?
**Service record** — specifies location (hostname and port) of servers for specific services. Format: `_service._protocol.name TTL class SRV priority weight port target`
```
_sip._tcp.example.com.  300  IN  SRV  10 20 5060 sip.example.com.
```

## What is a CAA record?
**Certification Authority Authorization** — specifies which Certificate Authorities (CAs) are allowed to issue SSL/TLS certificates for a domain. Helps prevent unauthorized certificate issuance:
```
example.com.  300  IN  CAA  0 issue "letsencrypt.org"
```

## What is the difference between a CNAME and an ALIAS/ANAME record?
- **CNAME**: An alias at the DNS protocol level. Cannot be at zone apex. Client follows the chain.
- **ALIAS/ANAME**: A **DNS provider-specific** feature that behaves like a CNAME but resolves to an IP at query time, allowing it at the zone apex. Not a standard DNS record type.

## Can you put a CNAME at the root of a domain?
**No.** A CNAME at the zone apex (e.g., `example.com`) is not allowed by RFC 1034 because you cannot have other records (like MX, NS) alongside a CNAME. Use ALIAS/ANAME instead if your provider supports it.

## What happens during a DNS lookup for `blog.example.com` if it's a CNAME?
1. Resolver queries for `blog.example.com`
2. Gets CNAME → `www.example.com`
3. Resolver queries for `www.example.com`
4. Gets A record → `203.0.113.10`
5. Returns IP to client (multiple round trips = extra latency)

## What is TTL in DNS?
**Time to Live** — how long (in seconds) a DNS record should be cached by resolvers and clients. Lower TTL = faster propagation of changes but more DNS queries. Higher TTL = less query load but slower propagation.

## What is DNS propagation?
The time it takes for DNS record changes to propagate across DNS servers worldwide. Determined primarily by the **TTL** of the record being changed. Lowering TTL before a change (e.g., 5 minutes) speeds propagation.
