"""Tests for survey_with_chatbot.pdf2txt_dir_tar_zip."""

from __future__ import annotations

import os
import tarfile
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest

from survey_with_chatbot.pdf2txt_dir_tar_zip import (
    _extract_input,
    _safe_tar_extract,
    _safe_zip_extract,
    _write_output,
    convert_directory,
    main,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_TEXT = "Hello PDF world.\nThis is page one.\n"


def _make_fake_pdf(path: Path) -> None:
    """Write a minimal (but syntactically valid enough) PDF byte string."""
    path.write_bytes(
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\n"
        b"xref\n0 4\n0000000000 65535 f \n"
        b"trailer<</Size 4/Root 1 0 R>>\n"
        b"startxref\n9\n%%EOF\n"
    )


def _mock_pdf_to_text(_path: str) -> str:
    return SAMPLE_TEXT


# ---------------------------------------------------------------------------
# _extract_input
# ---------------------------------------------------------------------------

class TestExtractInput:
    def test_directory_returned_as_is(self, tmp_path: Path) -> None:
        src = tmp_path / "pdfs"
        src.mkdir()
        result = _extract_input(src, tmp_path / "work")
        assert result == src

    def test_tar_gz_extracted(self, tmp_path: Path) -> None:
        pdf_dir = tmp_path / "src"
        pdf_dir.mkdir()
        _make_fake_pdf(pdf_dir / "a.pdf")

        archive = tmp_path / "bundle.tar.gz"
        with tarfile.open(str(archive), "w:gz") as tf:
            tf.add(str(pdf_dir / "a.pdf"), arcname="a.pdf")

        work = tmp_path / "work"
        work.mkdir()
        result = _extract_input(archive, work)
        assert (result / "a.pdf").exists()

    def test_zip_extracted(self, tmp_path: Path) -> None:
        pdf_dir = tmp_path / "src"
        pdf_dir.mkdir()
        _make_fake_pdf(pdf_dir / "b.pdf")

        archive = tmp_path / "bundle.zip"
        with zipfile.ZipFile(str(archive), "w") as zf:
            zf.write(str(pdf_dir / "b.pdf"), "b.pdf")

        work = tmp_path / "work"
        work.mkdir()
        result = _extract_input(archive, work)
        assert (result / "b.pdf").exists()

    def test_invalid_input_raises(self, tmp_path: Path) -> None:
        bad = tmp_path / "not_an_archive.txt"
        bad.write_text("nope")
        work = tmp_path / "work"
        work.mkdir()
        with pytest.raises(ValueError, match="not a directory"):
            _extract_input(bad, work)


# ---------------------------------------------------------------------------
# Security: safe extraction
# ---------------------------------------------------------------------------

class TestSafeExtraction:
    def test_tar_path_traversal_rejected(self, tmp_path: Path) -> None:
        archive = tmp_path / "evil.tar"
        with tarfile.open(str(archive), "w") as tf:
            info = tarfile.TarInfo(name="../evil.txt")
            import io
            data = b"boom"
            info.size = len(data)
            tf.addfile(info, io.BytesIO(data))

        dest = tmp_path / "dest"
        dest.mkdir()
        with tarfile.open(str(archive)) as tf:
            with pytest.raises(ValueError, match="Unsafe tar member"):
                _safe_tar_extract(tf, dest)

    def test_zip_path_traversal_rejected(self, tmp_path: Path) -> None:
        archive = tmp_path / "evil.zip"
        with zipfile.ZipFile(str(archive), "w") as zf:
            zf.writestr("../evil.txt", "boom")

        dest = tmp_path / "dest"
        dest.mkdir()
        with zipfile.ZipFile(str(archive)) as zf:
            with pytest.raises(ValueError, match="Unsafe zip member"):
                _safe_zip_extract(zf, dest)


# ---------------------------------------------------------------------------
# convert_directory
# ---------------------------------------------------------------------------

class TestConvertDirectory:
    def test_converts_pdfs(self, tmp_path: Path) -> None:
        input_dir = tmp_path / "in"
        input_dir.mkdir()
        _make_fake_pdf(input_dir / "paper.pdf")

        output_dir = tmp_path / "out"
        output_dir.mkdir()

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            count = convert_directory(input_dir, output_dir)

        assert count == 1
        txt = (output_dir / "paper.txt").read_text(encoding="utf-8")
        assert txt == SAMPLE_TEXT

    def test_preserves_subdirectory_structure(self, tmp_path: Path) -> None:
        input_dir = tmp_path / "in"
        sub = input_dir / "sub"
        sub.mkdir(parents=True)
        _make_fake_pdf(sub / "deep.pdf")

        output_dir = tmp_path / "out"
        output_dir.mkdir()

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            count = convert_directory(input_dir, output_dir)

        assert count == 1
        assert (output_dir / "sub" / "deep.txt").exists()

    def test_skips_non_pdf_files(self, tmp_path: Path) -> None:
        input_dir = tmp_path / "in"
        input_dir.mkdir()
        (input_dir / "readme.txt").write_text("hello")

        output_dir = tmp_path / "out"
        output_dir.mkdir()

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            count = convert_directory(input_dir, output_dir)

        assert count == 0

    def test_continues_on_conversion_error(self, tmp_path: Path) -> None:
        input_dir = tmp_path / "in"
        input_dir.mkdir()
        _make_fake_pdf(input_dir / "bad.pdf")
        _make_fake_pdf(input_dir / "good.pdf")

        output_dir = tmp_path / "out"
        output_dir.mkdir()

        call_count = {"n": 0}

        def flaky(path) -> str:
            call_count["n"] += 1
            if "bad" in str(path):
                raise RuntimeError("parse error")
            return SAMPLE_TEXT

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=flaky,
        ):
            count = convert_directory(input_dir, output_dir)

        assert count == 1
        assert (output_dir / "good.txt").exists()
        assert not (output_dir / "bad.txt").exists()


