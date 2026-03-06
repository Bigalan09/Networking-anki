# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2026-03-06

### Added

- **595+ networking flashcards** covering nine topic categories:
  - 01 - Networking Fundamentals (IPv4, IPv6, subnetting, CIDR)
  - 02 - Subnetting Mastery (/16–/30 calculations, host counts)
  - 03 - Protocols (TCP, UDP, ports, ICMP, ARP, DHCP)
  - 04 - DNS Architecture (resolvers, record types, caching, split-horizon)
  - 05 - Switching & VLANs (segmentation, trunk/access ports, inter-VLAN routing)
  - 06 - VPN Architecture (WireGuard, Tailscale, subnet routers, exit nodes)
  - 07 - Modern Infrastructure (Docker, Kubernetes, reverse proxies, Traefik, Nginx)
  - 08 - Infrastructure Engineering (IaC, Ansible, Terraform, Prometheus, Grafana)
  - 09 - Troubleshooting (DHCP, DNS, TLS, VLAN, container networking scenarios)
- `build_anki.py` script to convert markdown flashcards into `.apkg` Anki packages
- `validate_cards.py` script to check card format, detect duplicates, and verify structure
- GitHub Actions workflow for PR validation (lint + test on every pull request)
- GitHub Actions workflow for tag-based releases (builds and publishes `.apkg` files)
- Unit and integration test suite (`pytest`)
