# Ports and Service Identification

## What is a network port?
A **16-bit number** (0–65535) used to identify a specific process or service on a host. Combined with an IP address, a port forms a **socket**. Ports allow a single host to run multiple network services simultaneously.

## What are the three ranges of port numbers?
- **Well-known ports**: 0–1023 (assigned by IANA, require root/admin to bind)
- **Registered ports**: 1024–49151 (registered with IANA for specific services)
- **Dynamic/Ephemeral ports**: 49152–65535 (used by clients for source ports)

## What are the most important well-known port numbers?

| Port | Protocol | Service         |
|------|----------|-----------------|
| 20   | TCP      | FTP (data)      |
| 21   | TCP      | FTP (control)   |
| 22   | TCP      | SSH             |
| 23   | TCP      | Telnet          |
| 25   | TCP      | SMTP            |
| 53   | TCP/UDP  | DNS             |
| 67   | UDP      | DHCP (server)   |
| 68   | UDP      | DHCP (client)   |
| 69   | UDP      | TFTP            |
| 80   | TCP      | HTTP            |
| 110  | TCP      | POP3            |
| 123  | UDP      | NTP             |
| 143  | TCP      | IMAP            |
| 161  | UDP      | SNMP            |
| 162  | UDP      | SNMP Trap       |
| 389  | TCP/UDP  | LDAP            |
| 443  | TCP      | HTTPS           |
| 445  | TCP      | SMB/CIFS        |
| 465  | TCP      | SMTPS           |
| 514  | UDP      | Syslog          |
| 587  | TCP      | SMTP submission |
| 636  | TCP      | LDAPS           |
| 993  | TCP      | IMAPS           |
| 995  | TCP      | POP3S           |
| 3306 | TCP      | MySQL           |
| 3389 | TCP      | RDP             |
| 5432 | TCP      | PostgreSQL      |
| 6443 | TCP      | Kubernetes API  |
| 8080 | TCP      | HTTP alt        |
| 8443 | TCP      | HTTPS alt       |

## What is an ephemeral port?
A **temporary, short-lived** source port assigned by the OS to a client for the duration of a connection. After the connection closes, the port is returned to the pool. Range typically 49152–65535 (Linux default: 32768–60999).

## What is a socket?
The combination of an **IP address + port number** (e.g., `192.168.1.5:443`). A **socket pair** (source socket + destination socket) uniquely identifies a network connection.

## What command shows open ports on Linux?
```bash
ss -tlnp      # Show TCP listening ports with PID
netstat -tlnp  # Alternative (older)
lsof -i :80   # Show what's using port 80
```

## What command shows open ports on Windows?
```cmd
netstat -an   # Show all connections and listening ports
netstat -ano  # Include PID
```

## What is port scanning?
A technique to discover which ports on a host are open (have a listening service). **Nmap** is the most common tool:
```bash
nmap -sV 192.168.1.1        # Version scan
nmap -p 1-1000 192.168.1.1  # Scan specific port range
```

## What is the difference between a service port and a dynamic port?
- **Service/listening port**: A fixed port on which a server waits for incoming connections (e.g., port 443 for HTTPS)
- **Dynamic/ephemeral port**: A randomly chosen port on the **client side** used as the source port for a connection

## What is port forwarding?
A NAT technique that redirects traffic arriving at a specific port on a router to a different internal host:port. Allows external access to services on private IP addresses.

## What is a firewall rule based on ports?
Firewall rules filter traffic by **port number** (and protocol). Example: `ALLOW TCP 443 INBOUND` permits HTTPS traffic. `DENY TCP 23 INBOUND` blocks Telnet.

## What port does RDP use and why is it a security concern?
**Port 3389 (TCP)**. RDP is a frequent target for:
- Brute-force attacks
- BlueKeep and other RDP vulnerabilities
- Should never be exposed directly to the internet without VPN or firewall restriction

## What is a well-known port below 1024 for database replication?
MySQL uses **3306** (above 1024). There are no commonly-used database ports below 1024. The key insight: ports below 1024 require **elevated privileges** to bind, providing a security boundary.
