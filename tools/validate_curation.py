#!/usr/bin/env python3
"""
ASCII Art Curation Validation Script

Validates that the curation processing was successful by checking:
- File counts match expectations
- Metadata references match actual files
- Archive matches "bad" selections
- No orphaned or missing files
"""

import yaml
import json
from pathlib import Path
import sys


def main():
    """Run validation checks on curated ASCII art collection."""

    print("=" * 70)
    print("ASCII Art Curation Validation")
    print("=" * 70)
    print()

    # Check if curation file exists
    curation_file = Path('ascii_art_curation.json')
    if not curation_file.exists():
        print("⚠ WARNING: ascii_art_curation.json not found")
        print("  Validation can only check file/metadata consistency")
        curation = None
    else:
        with open(curation_file) as f:
            curation = json.load(f)

    # Load metadata
    metadata_file = Path('data/ascii_art/metadata.yaml')
    if not metadata_file.exists():
        print("✗ ERROR: metadata.yaml not found")
        sys.exit(1)

    with open(metadata_file) as f:
        metadata = yaml.safe_load(f)

    # Count pieces in metadata
    metadata_files = set()
    theme_counts = {}
    for theme, pieces in metadata.items():
        theme_counts[theme] = len(pieces)
        for piece in pieces:
            for variant in piece['variants']:
                metadata_files.add(variant['file'])

    # Count actual files
    actual_files = set()
    actual_theme_counts = {}
    for theme_dir in Path('data/ascii_art').iterdir():
        if theme_dir.is_dir():
            theme = theme_dir.name
            count = len(list(theme_dir.glob('*.txt')))
            actual_theme_counts[theme] = count
            for txt_file in theme_dir.glob('*.txt'):
                rel_path = txt_file.relative_to('data/ascii_art')
                actual_files.add(str(rel_path).replace('\\', '/'))

    # Count archived files
    archived_files = set()
    archive_theme_counts = {}
    archive_dir = Path('data/ascii_art_archive')
    if archive_dir.exists():
        for theme_dir in archive_dir.iterdir():
            if theme_dir.is_dir():
                theme = theme_dir.name
                count = len(list(theme_dir.glob('*.txt')))
                archive_theme_counts[theme] = count
                for txt_file in theme_dir.glob('*.txt'):
                    rel_path = txt_file.relative_to('data/ascii_art_archive')
                    archived_files.add(str(rel_path).replace('\\', '/'))

    # Display curation summary if available
    if curation:
        good_count = sum(1 for v in curation['curated'].values() if v == 'good')
        bad_count = sum(1 for v in curation['curated'].values() if v == 'bad')
        unmarked_count = curation['total'] - good_count - bad_count

        print("📊 CURATION SUMMARY")
        print("-" * 70)
        print(f"  Good (kept):      {good_count:3d} pieces")
        print(f"  Bad (archived):   {bad_count:3d} pieces")
        print(f"  Unmarked (kept):  {unmarked_count:3d} pieces")
        print(f"  Total reviewed:   {curation['total']:3d} pieces")
        print()

    # Display file counts
    print("📁 FILE COUNTS")
    print("-" * 70)
    print(f"  Metadata refs:    {len(metadata_files):3d} files")
    print(f"  Actual files:     {len(actual_files):3d} files")
    print(f"  Archived files:   {len(archived_files):3d} files")
    print()

    # Display theme breakdown
    print("🎨 THEME BREAKDOWN")
    print("-" * 70)
    all_themes = sorted(set(theme_counts.keys()) | set(actual_theme_counts.keys()))

    for theme in all_themes:
        meta_count = theme_counts.get(theme, 0)
        actual_count = actual_theme_counts.get(theme, 0)
        archive_count = archive_theme_counts.get(theme, 0)

        status = "✓" if meta_count == actual_count else "✗"

        print(f"  {status} {theme:15s}  Meta: {meta_count:2d}  Files: {actual_count:2d}  Archived: {archive_count:2d}")
    print()

    # Validation checks
    errors = []
    warnings = []

    # Check 1: Metadata files should match actual files
    if metadata_files == actual_files:
        print("✓ All metadata file references exist")
    else:
        orphaned = actual_files - metadata_files
        missing = metadata_files - actual_files

        if orphaned:
            warnings.append(f"Orphaned files (exist but not in metadata): {len(orphaned)}")
            for f in sorted(orphaned):
                print(f"  ⚠ Orphaned: {f}")

        if missing:
            errors.append(f"Missing files (in metadata but don't exist): {len(missing)}")
            for f in sorted(missing):
                print(f"  ✗ Missing: {f}")

    # Check 2: If curation exists, validate archive count
    if curation and archive_dir.exists():
        bad_count = sum(1 for v in curation['curated'].values() if v == 'bad')
        if len(archived_files) == bad_count:
            print("✓ Archive count matches 'bad' selections")
        else:
            warnings.append(
                f"Archive mismatch: {len(archived_files)} archived vs {bad_count} marked bad"
            )

    # Check 3: Expected vs actual counts
    if curation:
        expected_kept = good_count + unmarked_count
        expected_archived = bad_count

        print()
        print("🔍 VALIDATION RESULTS")
        print("-" * 70)
        print(f"  Expected kept:    {expected_kept:3d} files")
        print(f"  Actual kept:      {len(actual_files):3d} files")
        print(f"  Expected archive: {expected_archived:3d} files")
        print(f"  Actual archive:   {len(archived_files):3d} files")

        if len(actual_files) == expected_kept:
            print("  ✓ Kept files match expectation")
        else:
            errors.append(
                f"Kept file mismatch: expected {expected_kept}, got {len(actual_files)}"
            )

        if len(archived_files) == expected_archived:
            print("  ✓ Archived files match expectation")
        else:
            warnings.append(
                f"Archive mismatch: expected {expected_archived}, got {len(archived_files)}"
            )

    # Final summary
    print()
    print("=" * 70)
    if errors:
        print(f"✗ VALIDATION FAILED - {len(errors)} error(s)")
        for error in errors:
            print(f"  ✗ {error}")
        sys.exit(1)
    elif warnings:
        print(f"⚠ VALIDATION PASSED WITH WARNINGS - {len(warnings)} warning(s)")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        sys.exit(0)
    else:
        print("✓ VALIDATION PASSED - All checks successful!")
        sys.exit(0)


if __name__ == '__main__':
    main()
