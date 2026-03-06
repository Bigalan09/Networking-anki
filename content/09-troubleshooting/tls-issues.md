# TLS/SSL Troubleshooting

## Scenario: Browser shows "NET::ERR_CERT_AUTHORITY_INVALID". What does this mean?
The server's TLS certificate is **not trusted by the browser** because:
- Self-signed certificate (not issued by a trusted CA)
- Certificate issued by an internal/private CA not in the browser's trust store
- Root certificate expired

Fix: Use a certificate from a publicly trusted CA (Let's Encrypt, DigiCert, etc.) or install the internal CA certificate.

## Scenario: Browser shows "NET::ERR_CERT_DATE_INVALID". What is the cause?
The TLS certificate has **expired** (or is not yet valid). Check:
```bash
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
# notBefore and notAfter dates
```
Fix: Renew the certificate. Enable auto-renewal (certbot, cert-manager).

## What tools are used to debug TLS issues?
```bash
# Check certificate details
openssl s_client -connect example.com:443 -servername example.com

# Check certificate expiry
echo Q | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Check certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check supported TLS versions
nmap --script ssl-enum-ciphers -p 443 example.com

# Using curl with verbose TLS output
curl -v https://example.com
```

## Scenario: `curl: (60) SSL certificate problem: unable to get local issuer certificate`. What is the issue?
The **certificate chain is incomplete** — the server is not sending the intermediate certificate(s). The client can't build a chain to a trusted root CA.

Fix: Configure the server to send the **full certificate chain** (leaf certificate + all intermediate certificates, in order).

## What is SNI (Server Name Indication)?
A TLS extension that allows the **client to specify the hostname** during the TLS handshake (before the certificate is sent). This allows multiple TLS sites on the same IP/port.

Without SNI, the server can only serve one certificate per IP address.

```bash
# Test with SNI
openssl s_client -connect 203.0.113.1:443 -servername example.com
```

## Scenario: HTTPS works in browser but curl fails with certificate error. What might be wrong?
The server may be checking the **`Host` header or SNI** to select a certificate, and curl isn't sending SNI properly. Or:
- The system CA bundle used by curl is outdated
- A corporate MITM proxy is intercepting TLS with a certificate not in the system trust store

## What is a TLS handshake timeout?
The TLS handshake takes too long (due to slow server, firewall blocking, or misconfigured DH parameters). Check:
- Server CPU overload
- Firewall blocking return traffic
- Use TLS 1.3 (faster handshake than TLS 1.2)

## What is certificate pinning?
A security mechanism where an app **only accepts a specific certificate or public key** (not just any trusted CA). If the certificate changes (rotation or MITM), the connection fails. Common in mobile apps.

## What is mutual TLS (mTLS)?
Both the client and server present certificates to authenticate each other. Used in:
- Service-to-service authentication (microservices)
- API authentication
- Zero-trust network access

## Scenario: Let's Encrypt certificate renewal fails. What do you check?
1. **Port 80 accessible**: HTTP-01 challenge requires port 80 open to internet
2. **DNS propagation**: DNS-01 challenge requires correct TXT record
3. **Domain validation**: Does the domain resolve to the server? (`dig example.com`)
4. **Certbot logs**: `/var/log/letsencrypt/letsencrypt.log`
5. **Rate limits**: Let's Encrypt has rate limits (5 certs per domain per week)

## What TLS versions should you support?
- **TLS 1.3**: Preferred — use wherever possible
- **TLS 1.2**: Required for compatibility with older clients
- **TLS 1.1**: Deprecated — disable
- **TLS 1.0**: Deprecated — disable
- **SSLv3**: Critically broken (POODLE) — must disable

## What is HSTS (HTTP Strict Transport Security)?
A header that tells browsers to **always use HTTPS** for the domain:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
Prevents downgrade attacks. After the first HTTPS visit, the browser won't try HTTP.

## What is certificate transparency (CT)?
A public log of all TLS certificates issued by CAs. Allows detection of misissued or unauthorized certificates. Browsers require CT logging for trusted certificates.
