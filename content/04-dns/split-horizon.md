# Split Horizon DNS

## What is split-horizon DNS?
**Split-horizon DNS** (also called split-brain DNS) is a configuration where the **same domain name returns different DNS records** depending on where the query originates (e.g., internal vs. external network).

## Why is split-horizon DNS used?
- **Internal access**: Return private IP addresses for internal services when queried from inside the network
- **External access**: Return public IP addresses for the same services when queried from the internet
- **Security**: Hide internal network topology from external users
- **Performance**: Direct internal clients to internal resources (avoiding hairpin NAT)

## Give a real-world example of split-horizon DNS
`api.example.com`:
- **Internal DNS** returns `10.0.1.50` (private server IP)
- **External DNS** returns `203.0.113.100` (public IP/load balancer)

Internal users go directly to the server. External users go through the load balancer/firewall.

## What is hairpin NAT (NAT hairpinning)?
When an internal client uses a domain's **public IP** (returned by external DNS) to reach an internal server, the traffic goes: client → router (NAT) → server on same network. This is inefficient and sometimes breaks. Split-horizon DNS avoids this.

## How is split-horizon DNS implemented with BIND?
Using **views** in `named.conf`:
```
view "internal" {
    match-clients { 10.0.0.0/8; 192.168.0.0/16; };
    zone "example.com" {
        type master;
        file "internal.example.com.zone";
    };
};
view "external" {
    match-clients { any; };
    zone "example.com" {
        type master;
        file "external.example.com.zone";
    };
};
```

## How is split-horizon DNS implemented with CoreDNS?
Use separate **corefile blocks** or plugins:
```
example.com {
    # Serve different responses based on source
    rewrite name regex (.*).internal.example.com {1}.example.com
    forward . 10.0.0.1
}
```

## What are the challenges of split-horizon DNS?
1. **Maintaining two zone files**: Changes must be made in both places
2. **Testing complexity**: Hard to test external responses from inside the network
3. **DNSSEC complications**: Signing different zones for the same name is complex
4. **Email delivery**: SPF, DKIM records need to be consistent in external view

## How does Kubernetes implement split-horizon DNS?
CoreDNS (Kubernetes default DNS) serves `cluster.local` domain internally. Services get internal DNS names like `my-service.namespace.svc.cluster.local` that resolve to ClusterIP addresses — inaccessible externally.

## What is a DNS view in AWS Route 53?
AWS Route 53 supports **private hosted zones** associated with specific VPCs. The same domain can have a public hosted zone (for internet) and a private hosted zone (for VPC internal traffic) — implementing split-horizon DNS natively.

## What is the difference between split-horizon and split-brain DNS?
These terms are often used **interchangeably**. Technically:
- **Split-horizon**: Same server, different answers based on source
- **Split-brain**: Separate, isolated DNS systems for internal and external (more extreme separation)

## How do you test that split-horizon DNS is working correctly?
```bash
# Query internal DNS from inside
dig @10.0.0.1 api.example.com  # Should return private IP

# Query external DNS from inside (simulate external)
dig @8.8.8.8 api.example.com   # Should return public IP

# Compare results
```

## What security consideration is important for split-horizon DNS?
**Prevent internal records from leaking to external DNS**. Ensure:
- Zone transfers are restricted (`allow-transfer { none; };` for external zones)
- Internal nameservers are not publicly reachable
- DNS firewall rules block external queries to internal resolvers
