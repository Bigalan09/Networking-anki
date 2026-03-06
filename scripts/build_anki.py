#!/usr/bin/env python3
"""
build_anki.py — Convert markdown flashcard files into Anki packages (.apkg).

Markdown format expected:
    # Deck Name (first H1 = deck name)

    ## Front of card
    Back of card content (everything until the next ## or end of file)

Usage:
    python scripts/build_anki.py                        # Build all decks
    python scripts/build_anki.py --output ./output      # Custom output dir
    python scripts/build_anki.py content/01-networking-fundamentals/ipv4-ipv6.md
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

import genanki

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"

# Deterministic model ID derived from a fixed seed so decks remain
# compatible across rebuilds.
MODEL_ID = int(hashlib.md5(b"networking-anki-basic-model-v1").hexdigest()[:8], 16)

ANKI_MODEL = genanki.Model(
    MODEL_ID,
    "Networking Basic",
    fields=[
        {"name": "Front"},
        {"name": "Back"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": "{{FrontSide}}<hr id=answer>{{Back}}",
        }
    ],
    css="""
.card {
    font-family: Arial, sans-serif;
    font-size: 16px;
    text-align: left;
    color: #1a1a1a;
    background-color: #ffffff;
    padding: 20px;
    line-height: 1.6;
}
code, pre {
    font-family: 'Courier New', monospace;
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 14px;
}
pre {
    display: block;
    padding: 12px;
    overflow-x: auto;
    white-space: pre-wrap;
}
table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
th {
    background-color: #f0f0f0;
}
""",
)


def parse_markdown_file(filepath: Path) -> tuple[str, list[tuple[str, str]]]:
    """
    Parse a markdown file into a deck name and a list of (front, back) card tuples.

    Returns:
        (deck_name, [(front, back), ...])
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    deck_name = "Networking"
    cards: list[tuple[str, str]] = []

    # Extract deck name from the first H1 heading
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            deck_name = stripped[2:].strip()
            break

    # Split on H2 headings (##) — each H2 is a card front
    # Everything between two H2 headings (or end of file) is the card back
    current_front: str | None = None
    current_back_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            # Save previous card if we have one
            if current_front is not None:
                back = "\n".join(current_back_lines).strip()
                if back:
                    cards.append((current_front, back))
            current_front = line[3:].strip()
            current_back_lines = []
        elif current_front is not None:
            current_back_lines.append(line)

    # Save the last card
    if current_front is not None:
        back = "\n".join(current_back_lines).strip()
        if back:
            cards.append((current_front, back))

    return deck_name, cards


def markdown_to_html(text: str) -> str:
    """Convert simple markdown to HTML for Anki card display."""
    lines = text.split("\n")
    html_parts: list[str] = []
    in_code_block = False
    in_table = False
    code_lines: list[str] = []
    table_lines: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                code_content = "\n".join(code_lines)
                # Escape HTML entities in code
                code_content = (
                    code_content.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )
                html_parts.append(f"<pre><code>{code_content}</code></pre>")
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Tables: detect by | separator
        if "|" in line and line.strip().startswith("|"):
            table_lines.append(line)
            i += 1
            continue
        elif table_lines:
            html_parts.append(_table_to_html(table_lines))
            table_lines = []

        # Blank line
        if not line.strip():
            html_parts.append("")
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            content = _inline_markdown(line[4:])
            html_parts.append(f"<h3>{content}</h3>")
        elif line.startswith("## "):
            content = _inline_markdown(line[3:])
            html_parts.append(f"<h2>{content}</h2>")
        elif line.startswith("# "):
            content = _inline_markdown(line[2:])
            html_parts.append(f"<h1>{content}</h1>")
        # Unordered list items
        elif line.startswith("- ") or line.startswith("* "):
            content = _inline_markdown(line[2:])
            html_parts.append(f"<li>{content}</li>")
        # Ordered list items
        elif re.match(r"^\d+\. ", line):
            content = _inline_markdown(re.sub(r"^\d+\. ", "", line))
            html_parts.append(f"<li>{content}</li>")
        else:
            content = _inline_markdown(line)
            html_parts.append(f"<p>{content}</p>")

        i += 1

    # Flush remaining table
    if table_lines:
        html_parts.append(_table_to_html(table_lines))

    return "\n".join(html_parts)


