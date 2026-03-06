# DNS Misconfiguration Troubleshooting

## Scenario: A website is accessible by IP but not by domain name. What is the issue?
This is a **DNS resolution failure**. The domain is not resolving to the correct IP (or at all).

Steps:
1. `nslookup example.com` or `dig example.com` — check what IP is returned
2. Check if correct A record exists at the authoritative nameserver
3. Check TTL — might be serving a cached wrong answer
4. `dig +trace example.com` — trace the full resolution path

## What tools are used to diagnose DNS issues?

| Tool | Use |
|------|-----|
| `dig` | Detailed DNS query tool (preferred) |
| `nslookup` | Basic DNS queries |
| `host` | Simple DNS lookups |
| `drill` | Similar to dig |
| `resolvectl` | Query systemd-resolved |
| `tcpdump -i eth0 port 53` | Capture DNS traffic |
| `whois` | Check domain registration and NS records |

## Scenario: `dig example.com` returns NXDOMAIN but the domain exists. What do you check?
1. Check the **authoritative nameserver** directly: `dig @ns1.example.com example.com`
2. Check if the A record exists in the zone file
3. Check for typos in the domain name
4. Check if there's a negative cache hit: `dig example.com` shows `ANSWER: 0` with SOA in Authority section — wait for negative TTL

## What is the difference between NXDOMAIN and SERVFAIL?
- **NXDOMAIN**: The domain does not exist
- **SERVFAIL**: The nameserver encountered an error processing the query (misconfigured zone, DNSSEC failure, unreachable nameserver)

## Scenario: Internal services are resolving to external IPs from inside the network. What is the cause?
Missing or misconfigured **split-horizon DNS**. The internal DNS server doesn't have a zone for the domain, so it forwards to external DNS which returns the public IP.

Fix: Create an internal DNS zone for the domain with correct internal IP records.

## Scenario: DNS changes are not propagating. What do you check?
1. Was the change made on the **primary nameserver**?
2. What is the **TTL** of the old record? Resolvers cache until TTL expires.
3. Did the **SOA serial number increment**? Secondary servers check serial before doing zone transfers.
4. Are secondary nameservers updated? (`dig @ns2.example.com example.com`)
5. Did you modify the correct zone? (e.g., typo in zone name)

## What causes a DNS loop?
Circular CNAME chains (A → B → C → A) or a forwarder pointing to itself. Resolvers detect loops after a maximum number of CNAME follow-throughs and return SERVFAIL.

## Scenario: Email is not being delivered to a domain. How do you check DNS?
1. `dig MX example.com` — verify MX records exist and point to correct mail servers
2. `dig A mail.example.com` — verify MX target resolves to correct IP
3. `dig TXT example.com` — check SPF record (`v=spf1 ...`)
4. Check DMARC: `dig TXT _dmarc.example.com`
5. Check DKIM: `dig TXT <selector>._domainkey.example.com`

## Scenario: Kubernetes pods can't resolve external hostnames. What do you check?
1. Check CoreDNS pods are running: `kubectl get pods -n kube-system | grep coredns`
2. Check CoreDNS logs: `kubectl logs -n kube-system -l k8s-app=kube-dns`
3. Test from a pod: `kubectl run debug --image=busybox --rm -it -- nslookup google.com`
4. Check CoreDNS configmap: `kubectl get configmap coredns -n kube-system -o yaml`
5. Check node DNS: Are nodes resolving correctly? CoreDNS forwards to node DNS.

## Scenario: DNS resolution is intermittently slow. What are potential causes?
1. **DNS server overloaded**: Check CPU/memory on resolver
2. **High query rate**: Application not caching DNS responses
3. **Long CNAME chains**: Each CNAME is an extra lookup
4. **Round-trip latency**: Using a distant resolver; switch to a closer one or run a local cache (unbound, dnsmasq)
5. **DNS packet fragmentation**: EDNS0 large responses fragmented; check with `dig +bufsize=512 example.com`
6. **DNSSEC validation failures**: Slow validation chain

## What is a DNS rebinding attack?
An attacker controls DNS for a domain and initially returns their server's IP. After the browser caches it, they change the DNS to return an internal IP address (`192.168.x.x`). The browser now sends requests "to the attacker's domain" but they land on an internal server.

Mitigation: DNS rebinding protection in resolvers (reject private IPs for public domains).
