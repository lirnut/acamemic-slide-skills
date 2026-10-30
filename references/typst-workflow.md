# Editable Typst workflow

## Starter and environment

Copy `assets/typst-template/main.typ` and `theme.typ` into a new deck directory. Replace the instructional placeholder text with audited content. Do not treat the template's examples as research findings.

The starter uses `@preview/sci-brain-slides:0.1.0` with its academic theme. A tested Python environment uses `typst==0.15.0`, `pymupdf==2.0`, and `pillow==13.0.0`. Use a virtual environment or `uv run --with ...`; no personal venv paths are required. First compilation may need network access for Typst packages. Check that Noto Sans is installed; choose an actually installed sans-serif alternative if not.

Check `python --version` (Python 3.11+ for these scripts). Prefer the following portable execution when `uv` is available:

```sh
uv run --with typst==0.15.0 --with pymupdf==2.0 --with pillow==13.0.0 python <skill-dir>/scripts/build.py <deck-dir>
```

Otherwise create an isolated environment in a new task-owned directory with `python -m venv <env-dir>`, then run `<env-dir>/bin/python -m pip install typst==0.15.0 pymupdf==2.0 pillow==13.0.0` and use that interpreter. On Windows use `Scripts/python.exe`. Do not assume packages, fonts, downloads, or executables exist; report blocked installation rather than claiming a successful build.

For template testing use `--draft`, because its instructional placeholders must fail a final build. For a deliverable remove placeholders and run without `--draft`. The placeholder detector is heuristic: review literal matches in legitimate quotations before changing scientific wording. Run `<skill-dir>/scripts/self_test.py` under the same environment for self-contained tool regression checks.

```sh
python <skill-dir>/scripts/build.py <deck-dir>
```

The default counting convention is one explicit `#title-slide(` plus one page for each `==` heading in `main.typ`. It deliberately excludes animations, manual breaks, and multi-file heading expansion. Supply `--expected-pages N` for those layouts and verify the expected count independently; do not simply set N to the overflowing PDF's current count. Supply `--allow-missing-notes` only for an intentional intermediate draft.

The build uses a fresh output directory each run (`<deck-dir>/build` by default, or `--output-dir`) to avoid stale preview pages. It refuses an existing output directory; choose a new one rather than deleting user files. It exports `slides.pdf`, `slides.pdfpc`, `speech-script.md`, `preview.png`, and individual previews.

## Source conventions

- Use `==` for each page, native `figure` and `table`, and the theme's `twocol` / `spread` layouts.
- Edit appearance in `theme.typ`; keep page-specific content in `main.typ`.
- Keep four or five consistent type roles. Use weight rather than arbitrary new font sizes.
- Use `#cite[...]` once per page, combining multiple references in that block. Put the title-page citation inside `title-slide`'s `extra`.
- Put `#speaker-note[...]` after the slide it describes. Edit that source, not the exported Markdown or pdfpc JSON.
- Use physical page numbers in scripts/audits or explicitly distinguish them from the displayed counter, which may exclude the cover.

## Known failure modes

- Do not assume package API compatibility. `academic` rejects `primary`; that option requires the package's `brand` theme. Verify actual APIs before adding configuration.
- Use `config-page`, not bare `set page`, for Touying page settings.
- Match footer metadata using `here().page()` and `it.location().page()`, not a logical page counter that may skip the cover.
- Metadata placed after an explicit title slide can create an unintended blank page; keep cover references inside `extra`.
- Successful compilation can still create overflow pages. Compare intended and actual counts.
- Font fallback can silently change the design. Inspect rendered fonts and glyph coverage.
- Text-bounds tests cannot detect every overlap, invisible notes, figure clipping, or tiny labels. Inspect rendered pages.
- Do not conceal content with clipping just to satisfy bounds checks.

## Delivery gate

Inspect the contact sheet for pacing and consistency; open each figure/table/formula page at readable size. Confirm footer clearance, source-note alignment, actual dimensions, no extra/blank pages, no notes visible to the audience, and no scientific omissions introduced during layout changes. Re-run the build after the final edit. Describe only checks actually performed.