def _inline_markdown(text: str) -> str:
    """Convert inline markdown (bold, italic, code) to HTML."""
    # Escape HTML special characters first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Bold+italic: ***text***
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    # Inline code: `code`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def _table_to_html(table_lines: list[str]) -> str:
    """Convert markdown table lines to HTML table."""
    rows = []
    for line in table_lines:
        # Skip separator rows (|---|---|)
        if re.match(r"^\|[\s\-|:]+\|?\s*$", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)

    if not rows:
        return ""

    html = ["<table>"]
    for idx, row in enumerate(rows):
        tag = "th" if idx == 0 else "td"
        html.append("<tr>")
        for cell in row:
            html.append(f"<{tag}>{_inline_markdown(cell)}</{tag}>")
        html.append("</tr>")
    html.append("</table>")
    return "\n".join(html)


def make_note_id(deck_name: str, front: str) -> int:
    """Generate a deterministic note ID from deck name and card front."""
    key = f"{deck_name}::{front}"
    return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)


def build_deck_from_file(filepath: Path) -> genanki.Deck | None:
    """Build an Anki deck from a single markdown file."""
    deck_name, cards = parse_markdown_file(filepath)

    if not cards:
        print(f"  [WARN] No cards found in {filepath}", file=sys.stderr)
        return None

    # Generate a deterministic deck ID
    deck_id = int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16)
    deck = genanki.Deck(deck_id, deck_name)

    for front, back in cards:
        note = genanki.Note(
            model=ANKI_MODEL,
            fields=[front, markdown_to_html(back)],
            guid=make_note_id(deck_name, front),
        )
        deck.add_note(note)

    return deck


def build_category_deck(category_dir: Path) -> genanki.Deck | None:
    """Build a combined Anki deck from all markdown files in a category directory."""
    md_files = sorted(category_dir.glob("*.md"))
    if not md_files:
        return None

    category_name = category_dir.name.replace("-", " ").title()
    # Strip leading number prefix (e.g., "01 Networking Fundamentals" → "Networking Fundamentals")
    category_name = re.sub(r"^\d+\s+", "", category_name)

    deck_id = int(hashlib.md5(category_name.encode()).hexdigest()[:8], 16)
    deck = genanki.Deck(deck_id, f"Networking :: {category_name}")

    total_cards = 0
    for md_file in md_files:
        _, cards = parse_markdown_file(md_file)
        for front, back in cards:
            note = genanki.Note(
                model=ANKI_MODEL,
                fields=[front, markdown_to_html(back)],
                guid=make_note_id(f"Networking :: {category_name}", front),
            )
            deck.add_note(note)
            total_cards += 1

    if total_cards == 0:
        return None

    print(f"  Built '{deck.name}' ({total_cards} cards from {len(md_files)} files)")
    return deck


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Anki flashcard packages from markdown files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific markdown files to build (default: all files in content/)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=str(DEFAULT_OUTPUT_DIR),
        help=f"Output directory for .apkg files (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Also build a single combined deck with all cards",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.files:
        # Build from specific files
        for file_path in args.files:
            fp = Path(file_path)
            if not fp.exists():
                print(f"[ERROR] File not found: {fp}", file=sys.stderr)
                return 1
            deck = build_deck_from_file(fp)
            if deck:
                pkg = genanki.Package(deck)
                out = output_dir / f"{fp.stem}.apkg"
                pkg.write_to_file(str(out))
                print(f"  Written: {out}")
    else:
        # Build one deck per category directory
        print(f"Building Anki decks from: {CONTENT_DIR}")
        print(f"Output directory: {output_dir}\n")

        all_decks: list[genanki.Deck] = []
        category_dirs = sorted(d for d in CONTENT_DIR.iterdir() if d.is_dir())

        for cat_dir in category_dirs:
            deck = build_category_deck(cat_dir)
            if deck:
                pkg = genanki.Package(deck)
                safe_name = cat_dir.name
                out = output_dir / f"{safe_name}.apkg"
                pkg.write_to_file(str(out))
                print(f"  Written: {out}\n")
                all_decks.append(deck)

        if args.combined and all_decks:
            combined_pkg = genanki.Package(all_decks)
            combined_out = output_dir / "networking-all.apkg"
            combined_pkg.write_to_file(str(combined_out))
            total = sum(len(d.notes) for d in all_decks)
            print(f"\nCombined deck: {combined_out} ({total} total cards)")

        if not all_decks:
            print("[ERROR] No decks built — check content directory.", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
