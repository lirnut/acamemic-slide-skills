"""Build a simple heading-based Touying deck and check structural invariants.

Requires typst, pymupdf, pillow. Visual and scientific review remain manual.
"""

import argparse
import json
import math
from pathlib import Path
import re

import pymupdf
import typst
from PIL import Image, ImageDraw


def build(args):
    root = args.deck.resolve()
    source_path = root / "main.typ"
    source = source_path.read_text(encoding="utf-8")
    if args.expected_pages is None:
        # This is a convention check, not a general Typst parser.
        active = "\n".join(line for line in source.splitlines()
                           if not line.lstrip().startswith("//"))
        unsupported = r"#(?:pause|meanwhile|slide|pagebreak|include)\b|^=\s|/\*"
        if re.search(unsupported, active, re.MULTILINE):
            raise ValueError("Complex source: supply independently verified --expected-pages")
        expected = len(re.findall(r"^==\s+.+$", active, re.MULTILINE))
        expected += len(re.findall(r"#title-slide\s*\(", active))
    else:
        expected = args.expected_pages
    if expected < 1:
        raise ValueError("Expected page count must be positive")

    output = (args.output_dir or root / "build").resolve()
    # Never overwrite previous generated outputs or a user's existing directory.
    output.mkdir(parents=True, exist_ok=False)
    pdf = output / "slides.pdf"
    typst.compile(str(source_path), output=str(pdf), root=str(root))
    raw = typst.query(str(source_path), "<pdfpc-file>", field="value",
                      one=True, root=str(root))
    notes = json.loads(raw)
    with pymupdf.open(pdf) as doc:
        errors = []
        if len(doc) != expected:
            errors.append(f"Expected {expected} pages, got {len(doc)}; check overflow/blank pages")
        pages = notes.get("pages", [])
        indices = [p.get("idx") for p in pages]
        if sorted(i for i in indices if isinstance(i, int)) != list(range(len(doc))):
            errors.append("Presenter metadata must contain one entry per physical page")
        if not args.allow_missing_notes:
            missing = [p.get("idx", -1) + 1 for p in pages if not p.get("note", "").strip()]
            if missing:
                errors.append(f"Missing speaker notes on pages {missing}")
        for number, page in enumerate(doc, 1):
            if not args.draft and re.search(
                r"\b(?:DRAFT|TODO|TBD)\b|lorem ipsum|Replace (?:this|with)|Insert an original",
                page.get_text(), re.IGNORECASE,
            ):
                errors.append(f"Page {number}: possible unfinished placeholder; replace it or review before final delivery")
            if abs(page.rect.width - args.width) > 1 or abs(page.rect.height - args.height) > 1:
                errors.append(f"Page {number}: unexpected dimensions {page.rect}")
            for block in page.get_text("blocks"):
                if block[6] == 0 and (block[0] < -1 or block[1] < -1 or
                                     block[2] > page.rect.width + 1 or
                                     block[3] > page.rect.height + 1):
                    errors.append(f"Page {number}: text outside page: {block[4][:60]!r}")
        if errors:
            raise ValueError("\n".join(errors))

        (output / "slides.pdfpc").write_text(
            json.dumps(notes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        scripts = ["# Speaker scripts\n", "Generated from source speaker-note blocks; edit the source.\n"]
        for page in sorted(pages, key=lambda p: p["idx"]):
            note = page.get("note", "").strip()
            if note:
                scripts.append(f"## PDF page {page['idx'] + 1}\n\n{note}\n")
        (output / "speech-script.md").write_text("\n".join(scripts), encoding="utf-8")
        preview = output / "preview"
        preview.mkdir()
        sheet = Image.new("RGB", (1440, math.ceil(len(doc) / 3) * 305), "#e7ebef")
        draw = ImageDraw.Draw(sheet)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
            pix.save(preview / f"slide-{i + 1:02}.png")
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            image.thumbnail((468, 264))
            x, y = i % 3 * 480 + 6, i // 3 * 305 + 27
            sheet.paste(image, (x, y))
            draw.text((x, y - 19), f"{i + 1:02}", fill="#162b3d")
        sheet.save(output / "preview.png")
        print(f"Built {len(doc)} pages with {len(pages)} presenter entries in {output}")
        print("Structural checks passed. Inspect figures, fonts, overlaps, and scientific claims manually.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", type=Path, help="Directory containing main.typ and theme.typ")
    parser.add_argument("--output-dir", type=Path, help="New directory; default: DECK/build")
    parser.add_argument("--expected-pages", type=int, help="Override simple-source page counting")
    parser.add_argument("--width", type=float, default=960, help="Expected PDF width in points")
    parser.add_argument("--height", type=float, default=540, help="Expected PDF height in points")
    parser.add_argument("--allow-missing-notes", action="store_true")
    parser.add_argument("--draft", action="store_true", help="Allow instructional placeholders in intermediate builds")
    args = parser.parse_args()
    try:
        build(args)
    except (ValueError, FileExistsError) as error:
        parser.exit(1, f"Build failed: {error}\n")


if __name__ == "__main__":
    main()
