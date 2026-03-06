"""
Tests for validate_cards.py — card validation logic.
"""

import sys
import textwrap
from pathlib import Path

import pytest

# Allow importing from scripts/
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate_cards import (
    CONTENT_DIR,
    MIN_BACK_LENGTH,
    find_markdown_files,
    parse_cards,
    validate_all_files,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_md(content: str, tmp_path: Path) -> Path:
    """Write markdown content to a temp file and return its path."""
    f = tmp_path / "test.md"
    f.write_text(textwrap.dedent(content), encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# parse_cards unit tests
# ---------------------------------------------------------------------------


class TestParseCards:
    def test_basic_card(self, tmp_path):
        md = make_md(
            """\
            # Test Deck

            ## What is TCP?
            TCP is a reliable transport protocol.
            """,
            tmp_path,
        )
        deck_name, cards, errors = parse_cards(md)
        assert deck_name == "Test Deck"
        assert len(cards) == 1
        assert cards[0][0] == "What is TCP?"
        assert "reliable transport protocol" in cards[0][1]
        assert errors == []

    def test_multiple_cards(self, tmp_path):
        md = make_md(
            """\
            # Protocols

            ## What is TCP?
            Transmission Control Protocol — reliable.

            ## What is UDP?
            User Datagram Protocol — unreliable.

            ## What is ICMP?
            Internet Control Message Protocol.
            """,
            tmp_path,
        )
        _deck, cards, errors = parse_cards(md)
        assert len(cards) == 3
        assert errors == []
        fronts = [c[0] for c in cards]
        assert "What is TCP?" in fronts
        assert "What is UDP?" in fronts
        assert "What is ICMP?" in fronts

    def test_missing_deck_name(self, tmp_path):
        md = make_md(
            """\
            ## What is TCP?
            TCP is reliable.
            """,
            tmp_path,
        )
        deck_name, _cards, errors = parse_cards(md)
        assert deck_name is None
        assert any("H1" in e or "deck name" in e.lower() for e in errors)

    def test_empty_card_back(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## Question with no back

            ## Another question
            This one has a back.
            """,
            tmp_path,
        )
        _deck, _cards, errors = parse_cards(md)
        assert any("Empty card back" in e for e in errors)

    def test_duplicate_fronts_within_file(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## Same question?
            First answer.

            ## Same question?
            Second answer.
            """,
            tmp_path,
        )
        _deck, _cards, errors = parse_cards(md)
        assert any("Duplicate card front" in e for e in errors)

    def test_card_back_too_short(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## What is X?
            Hi
            """,
            tmp_path,
        )
        _deck, _cards, errors = parse_cards(md)
        # "Hi" is 2 chars < MIN_BACK_LENGTH
        assert any("too short" in e for e in errors)

    def test_no_cards(self, tmp_path):
        md = make_md(
            """\
            # Deck with no cards
            Just some text, no H2 headings.
            """,
            tmp_path,
        )
        _deck, cards, errors = parse_cards(md)
        assert cards == []
        assert any("No cards" in e for e in errors)

    def test_cards_with_code_block(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## How do you bring up WireGuard?
            Use wg-quick:
            ```bash
            wg-quick up wg0
            ```
            """,
            tmp_path,
        )
        _deck, cards, errors = parse_cards(md)
        assert len(cards) == 1
        assert errors == []
        assert "wg-quick" in cards[0][1]

    def test_cards_with_table(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## What are the TCP flags?
            | Flag | Meaning  |
            |------|----------|
            | SYN  | Sync     |
            | ACK  | Ack      |
            """,
            tmp_path,
        )
        _deck, cards, errors = parse_cards(md)
        assert len(cards) == 1
        assert errors == []


# ---------------------------------------------------------------------------
# validate_all_files unit tests
# ---------------------------------------------------------------------------


class TestValidateAllFiles:
    def test_valid_files(self, tmp_path):
        f1 = tmp_path / "a.md"
        f1.write_text("# Deck A\n\n## Q1?\nAnswer one.\n\n## Q2?\nAnswer two.\n")
        f2 = tmp_path / "b.md"
        f2.write_text("# Deck B\n\n## Q3?\nAnswer three.\n\n## Q4?\nAnswer four.\n")

        n_files, n_cards, n_errors = validate_all_files([f1, f2])
        assert n_files == 2
        assert n_cards == 4
        assert n_errors == 0

    def test_cross_file_duplicates(self, tmp_path):
        f1 = tmp_path / "a.md"
        f1.write_text("# Deck A\n\n## Same question?\nFirst answer.\n")
        f2 = tmp_path / "b.md"
        f2.write_text("# Deck B\n\n## Same question?\nSecond answer.\n")

        _n_files, _n_cards, n_errors = validate_all_files([f1, f2])
        assert n_errors > 0

    def test_case_insensitive_duplicate_detection(self, tmp_path):
        f1 = tmp_path / "a.md"
        f1.write_text("# Deck A\n\n## What is TCP?\nAnswer one.\n")
        f2 = tmp_path / "b.md"
        f2.write_text("# Deck B\n\n## what is tcp?\nAnswer two.\n")

        _n_files, _n_cards, n_errors = validate_all_files([f1, f2])
        assert n_errors > 0


# ---------------------------------------------------------------------------
# Integration tests against the real content directory
# ---------------------------------------------------------------------------


class TestRealContentFiles:
    def test_content_directory_exists(self):
        assert CONTENT_DIR.exists(), f"Content directory not found: {CONTENT_DIR}"

    def test_content_directory_has_markdown_files(self):
        files = find_markdown_files(CONTENT_DIR)
        assert len(files) > 0, "No markdown files found in content/"

    def test_all_categories_present(self):
        categories = {d.name for d in CONTENT_DIR.iterdir() if d.is_dir()}
        required_prefixes = [
            "01-networking-fundamentals",
            "02-subnetting-mastery",
            "03-protocols",
            "04-dns",
            "05-switching-vlans",
            "06-vpn",
            "07-modern-infrastructure",
            "08-infrastructure-engineering",
            "09-troubleshooting",
        ]
        for prefix in required_prefixes:
            assert any(c.startswith(prefix) for c in categories), (
                f"Missing category directory starting with: {prefix}"
            )

    def test_minimum_card_count(self):
        files = find_markdown_files(CONTENT_DIR)
        total_cards = 0
        for f in files:
            _, cards, _ = parse_cards(f)
            total_cards += len(cards)
        # We expect at least 200 cards across all files
        assert total_cards >= 200, (
            f"Expected at least 200 cards total, got {total_cards}"
        )

    def test_all_real_files_pass_validation(self):
        files = find_markdown_files(CONTENT_DIR)
        assert files, "No markdown files found"
        _n_files, _n_cards, n_errors = validate_all_files(files)
        assert n_errors == 0, (
            f"Validation failed with {n_errors} error(s) — "
            "run 'python scripts/validate_cards.py' for details"
        )

    def test_each_file_has_deck_name(self):
        files = find_markdown_files(CONTENT_DIR)
        for f in files:
            deck_name, _cards, _errors = parse_cards(f)
            assert deck_name is not None, f"{f} is missing an H1 heading (deck name)"

    def test_each_file_has_cards(self):
        files = find_markdown_files(CONTENT_DIR)
        for f in files:
            _deck, cards, _errors = parse_cards(f)
            assert len(cards) > 0, f"{f} has no cards"

    @pytest.mark.parametrize(
        "category,min_files",
        [
            ("01-networking-fundamentals", 4),
            ("02-subnetting-mastery", 2),
            ("03-protocols", 4),
            ("04-dns", 4),
            ("05-switching-vlans", 3),
            ("06-vpn", 4),
            ("07-modern-infrastructure", 5),
            ("08-infrastructure-engineering", 5),
            ("09-troubleshooting", 5),
        ],
    )
    def test_category_file_count(self, category, min_files):
        cat_dir = CONTENT_DIR / category
        assert cat_dir.exists(), f"Category directory not found: {cat_dir}"
        md_files = list(cat_dir.glob("*.md"))
        assert len(md_files) >= min_files, (
            f"{category} has {len(md_files)} files, expected at least {min_files}"
        )
