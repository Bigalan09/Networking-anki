# DNS Caching

## What is DNS caching?
DNS caching is the **temporary storage of DNS query results** by resolvers, OS, and applications to avoid redundant lookups and reduce latency. Entries are cached for the duration of their **TTL** (Time to Live).

## Where does DNS caching happen?
DNS responses are cached at multiple levels:
1. **Browser cache**: Chrome, Firefox cache DNS results (typically 60s)
2. **OS resolver cache**: systemd-resolved, nscd, Windows DNS cache
3. **Stub resolver**: Forwards to recursive resolver
4. **Recursive resolver cache**: Your ISP or `8.8.8.8` caches results
5. **Intermediate nameservers**: Any server in the chain

## How do you flush the DNS cache on Linux?
```bash
# systemd-resolved
sudo systemd-resolve --flush-caches

# nscd
sudo systemctl restart nscd

# Check resolved statistics
sudo systemd-resolve --statistics
```

## How do you flush the DNS cache on macOS?
```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## How do you flush the DNS cache on Windows?
```cmd
ipconfig /flushdns
```

## What is a DNS cache poisoning attack?
An attack where a malicious DNS response is injected into a resolver's cache, redirecting users to attacker-controlled servers. **DNSSEC** prevents this by validating cryptographic signatures on DNS responses.

## What is the Kaminsky attack?
A sophisticated DNS cache poisoning attack discovered by Dan Kaminsky in 2008 that exploited predictable DNS transaction IDs. Mitigation: **source port randomization** (RFC 5452) and **DNSSEC**.

## What is negative caching?
Caching **NXDOMAIN** (non-existent domain) responses to avoid repeated queries for domains that don't exist. Cached for the duration of the **Minimum TTL** in the SOA record.

## What is the recommended TTL for DNS records under normal operation?
- **Production records**: 3600s (1 hour) to 86400s (24 hours) is common
- **Before a planned change**: Lower to 300s (5 minutes) at least an hour before
- **After a change**: Restore to normal TTL once propagation is confirmed
- **Time-sensitive records** (failover): 60–300 seconds

## How do you check what's cached in systemd-resolved?
```bash
sudo systemd-resolve --statistics
# or check individual lookups
systemd-resolve --no-pager example.com
```

## What is resolver-side caching vs authoritative-side caching?
- **Resolver-side**: Caches responses from authoritative servers up to the record TTL
- **Authoritative-side**: Does not cache (it IS the source of truth). Some providers use CDN-like edge caches to reduce load.

## What tools can show DNS lookup times (to detect caching)?
```bash
dig example.com          # Shows query time in milliseconds
dig +norecurse example.com @8.8.8.8  # Direct query to resolver
# Cached response: <10ms; uncached: 50-500ms
```

## What is DNS prefetching?
Browsers resolve DNS names **speculatively** before a user clicks a link, storing results in the browser cache. Controlled via `<link rel="dns-prefetch" href="//example.com">` or browser settings.

## What does a TTL of 0 mean?
A TTL of 0 means the record should **not be cached** — every request goes to the authoritative server. Used for highly dynamic records, though it can severely increase DNS load and latency.
