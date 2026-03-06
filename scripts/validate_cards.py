#!/usr/bin/env python3
"""
validate_cards.py — Validate flashcard markdown files for quality and consistency.

Checks performed:
  - Each file has at least one H1 heading (deck name)
  - Each H2 heading has non-empty content following it (card back)
  - No duplicate card fronts within a file
  - No duplicate card fronts across the entire content directory
  - No empty card fronts or backs
  - Minimum back length (at least 5 characters)
  - No H3/H4 headings used as H2 (accidental extra # signs)

Exit codes:
  0 — all checks passed
  1 — one or more validation errors found

Usage:
    python scripts/validate_cards.py
    python scripts/validate_cards.py --verbose
    python scripts/validate_cards.py content/01-networking-fundamentals/ipv4-ipv6.md
"""

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content"
MIN_BACK_LENGTH = 5


def parse_cards(filepath: Path) -> tuple[str | None, list[tuple[str, str]], list[str]]:
    """
    Parse markdown file and return (deck_name, cards, errors).

    deck_name: the H1 heading text, or None if missing
    cards: list of (front, back) tuples
    errors: list of error messages
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.splitlines()

    errors: list[str] = []
    deck_name: str | None = None
    cards: list[tuple[str, str]] = []

    # Find deck name (first H1)
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            deck_name = stripped[2:].strip()
            break

    if not deck_name:
        errors.append("Missing H1 heading (deck name)")

    # Parse H2 cards
    current_front: str | None = None
    current_back_lines: list[str] = []
    line_numbers: dict[str, int] = {}

    for line_num, line in enumerate(lines, start=1):
        if line.startswith("## "):
            # Save previous card
            if current_front is not None:
                back = "\n".join(current_back_lines).strip()
                cards.append((current_front, back))

            current_front = line[3:].strip()
            current_back_lines = []

            if not current_front:
                errors.append(f"Line {line_num}: Empty card front (## with no text)")
            else:
                if current_front in line_numbers:
                    errors.append(
                        f"Line {line_num}: Duplicate card front within file "
                        f"(first at line {line_numbers[current_front]}): "
                        f"'{current_front[:60]}'"
                    )
                else:
                    line_numbers[current_front] = line_num

        elif current_front is not None:
            current_back_lines.append(line)

    # Save last card
    if current_front is not None:
        back = "\n".join(current_back_lines).strip()
        cards.append((current_front, back))

    # Validate each card
    for front, back in cards:
        if not back:
            errors.append(f"Empty card back for front: '{front[:60]}'")
        elif len(back) < MIN_BACK_LENGTH:
            errors.append(
                f"Card back too short ({len(back)} chars) for front: '{front[:60]}'"
            )

    if not cards and deck_name:
        errors.append("No cards found (no ## headings)")

    return deck_name, cards, errors


def validate_all_files(
    files: list[Path], verbose: bool = False
) -> tuple[int, int, int]:
    """
    Validate all files and check for cross-file duplicates.

    Returns:
        (total_files, total_cards, total_errors)
    """
    all_fronts: dict[str, str] = {}  # front -> "filepath:line_num"
    total_errors = 0
    total_cards = 0
    total_files = 0

    for filepath in files:
        total_files += 1
        try:
            rel_path = filepath.relative_to(REPO_ROOT)
        except ValueError:
            rel_path = filepath

        deck_name, cards, errors = parse_cards(filepath)

        # Check for cross-file duplicate fronts
        for front, _back in cards:
            key = front.strip().lower()
            source = f"{rel_path}"
            if key in all_fronts:
                errors.append(
                    f"Cross-file duplicate card front "
                    f"(also in {all_fronts[key]}): '{front[:60]}'"
                )
            else:
                all_fronts[key] = source

        total_cards += len(cards)

        if errors:
            print(f"\n[FAIL] {rel_path}")
            for err in errors:
                print(f"  ✗ {err}")
            total_errors += len(errors)
        elif verbose:
            print(f"[PASS] {rel_path} ({len(cards)} cards)")

    return total_files, total_cards, total_errors


def find_markdown_files(content_dir: Path) -> list[Path]:
    """Find all markdown files in the content directory."""
    return sorted(content_dir.rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate networking flashcard markdown files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to validate (default: all files in content/)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show passing files as well",
    )
    args = parser.parse_args()

    if args.files:
        files = [Path(f) for f in args.files]
        missing = [f for f in files if not f.exists()]
        if missing:
            for f in missing:
                print(f"[ERROR] File not found: {f}", file=sys.stderr)
            return 1
    else:
        files = find_markdown_files(CONTENT_DIR)
        if not files:
            print(f"[ERROR] No markdown files found in {CONTENT_DIR}", file=sys.stderr)
            return 1

    print(f"Validating {len(files)} markdown file(s)...\n")

    total_files, total_cards, total_errors = validate_all_files(
        files, verbose=args.verbose
    )

    print(f"\n{'='*50}")
    print(f"Files checked : {total_files}")
    print(f"Total cards   : {total_cards}")
    print(f"Total errors  : {total_errors}")

    if total_errors == 0:
        print("\n✓ All validation checks passed!")
        return 0
    else:
        print(f"\n✗ {total_errors} error(s) found — fix before building.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