# ---------------------------------------------------------------------------
# _write_output
# ---------------------------------------------------------------------------

class TestWriteOutput:
    def _make_converted_dir(self, tmp_path: Path) -> Path:
        d = tmp_path / "converted"
        d.mkdir()
        (d / "paper.txt").write_text(SAMPLE_TEXT, encoding="utf-8")
        return d

    def test_write_to_directory(self, tmp_path: Path) -> None:
        converted = self._make_converted_dir(tmp_path)
        out_dir = tmp_path / "result"
        _write_output(converted, out_dir)
        assert (out_dir / "paper.txt").read_text(encoding="utf-8") == SAMPLE_TEXT

    def test_write_to_tar_gz(self, tmp_path: Path) -> None:
        converted = self._make_converted_dir(tmp_path)
        out = tmp_path / "result.tar.gz"
        _write_output(converted, out)
        assert out.exists()
        with tarfile.open(str(out)) as tf:
            names = tf.getnames()
        assert "paper.txt" in names

    def test_write_to_zip(self, tmp_path: Path) -> None:
        converted = self._make_converted_dir(tmp_path)
        out = tmp_path / "result.zip"
        _write_output(converted, out)
        assert out.exists()
        with zipfile.ZipFile(str(out)) as zf:
            names = zf.namelist()
        assert "paper.txt" in names

    def test_write_to_tar(self, tmp_path: Path) -> None:
        converted = self._make_converted_dir(tmp_path)
        out = tmp_path / "result.tar"
        _write_output(converted, out)
        assert out.exists()
        with tarfile.open(str(out)) as tf:
            names = tf.getnames()
        assert "paper.txt" in names


# ---------------------------------------------------------------------------
# main (CLI)
# ---------------------------------------------------------------------------

class TestMain:
    def test_missing_input_returns_1(self, tmp_path: Path) -> None:
        rc = main([str(tmp_path / "nonexistent"), str(tmp_path / "out")])
        assert rc == 1

    def test_converts_directory_to_directory(self, tmp_path: Path) -> None:
        in_dir = tmp_path / "in"
        in_dir.mkdir()
        _make_fake_pdf(in_dir / "doc.pdf")
        out_dir = tmp_path / "out"

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            rc = main([str(in_dir), str(out_dir)])

        assert rc == 0
        assert (out_dir / "doc.txt").read_text(encoding="utf-8") == SAMPLE_TEXT

    def test_converts_zip_to_directory(self, tmp_path: Path) -> None:
        pdf_dir = tmp_path / "src"
        pdf_dir.mkdir()
        _make_fake_pdf(pdf_dir / "z.pdf")

        archive = tmp_path / "bundle.zip"
        with zipfile.ZipFile(str(archive), "w") as zf:
            zf.write(str(pdf_dir / "z.pdf"), "z.pdf")

        out_dir = tmp_path / "out"

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            rc = main([str(archive), str(out_dir)])

        assert rc == 0
        assert (out_dir / "z.txt").read_text(encoding="utf-8") == SAMPLE_TEXT

    def test_converts_directory_to_zip(self, tmp_path: Path) -> None:
        in_dir = tmp_path / "in"
        in_dir.mkdir()
        _make_fake_pdf(in_dir / "q.pdf")
        out_zip = tmp_path / "out.zip"

        with patch(
            "survey_with_chatbot.pdf2txt_dir_tar_zip._pdf_to_text",
            side_effect=_mock_pdf_to_text,
        ):
            rc = main([str(in_dir), str(out_zip)])

        assert rc == 0
        with zipfile.ZipFile(str(out_zip)) as zf:
            assert "q.txt" in zf.namelist()
