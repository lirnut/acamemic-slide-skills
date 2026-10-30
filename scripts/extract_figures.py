"""Render unchanged local PDF crops from a JSON manifest; record provenance.

Requires pymupdf. Pages are 1-based; rectangles are normalized to the visible
rotated page, origin top-left. Sources are never modified. No downloads occur.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re

import pymupdf


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def extract(manifest, output, dpi):
    if dpi <= 0:
        raise ValueError("DPI must be positive")
    manifest = manifest.resolve()
    spec = json.loads(manifest.read_text(encoding="utf-8"))
    jobs = []
    names = set()
    for crop in spec["crops"]:
        name = crop["name"]
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", name) or name in names:
            raise ValueError(f"Invalid or duplicate crop name: {name!r}")
        names.add(name)
        source = spec["sources"][crop["source"]]
        pdf = (manifest.parent / source["pdf"]).resolve()
        rect = crop["rect"]
        if len(rect) != 4 or not (0 <= rect[0] < rect[2] <= 1 and 0 <= rect[1] < rect[3] <= 1):
            raise ValueError(f"Invalid normalized rectangle for {name}")
        with pymupdf.open(pdf) as doc:
            page = crop["page"]
            if type(page) is not int or not 1 <= page <= len(doc):
                raise ValueError(f"Invalid 1-based PDF page for {name}")
        jobs.append((crop, source, pdf))
    if not jobs:
        raise ValueError("Manifest has no crops")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []
    for crop, source, pdf in jobs:
        target = output / f"{crop['name']}.png"
        with pymupdf.open(pdf) as doc:
            page = doc[crop["page"] - 1]
            x0, y0, x1, y1 = crop["rect"]
            bounds = page.rect
            clip = pymupdf.Rect(bounds.x0 + x0 * bounds.width,
                               bounds.y0 + y0 * bounds.height,
                               bounds.x0 + x1 * bounds.width,
                               bounds.y0 + y1 * bounds.height)
            page.get_pixmap(clip=clip, dpi=dpi, alpha=False).save(target)
        records.append({**crop, "source_metadata": source, "resolved_pdf": str(pdf),
                        "pdf_sha256": digest(pdf), "output": target.name,
                        "output_sha256": digest(target), "dpi": dpi,
                        "pymupdf_version": pymupdf.VersionBind})
    (output / "sources.json").write_text(
        json.dumps({"crops": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(records)} crops to {output}; inspect every crop visually.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path, help="New directory; refuses overwrite")
    parser.add_argument("--dpi", type=int, default=200)
    args = parser.parse_args()
    try:
        extract(args.manifest, args.output_dir, args.dpi)
    except (ValueError, FileExistsError) as error:
        parser.exit(1, f"Crop extraction failed: {error}\n")


if __name__ == "__main__":
    main()
