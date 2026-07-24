"""
pdf2txt_dir_tar_zip: Convert PDF files in a directory, tar, or zip archive to text.

Usage
-----
pdf2txt_dir_tar_zip <input> <output>

Where *input* is one of:
  - a directory containing PDF files (recursively searched)
  - a .tar, .tar.gz, or .tgz archive containing PDF files
  - a .zip archive containing PDF files

And *output* is one of:
  - a directory path  (created if absent)
  - a path ending in .tar, .tar.gz, .tgz, or .zip

Each PDF found in *input* is converted to a UTF-8 text file with the same
relative path and a .txt extension, and placed in *output*.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path


# ---------------------------------------------------------------------------
# PDF extraction helpers
# ---------------------------------------------------------------------------

def _pdf_to_text(pdf_path: Path) -> str:
    """Return the text content of *pdf_path* using pdfminer.six."""
    from pdfminer.high_level import extract_text  # type: ignore[import-untyped]

    return extract_text(str(pdf_path))


# ---------------------------------------------------------------------------
# Safe archive extraction
# ---------------------------------------------------------------------------

def _safe_tar_extract(tf: tarfile.TarFile, dest: Path) -> None:
    """Extract *tf* to *dest*, rejecting dangerous member paths."""
    dest_resolved = dest.resolve()
    for member in tf.getmembers():
        # Reject absolute paths (handles POSIX, Windows drive letters, UNC paths).
        if os.path.isabs(member.name):
            raise ValueError(f"Unsafe tar member (absolute path): {member.name!r}")
        # Reject path components that escape the destination directory.
        resolved = (dest / member.name).resolve()
        if not resolved.is_relative_to(dest_resolved):
            raise ValueError(f"Unsafe tar member (path traversal): {member.name!r}")
    tf.extractall(str(dest), filter="data")


def _safe_zip_extract(zf: zipfile.ZipFile, dest: Path) -> None:
    """Extract *zf* to *dest*, rejecting dangerous member paths."""
    dest_resolved = dest.resolve()
    for name in zf.namelist():
        # Reject absolute paths (handles POSIX, Windows drive letters, UNC paths).
        if os.path.isabs(name):
            raise ValueError(f"Unsafe zip member (absolute path): {name!r}")
        # Reject path components that escape the destination directory.
        resolved = (dest / name).resolve()
        if not resolved.is_relative_to(dest_resolved):
            raise ValueError(f"Unsafe zip member (path traversal): {name!r}")
    zf.extractall(str(dest))


# ---------------------------------------------------------------------------
# Input reading
# ---------------------------------------------------------------------------

def _extract_input(input_path: Path, tmp_dir: Path) -> Path:
    """Return a directory containing the (possibly extracted) input files."""
    if input_path.is_dir():
        return input_path

    extract_dir = tmp_dir / "input"
    extract_dir.mkdir()

    # Try tar first (is_tarfile also matches .tar.gz/.tgz)
    if tarfile.is_tarfile(str(input_path)):
        with tarfile.open(str(input_path)) as tf:
            _safe_tar_extract(tf, extract_dir)
        return extract_dir

    if zipfile.is_zipfile(str(input_path)):
        with zipfile.ZipFile(str(input_path)) as zf:
            _safe_zip_extract(zf, extract_dir)
        return extract_dir

    raise ValueError(
        f"{input_path} is not a directory, a tar archive, or a zip archive."
    )


# ---------------------------------------------------------------------------
# Core conversion
# ---------------------------------------------------------------------------

def convert_directory(input_dir: Path, output_dir: Path) -> int:
    """Convert every PDF under *input_dir* to text, writing results to *output_dir*.

    Returns the number of PDFs converted.
    """
    count = 0
    for pdf_file in sorted(input_dir.rglob("*.pdf")):
        rel = pdf_file.relative_to(input_dir)
        out_file = output_dir / rel.with_suffix(".txt")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = _pdf_to_text(pdf_file)
        except Exception as exc:  # noqa: BLE001
            print(f"WARNING: could not convert {rel}: {exc}", file=sys.stderr)
            continue
        out_file.write_text(text, encoding="utf-8")
        print(f"Converted: {rel}", file=sys.stderr)
        count += 1
    return count


# ---------------------------------------------------------------------------
# Output writing
# ---------------------------------------------------------------------------

def _write_output(converted_dir: Path, output_path: Path) -> None:
    """Write the converted text files to *output_path* (dir or archive)."""
    name = output_path.name.lower()

    if name.endswith(".tar.gz") or name.endswith(".tgz"):
        with tarfile.open(str(output_path), "w:gz") as tf:
            for f in sorted(converted_dir.rglob("*")):
                if f.is_file():
                    tf.add(str(f), arcname=str(f.relative_to(converted_dir)))
        return

    if name.endswith(".tar"):
        with tarfile.open(str(output_path), "w") as tf:
            for f in sorted(converted_dir.rglob("*")):
                if f.is_file():
                    tf.add(str(f), arcname=str(f.relative_to(converted_dir)))
        return

    if name.endswith(".zip"):
        with zipfile.ZipFile(str(output_path), "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(converted_dir.rglob("*")):
                if f.is_file():
                    zf.write(str(f), str(f.relative_to(converted_dir)))
        return

    # Default: output is a directory
    output_path.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(converted_dir), str(output_path), dirs_exist_ok=True)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        prog="pdf2txt_dir_tar_zip",
        description=(
            "Convert PDF files inside a directory, tar archive, or zip archive "
            "to UTF-8 text files, preserving the relative directory structure."
        ),
    )
    parser.add_argument(
        "input",
        help="Source directory, .tar, .tar.gz, .tgz, or .zip file containing PDFs.",
    )
    parser.add_argument(
        "output",
        help=(
            "Destination directory or archive (.tar, .tar.gz, .tgz, .zip). "
            "Determined by the file extension; anything else is treated as a directory."
        ),
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        print(f"Error: input path does not exist: {input_path}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        try:
            source_dir = _extract_input(input_path, tmp)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        converted_dir = tmp / "output"
        converted_dir.mkdir()

        count = convert_directory(source_dir, converted_dir)

        if count == 0:
            print("Warning: no PDF files were found in the input.", file=sys.stderr)

        _write_output(converted_dir, output_path)

    print(f"Done. {count} PDF(s) converted.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
