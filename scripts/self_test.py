"""Test bundled tooling with synthetic inputs only; no previous deck is needed.

Run with the same typst, pymupdf, and pillow environment as build.py.
Temporary outputs are cleaned up. This is not scientific or visual validation.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import pymupdf


SKILL = Path(__file__).resolve().parents[1]


def run(script, *args, failure=None):
    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts" / script), *map(str, args)],
        capture_output=True, text=True,
    )
    if failure is None:
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
    elif result.returncode == 0 or failure not in result.stderr:
        raise RuntimeError(f"Expected failure {failure!r}: {result.stdout}{result.stderr}")


def check(root):
    template = SKILL / "assets/typst-template"
    run("build.py", template, "--draft", "--output-dir", root / "template")
    run("build.py", template, "--output-dir", root / "placeholders",
        failure="unfinished placeholder")
    run("build.py", template, "--draft", "--expected-pages", 99,
        "--output-dir", root / "wrong-count", failure="Expected 99 pages")
    run("build.py", template, "--draft", "--output-dir", root / "template",
        failure="File exists")

    deck = root / "fresh-deck"
    deck.mkdir()
    shutil.copy2(template / "theme.typ", deck / "theme.typ")
    # A tool fixture, not a scientific claim or sample paper.
    source = '''#import "theme.typ": *
#show: theme
#title-slide(config: config-page(footer: source-footer), extra: [
  Synthetic tooling fixture
  #cite[Tool test only.]
])
#speaker-note[中文备注只用于测试导出。]
== Rendering check
This page tests the build pipeline, not an empirical result.
#cite[Tool test only.]
#speaker-note[检查第二页备注与物理页码一致。]
'''
    (deck / "main.typ").write_text(source, encoding="utf-8")
    run("build.py", deck)
    notes = json.loads((deck / "build/slides.pdfpc").read_text(encoding="utf-8"))
    if len(notes["pages"]) != 2 or not all(p.get("note") for p in notes["pages"]):
        raise RuntimeError("Speaker notes were not exported")
    with pymupdf.open(deck / "build/slides.pdf") as pdf:
        if len(pdf) != 2 or any(
            any("\u4e00" <= char <= "\u9fff" for char in page.get_text()) for page in pdf
        ):
            raise RuntimeError("Page count or note-leakage regression")
    (deck / "main.typ").write_text(
        source.replace("#speaker-note[检查第二页备注与物理页码一致。]", ""), encoding="utf-8")
    run("build.py", deck, "--output-dir", root / "missing-notes",
        failure="Missing speaker notes")

    pdf = root / "source.pdf"
    with pymupdf.open() as doc:
        page = doc.new_page(width=400, height=300)
        page.draw_rect(pymupdf.Rect(40, 30, 360, 150), color=(0, 0, 0))
        page.insert_text((60, 80), "Synthetic crop fixture", fontsize=18)
        doc.save(pdf)
    spec = {
        "sources": {"fixture": {"pdf": pdf.name, "version": "synthetic"}},
        "crops": [{"name": "fixture", "source": "fixture", "page": 1,
                   "rect": [0.1, 0.1, 0.9, 0.5], "figure": "Tool test"}],
    }
    manifest = root / "manifest.json"
    manifest.write_text(json.dumps(spec), encoding="utf-8")
    run("extract_figures.py", manifest, "--output-dir", root / "crops")
    record = json.loads((root / "crops/sources.json").read_text())["crops"][0]
    if record["pdf_sha256"] != hashlib.sha256(pdf.read_bytes()).hexdigest():
        raise RuntimeError("Source hash regression")
    if record["output_sha256"] != hashlib.sha256((root / "crops/fixture.png").read_bytes()).hexdigest():
        raise RuntimeError("Output hash regression")
    run("extract_figures.py", manifest, "--output-dir", root / "crops", failure="File exists")
    spec["crops"][0]["rect"] = [0.9, 0.1, 0.2, 0.5]
    manifest.write_text(json.dumps(spec), encoding="utf-8")
    run("extract_figures.py", manifest, "--output-dir", root / "invalid",
        failure="Invalid normalized rectangle")
    if (root / "invalid").exists():
        raise RuntimeError("Invalid input created an output directory")


if __name__ == "__main__":
    preferred = Path("/tmp/opencode")
    with tempfile.TemporaryDirectory(prefix="academic-slides-test-",
                                     dir=preferred if preferred.is_dir() else None) as temp:
        check(Path(temp))
    print("PASS: draft/final builds, placeholders, counts, notes, overwrite guards, crop hashes, invalid rectangles")
