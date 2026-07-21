#!/usr/bin/env python3
"""
File Organizer — Automatically organize files into folders by type.

Usage:
    python -m file_organizer /path/to/directory [--dry-run] [--verbose]
    python -m file_organizer /path/to/directory --reverse
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

from .categories import CATEGORIES, get_category

# Files and folders to skip
SKIP_ITEMS = {
    ".DS_Store", "Thumbs.db", ".gitkeep", ".gitignore",
    "desktop.ini", ".directory",
}

SKIP_DIRS = {
    "__pycache__", ".git", ".svn", ".hg", "node_modules",
    ".venv", "venv", ".env", "env",
}


def collect_files(directory: Path) -> list[Path]:
    """Collect all files in the directory (non-recursive)."""
    files = []
    for item in directory.iterdir():
        if item.is_file() and item.name not in SKIP_ITEMS:
            files.append(item)
    return files


def organize_directory(
    directory: Path,
    dry_run: bool = False,
    verbose: bool = False,
    reverse: bool = False,
    custom_map: dict[str, str] | None = None,
) -> dict[str, list[tuple[str, str]]]:
    """
    Organize files in a directory by type.

    Returns a dict of category -> list of (filename, target_path) tuples.
    """
    if not directory.exists():
        print(f"❌ Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    if not directory.is_dir():
        print(f"❌ Error: '{directory}' is not a directory.")
        sys.exit(1)

    files = collect_files(directory)

    if not files:
        print(f"📂 No files found in '{directory}'.")
        return {}

    if reverse:
        return _reverse_organize(directory, files, dry_run, verbose)

    moved: dict[str, list[tuple[str, str]]] = {}
    skipped = 0
    errors = 0

    for file_path in files:
        ext = file_path.suffix  # e.g. '.jpg'
        category = get_category(ext)

        if category is None:
            # If custom map is provided, check it
            if custom_map and ext in custom_map:
                category = custom_map[ext]
            else:
                if verbose:
                    print(f"  ⏭️  Skipping '{file_path.name}' (unknown type: {ext})")
                skipped += 1
                continue

        target_dir = directory / category
        target_path = target_dir / file_path.name

        # Handle filename conflicts
        if target_path.exists():
            base = file_path.stem
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{base}_{counter}{ext}"
                counter += 1

        if category not in moved:
            moved[category] = []

        if dry_run:
            moved[category].append((file_path.name, str(target_path)))
            if verbose:
                print(f"  📋 Would move: '{file_path.name}' → {category}/")
        else:
            try:
                target_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(target_path))
                moved[category].append((file_path.name, str(target_path)))
                if verbose:
                    print(f"  ✅ Moved: '{file_path.name}' → {category}/")
            except OSError as e:
                print(f"  ❌ Error moving '{file_path.name}': {e}")
                errors += 1

    # Print summary
    action = "Would organize" if dry_run else "Organized"
    print(f"\n{action} {directory}:")

    total = sum(len(items) for items in moved.values())
    for cat, items in sorted(moved.items()):
        print(f"  📁 {cat}/  ({len(items)} files)")

    if skipped:
        print(f"  ⏭️  Skipped: {skipped} files (unknown types)")

    if dry_run:
        print(f"\n💡 Run without --dry-run to apply changes.")
    else:
        print(f"\n✅ Done! {total} files organized.")

    return moved


def _reverse_organize(
    directory: Path,
    files: list[Path],
    dry_run: bool = False,
    verbose: bool = False,
) -> dict[str, list[tuple[str, str]]]:
    """Reverse mode: move files from category folders back to root."""
    moved: dict[str, list[tuple[str, str]]] = {}
    errors = 0

    for file_path in files:
        parent_dir = file_path.parent
        if parent_dir == directory:
            continue  # Skip files already in root

        target_path = directory / file_path.name

        if target_path.exists():
            base = file_path.stem
            ext = file_path.suffix
            counter = 1
            while target_path.exists():
                target_path = directory / f"{base}_restored_{counter}{ext}"
                counter += 1

        category = parent_dir.name
        if category not in moved:
            moved[category] = []

        if dry_run:
            moved[category].append((file_path.name, str(target_path)))
            if verbose:
                print(f"  📋 Would restore: '{file_path.name}' → root/")
        else:
            try:
                shutil.move(str(file_path), str(target_path))
                moved[category].append((file_path.name, str(target_path)))
                if verbose:
                    print(f"  ✅ Restored: '{file_path.name}' → root/")
            except OSError as e:
                print(f"  ❌ Error restoring '{file_path.name}': {e}")
                errors += 1

    # Remove empty category folders
    if not dry_run:
        for cat in list(moved.keys()):
            cat_dir = directory / cat
            if cat_dir.exists() and not any(cat_dir.iterdir()):
                try:
                    cat_dir.rmdir()
                    if verbose:
                        print(f"  🗑️  Removed empty folder: {cat}/")
                except OSError:
                    pass

    action = "Would restore" if dry_run else "Restored"
    print(f"\n{action} files to root of {directory}:")
    total = sum(len(items) for items in moved.values())
    for cat, items in sorted(moved.items()):
        print(f"  ↪️  {cat}/ → ({len(items)} files)")
    print(f"\n✅ Done! {total} files restored.")

    return moved


def list_categories() -> None:
    """Print all supported categories and their extensions."""
    print("Supported file categories:\n")
    for cat, exts in sorted(CATEGORIES.items()):
        ext_list = ", ".join(exts)
        print(f"  {cat}/")
        print(f"     {ext_list}")
    print(f"\nTotal: {len(CATEGORIES)} categories")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by type.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  file-organizer /path/to/folder
  file-organizer /path/to/folder --dry-run --verbose
  file-organizer /path/to/folder --reverse
  file-organizer --list
  file-organizer --categories
        """,
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without actually moving files",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output for each file",
    )
    parser.add_argument(
        "--reverse", "-r",
        action="store_true",
        help="Reverse mode: move files from category folders back to root",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        dest="list_categories",
        help="List all supported file categories and extensions",
    )
    parser.add_argument(
        "--categories", "-c",
        action="store_true",
        help="Alias for --list",
    )

    args = parser.parse_args()

    if args.list_categories or args.categories:
        list_categories()
        return

    directory = Path(args.directory).resolve()
    organize_directory(
        directory=directory,
        dry_run=args.dry_run,
        verbose=args.verbose,
        reverse=args.reverse,
    )


if __name__ == "__main__":
    main()
