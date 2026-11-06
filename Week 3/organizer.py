#!/usr/bin/env python3
"""Organize files in a chosen directory by file extension."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path

EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".rtf": "Documents", ".odt": "Documents",
    ".md": "Documents", ".epub": "Documents",
    # Spreadsheets
    ".xls": "Spreadsheets", ".xlsx": "Spreadsheets",
    ".csv": "Spreadsheets", ".ods": "Spreadsheets",
    # Presentations
    ".ppt": "Presentations", ".pptx": "Presentations", ".odp": "Presentations",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images",
    ".webp": "Images", ".tiff": "Images", ".tif": "Images", ".ico": "Images",
    # Videos
    ".mp4": "Videos", ".avi": "Videos", ".mkv": "Videos",
    ".mov": "Videos", ".wmv": "Videos", ".flv": "Videos",
    ".webm": "Videos", ".m4v": "Videos", ".mpeg": "Videos", ".mpg": "Videos",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".aac": "Audio",
    ".flac": "Audio", ".ogg": "Audio", ".m4a": "Audio",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives", ".bz2": "Archives", ".xz": "Archives",
    # Code and configuration
    ".py": "Code", ".js": "Code", ".ts": "Code", ".jsx": "Code",
    ".tsx": "Code", ".html": "Code", ".css": "Code", ".scss": "Code",
    ".java": "Code", ".c": "Code", ".cpp": "Code", ".h": "Code",
    ".hpp": "Code", ".cs": "Code", ".go": "Code", ".rs": "Code",
    ".rb": "Code", ".php": "Code", ".swift": "Code", ".kt": "Code",
    ".sh": "Code", ".bash": "Code", ".json": "Code", ".xml": "Code",
    ".yaml": "Code", ".yml": "Code", ".toml": "Code", ".sql": "Code",
}

CATEGORIES = set(EXTENSION_MAP.values()) | {"Misc"}


def unique_destination(destination: Path) -> Path:
    """Avoid overwriting an existing file by adding _1, _2, etc."""
    if not destination.exists():
        return destination
    number = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{number}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        number += 1


def collect_files(root: Path, recursive: bool) -> list[Path]:
    """Collect eligible files without entering category folders or hidden folders."""
    found = []
    if recursive:
        for current, dirs, files in os.walk(root):
            current_path = Path(current)
            dirs[:] = [
                d for d in dirs
                if not d.startswith(".")
                and not (current_path == root and d in CATEGORIES)
            ]
            for filename in files:
                if filename.startswith("."):
                    continue
                path = current_path / filename
                if path.is_file():
                    found.append(path)
    else:
        for path in root.iterdir():
            if path.name.startswith(".") or not path.is_file():
                continue
            found.append(path)
    return found


def organize_directory(root: Path, dry_run: bool = False,
                       recursive: bool = False) -> tuple[int, dict[str, int], list[str]]:
    counts = defaultdict(int)
    errors = []
    moved = 0

    try:
        files = collect_files(root, recursive)
    except OSError as exc:
        return 0, {}, [f"Could not scan {root}: {exc}"]

    for source in files:
        category = EXTENSION_MAP.get(source.suffix.lower(), "Misc")
        destination_dir = root / category
        destination = unique_destination(destination_dir / source.name)

        if dry_run:
            print(f"[DRY RUN] {source.relative_to(root)} -> {category}/{destination.name}")
            counts[category] += 1
            moved += 1
            continue

        try:
            destination_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            counts[category] += 1
            moved += 1
            print(f"Moved: {source.relative_to(root)} -> {category}/{destination.name}")
        except (PermissionError, OSError) as exc:
            errors.append(f"Could not move {source}: {exc}")

    return moved, dict(counts), errors


def print_summary(total: int, counts: dict[str, int], errors: list[str]) -> None:
    print("\n" + "=" * 52)
    print("       DIRECTORY ORGANIZER - EXECUTION SUMMARY")
    print("=" * 52)
    print(f"Files processed       : {total}")
    if counts:
        print("\nBreakdown by category:")
        for category in sorted(counts):
            print(f"  {category:<18}: {counts[category]:>4}")
    else:
        print("\nNo eligible files found.")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    print("=" * 52)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sort files in a folder into category subfolders."
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="Folder to organize. Defaults to the current folder."
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview the moves without changing any files."
    )
    parser.add_argument(
        "--recursive", "-r", action="store_true",
        help="Also organize files inside subfolders."
    )
    args = parser.parse_args()

    root = Path(args.directory).expanduser().resolve()
    if not root.exists():
        print(f"Error: folder does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"Error: path is not a folder: {root}", file=sys.stderr)
        return 1

    print(f"Target folder: {root}")
    if args.dry_run:
        print("Mode: DRY RUN. No files will be moved.")
    if args.recursive:
        print("Mode: Recursive.")

    total, counts, errors = organize_directory(
        root, dry_run=args.dry_run, recursive=args.recursive
    )
    print_summary(total, counts, errors)
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
