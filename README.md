# Networking-anki

A comprehensive Anki flashcard repository for mastering networking — from beginner fundamentals through to production infrastructure engineering.

## Contents

| Category | Topics |
|----------|--------|
| [01 - Networking Fundamentals](content/01-networking-fundamentals/) | IPv4, IPv6, subnetting, CIDR, network/broadcast, gateways |
| [02 - Subnetting Mastery](content/02-subnetting-mastery/) | /16–/30 calculations, host counts, mental subnetting |
| [03 - Protocols](content/03-protocols/) | TCP, UDP, ports, service identification, ICMP, ARP, DHCP |
| [04 - DNS Architecture](content/04-dns/) | Resolvers, authoritative servers, A/AAAA/CNAME/MX/TXT, caching, split-horizon |
| [05 - Switching & VLANs](content/05-switching-vlans/) | VLAN segmentation, trunk vs access ports, inter-VLAN routing |
| [06 - VPN Architecture](content/06-vpn/) | VPN fundamentals, WireGuard, Tailscale, subnet routers, exit nodes |
| [07 - Modern Infrastructure](content/07-modern-infrastructure/) | Docker, Kubernetes, reverse proxies, Traefik, Nginx, scaling patterns |
| [08 - Infrastructure Engineering](content/08-infrastructure-engineering/) | IaC, Ansible, Terraform, observability, Prometheus, Grafana |
| [09 - Troubleshooting](content/09-troubleshooting/) | DHCP, DNS, TLS, VLAN, container networking, reverse proxy, VPN scenarios |

**Total: 595+ flashcards**

---

## Repository Structure

```
Networking-anki/
├── content/                    # Flashcard source files (markdown)
│   ├── 01-networking-fundamentals/
│   ├── 02-subnetting-mastery/
│   ├── 03-protocols/
│   ├── 04-dns/
│   ├── 05-switching-vlans/
│   ├── 06-vpn/
│   ├── 07-modern-infrastructure/
│   ├── 08-infrastructure-engineering/
│   └── 09-troubleshooting/
├── scripts/
│   ├── build_anki.py           # Converts markdown → .apkg Anki packages
│   ├── validate_cards.py       # Validates cards for duplicates and format
│   └── requirements.txt        # Python dependencies
├── tests/
│   ├── test_validate.py        # Tests for validate_cards.py
│   └── test_build.py           # Tests for build_anki.py
└── README.md
```

---

## Markdown Card Format

Each markdown file represents a topic. The format is:

```markdown
# Deck Name   ← becomes the Anki deck name

## Front of card (question)
Back of card (answer) — supports **bold**, *italic*, `inline code`,
code blocks, tables, and lists.

## Another question
Another answer.
```

- The **H1 heading** (`#`) is the deck name
- Each **H2 heading** (`##`) is the **front** of an Anki card
- The content below each H2 (until the next H2) is the **back** of the card

---

## Building Anki Decks

### Prerequisites

```bash
pip install -r scripts/requirements.txt
```

### Build all decks

```bash
python scripts/build_anki.py
```

Outputs `.apkg` files to `output/` — one file per category.

### Build a combined deck

```bash
python scripts/build_anki.py --combined
```

This creates `output/networking-all.apkg` in addition to the per-category files.

### Build from specific files

```bash
python scripts/build_anki.py content/01-networking-fundamentals/ipv4-ipv6.md
```

### Import into Anki

1. Open Anki
2. `File → Import`
3. Select one of the generated `.apkg` files
4. Click Import

---

## Validation

Run the validator to check all cards for quality issues:

```bash
python scripts/validate_cards.py
```

With verbose output (shows passing files too):

```bash
python scripts/validate_cards.py --verbose
```

The validator checks for:
- ✓ Every file has an H1 heading (deck name)
- ✓ Every card has a non-empty back
- ✓ No duplicate card fronts within a file
- ✓ No duplicate card fronts across the entire repository
- ✓ Card backs are at least 5 characters long
- ✓ Every category has the expected markdown files

---

## Running Tests

```bash
pip install -r scripts/requirements.txt
python -m pytest tests/ -v
```

Tests cover:
- Unit tests for the markdown parser
- Unit tests for HTML conversion
- Unit tests for the Anki deck builder
- Integration tests against all real content files (validate card count, format, duplicates)

---

## Adding New Cards

1. Open the relevant markdown file in `content/`
2. Add a new `## Your question?` section with the answer below it
3. Run the validator: `python scripts/validate_cards.py`
4. Rebuild the deck: `python scripts/build_anki.py`

To add a **new topic**:
1. Create a new markdown file in the appropriate category directory
2. Follow the markdown format above
3. Validate and rebuild