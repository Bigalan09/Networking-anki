"""
Tests for build_anki.py — Anki deck building logic.
"""

import sys
import textwrap
from pathlib import Path

import pytest

# Allow importing from scripts/
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from build_anki import (
    CONTENT_DIR,
    build_category_deck,
    build_deck_from_file,
    make_note_id,
    markdown_to_html,
    parse_markdown_file,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_md(content: str, tmp_path: Path) -> Path:
    f = tmp_path / "test.md"
    f.write_text(textwrap.dedent(content), encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# parse_markdown_file tests
# ---------------------------------------------------------------------------


class TestParseMarkdownFile:
    def test_basic_parse(self, tmp_path):
        md = make_md(
            """\
            # My Deck

            ## Card Front
            Card back content here.
            """,
            tmp_path,
        )
        deck_name, cards = parse_markdown_file(md)
        assert deck_name == "My Deck"
        assert len(cards) == 1
        assert cards[0][0] == "Card Front"
        assert "Card back content here" in cards[0][1]

    def test_multiple_cards(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## Q1
            Answer 1.

            ## Q2
            Answer 2.
            """,
            tmp_path,
        )
        _name, cards = parse_markdown_file(md)
        assert len(cards) == 2

    def test_no_deck_name_defaults(self, tmp_path):
        md = make_md(
            """\
            ## Q1
            Answer 1.
            """,
            tmp_path,
        )
        deck_name, _cards = parse_markdown_file(md)
        assert deck_name == "Networking"

    def test_empty_back_card_excluded(self, tmp_path):
        md = make_md(
            """\
            # Deck

            ## Q with back
            Actual content.

            ## Q without back
            """,
            tmp_path,
        )
        _name, cards = parse_markdown_file(md)
        # Only the card with actual back content should be included
        assert len(cards) == 1
        assert cards[0][0] == "Q with back"


# ---------------------------------------------------------------------------
# markdown_to_html tests
# ---------------------------------------------------------------------------


class TestMarkdownToHtml:
    def test_bold_conversion(self):
        html = markdown_to_html("**bold text**")
        assert "<strong>bold text</strong>" in html

    def test_italic_conversion(self):
        html = markdown_to_html("*italic text*")
        assert "<em>italic text</em>" in html

    def test_inline_code(self):
        html = markdown_to_html("`some code`")
        assert "<code>some code</code>" in html

    def test_code_block(self):
        text = "```bash\nnginx -t\n```"
        html = markdown_to_html(text)
        assert "<pre>" in html
        assert "nginx -t" in html

    def test_table_conversion(self):
        text = "| Port | Service |\n|------|---------||\n| 80   | HTTP    |\n"
        html = markdown_to_html(text)
        assert "<table>" in html
        assert "<th>" in html
        assert "HTTP" in html

    def test_html_entities_escaped_in_code(self):
        text = "```\n<script>alert(1)</script>\n```"
        html = markdown_to_html(text)
        assert "<script>" not in html
        assert "&lt;script&gt;" in html

    def test_list_items(self):
        text = "- Item one\n- Item two"
        html = markdown_to_html(text)
        assert "<li>Item one</li>" in html
        assert "<li>Item two</li>" in html

    def test_heading_conversion(self):
        html = markdown_to_html("### Subheading")
        assert "<h3>Subheading</h3>" in html


# ---------------------------------------------------------------------------
# make_note_id tests
# ---------------------------------------------------------------------------


class TestMakeNoteId:
    def test_deterministic(self):
        id1 = make_note_id("Deck A", "Front text")
        id2 = make_note_id("Deck A", "Front text")
        assert id1 == id2

    def test_different_decks_different_ids(self):
        id1 = make_note_id("Deck A", "Same front")
        id2 = make_note_id("Deck B", "Same front")
        assert id1 != id2

    def test_different_fronts_different_ids(self):
        id1 = make_note_id("Deck", "Front A")
        id2 = make_note_id("Deck", "Front B")
        assert id1 != id2

    def test_returns_integer(self):
        note_id = make_note_id("Deck", "Front")
        assert isinstance(note_id, int)


# ---------------------------------------------------------------------------
# build_deck_from_file tests
# ---------------------------------------------------------------------------


class TestBuildDeckFromFile:
    def test_builds_deck(self, tmp_path):
        md = make_md(
            """\
            # Test Deck

            ## What is a subnet?
            A subdivision of an IP network.

            ## What is CIDR?
            Classless Inter-Domain Routing.
            """,
            tmp_path,
        )
        deck = build_deck_from_file(md)
        assert deck is not None
        assert deck.name == "Test Deck"
        assert len(deck.notes) == 2

    def test_empty_file_returns_none(self, tmp_path):
        md = tmp_path / "empty.md"
        md.write_text("# Empty Deck\n\nNo cards here.\n")
        deck = build_deck_from_file(md)
        assert deck is None

    def test_deterministic_deck_id(self, tmp_path):
        md = make_md(
            """\
            # Stable Deck

            ## Q?
            Answer.
            """,
            tmp_path,
        )
        deck1 = build_deck_from_file(md)
        deck2 = build_deck_from_file(md)
        assert deck1 is not None
        assert deck2 is not None
        assert deck1.deck_id == deck2.deck_id


# ---------------------------------------------------------------------------
# build_category_deck tests
# ---------------------------------------------------------------------------


class TestBuildCategoryDeck:
    def test_builds_combined_deck(self, tmp_path):
        cat_dir = tmp_path / "01-test-category"
        cat_dir.mkdir()
        (cat_dir / "file1.md").write_text(
            "# File 1\n\n## Q1?\nAnswer 1.\n\n## Q2?\nAnswer 2.\n"
        )
        (cat_dir / "file2.md").write_text(
            "# File 2\n\n## Q3?\nAnswer 3.\n"
        )

        deck = build_category_deck(cat_dir)
        assert deck is not None
        assert len(deck.notes) == 3

    def test_empty_category_returns_none(self, tmp_path):
        cat_dir = tmp_path / "empty-category"
        cat_dir.mkdir()
        deck = build_category_deck(cat_dir)
        assert deck is None


# ---------------------------------------------------------------------------
# Integration: build from real content files
# ---------------------------------------------------------------------------


class TestBuildFromRealContent:
    def test_build_all_category_decks(self, tmp_path):
        """Build all category decks from real content and verify they contain cards."""
        category_dirs = sorted(d for d in CONTENT_DIR.iterdir() if d.is_dir())
        assert category_dirs, "No category directories found"

        total_cards = 0
        for cat_dir in category_dirs:
            deck = build_category_deck(cat_dir)
            assert deck is not None, f"Failed to build deck for {cat_dir.name}"
            assert len(deck.notes) > 0, f"Deck for {cat_dir.name} has no notes"
            total_cards += len(deck.notes)

        assert total_cards >= 200, (
            f"Expected at least 200 cards total, got {total_cards}"
        )

    def test_write_apkg_files(self, tmp_path):
        """Verify that .apkg files can be written without errors."""
        import genanki

        category_dirs = sorted(d for d in CONTENT_DIR.iterdir() if d.is_dir())
        for cat_dir in category_dirs[:2]:  # Test with first 2 categories
            deck = build_category_deck(cat_dir)
            if deck:
                out = tmp_path / f"{cat_dir.name}.apkg"
                pkg = genanki.Package(deck)
                pkg.write_to_file(str(out))
                assert out.exists(), f"Expected .apkg file at {out}"
                assert out.stat().st_size > 0, f".apkg file is empty: {out}"
