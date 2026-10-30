---
name: academic-slides
description: Create and revise evidence-grounded academic presentations from research papers, including literature group meetings, journal clubs, and multi-paper research talks. Use for paper selection, scientific storylines, original figure explanations, source audits, editable Typst/Touying slides, Chinese speaker notes, and rendered-slide quality checks. 用于论文组会、文献汇报、学术幻灯片及逐页讲稿。
---

# Academic slides

Build a traceable scientific argument, not merely a polished deck. Prefer source fidelity, understandable experiments, and editable source over narrative elegance or decorative layouts.

## Defaults and boundaries

- Follow explicit user requirements first. Otherwise use English audience text with original technical terminology, Chinese oral scripts retaining English technical terms, and a restrained academic layout. Impose no default duration, page limit, or seconds-per-slide rule.
- Default to `@preview/sci-brain-slides:0.1.0`, `academic`, with simple Touying heading-based source. Keep content in `main.typ`, appearance in `theme.typ`, and notes in per-page `#speaker-note[...]` blocks.
- Treat language, package, and layout as overridable defaults, not scientific rules. Only apply a duration constraint when the user supplies one; otherwise organize by the evidence and explanation needed. Do not invent a timed schedule.
- Read the existing project and preserve user work before editing. Do not modify library records or source PDFs merely to prepare slides.

## OpenCode and self-contained operation

Read [opencode.md](references/opencode.md) for discovery, invocation, and resource resolution. Resolve bundled paths from this skill's base directory supplied by OpenCode, not from the active deck directory. The instructions, template, and scripts here must work in a new project without previous conversations, neighboring slide files, private PDFs, personal virtual environments, other installed skills, or a particular MCP server. Other skills may supplement this one but are never required.

Distinguish **independence from previous project data** from **scientific evidence**: acquire the current task's papers/data from user-provided files or verifiable authorized sources. Never generate empirical evidence to fill a missing source. If only a topic is given, find and inspect candidate full texts; if research access fails, report missing sources and produce an explicitly incomplete outline instead of fictional findings.

Read [production-workflow.md](references/production-workflow.md) and follow its planning fields, acceptance checks, and repair loop. Populate the bundled empty audit template from the current task rather than copying a previous deck's claims.

## Workflow and quality gates

### 1. Establish the question before selecting papers

Determine audience, purpose, available full texts, and output format. Record a duration only if supplied. Reuse known preferences rather than re-asking settled questions; proceed with stated assumptions for nonblocking choices.

Read [paper-selection.md](references/paper-selection.md). Draft a small selection matrix: short title, actual research question, task, evidence, and role in the talk. Prefer a genuinely shared question with heterogeneous evidence. Reject a weak connection rather than inventing a unifying mechanism. Get agreement on a materially changed paper selection before building the whole deck.

### 2. Audit evidence before writing claims

Read [evidence-and-figures.md](references/evidence-and-figures.md). Use abstracts for screening only. Inspect methods, figure captions, results, discussion, conclusions, and relevant supplements for final claims.

Create a separate `claim-sources.md`: slide/claim, exact source version and location, experimental conditions, metric/unit/denominator, evidence type, and interpretation boundary. Distinguish observation, author interpretation, modeling assumption, fitted statistical explanation, and validated causal evidence. Never upgrade one category into another.

When a source is unavailable, flag the gap; omit or qualify unsupported claims. Do not fabricate quotes, numbers, figures, or cross-paper conclusions.

### 3. Plan the explanation, not a fixed number of pages

Use **Problem → Approach → Results** within each study; close with author-attributed interpretation and scope. Use short paper titles in overview tables and study headings, preserving published capitalization within titles.

Explain the task before showing effect sizes. For complex studies, include the actual process: setup → observed example → individual/group trajectories → aggregate results → model validation. Do not delete essential update-process figures just to meet a page target.

If the user supplies a duration, allocate it by explanation burden and rebalance after adding evidence. Label estimates as estimates. Otherwise omit timed schedules and do not truncate essential evidence to an assumed length.

### 4. Assemble readable, editable slides

For Typst, read [typst-workflow.md](references/typst-workflow.md). The bundled starter and reference are sufficient; optionally load `typst-touying` if available for features beyond the starter. Use `assets/typst-template/` as a starter in a **new** output directory; do not overwrite an existing presentation with the template.

- Keep a neutral background, restrained accent colors, consistent type scale, and minimal decoration. Prefer original paper figures and useful experimental details over ornamental cards.
- Give each page one explanatory job. Keep slide titles visible and center body content vertically when appropriate. Split crowded pages before shrinking text.
- Put concise author/year/section/figure/page references in a fixed footer. Keep extraction explanations and labels such as “Verbatim” or “Paraphrase” out of audience slides.
- Preserve original figure data. Use rectangular PDF crops with provenance; inspect axes, legends, and neighboring-panel fragments visually.
- Write a complete, editable Chinese oral script per page. Explain axes, units, colors, sample/trajectory denominator, task/model conditions, takeaway, and limits. Do not merely translate bullets.
- Export readable scripts and presenter metadata from source notes; never maintain conflicting copies manually.

### 5. Build, inspect, and iterate

Use the bundled tools; run `--help` for options:

```sh
python <skill-dir>/scripts/build.py <deck-dir>
python <skill-dir>/scripts/extract_figures.py <manifest.json> --output-dir <asset-dir>
```

Check Python and dependencies before running; create an isolated environment if needed using the Typst reference rather than assuming a personal installation. The build checks page count, dimensions, text bounds, note coverage, and common unfinished placeholders and generates PDF, pdfpc metadata, Markdown scripts, and previews. Use `--draft` only for instructional-template/intermediate builds. It does **not** certify scientific correctness or visual quality.

Inspect the contact sheet and every individual page, especially cropped figures and dense/table/formula pages. Check readability, real fonts, footer clearance, unexpected blank/overflow pages, cropping, and note leakage. Read the final talk against the source audit. Fix defects, rebuild in a new output directory, and inspect changed pages plus the overall deck again. Stop only after no blocking defects remain; otherwise explicitly deliver a draft with outstanding blockers. Do not claim visual inspection from compilation alone.

## Delivery

Provide editable source, audience PDF, original-figure provenance manifest, source audit, per-page notes, and previews as applicable. Link the main outputs and state remaining limitations briefly. When answering “what does page N mean?”, confirm physical PDF page versus displayed slide number; explain the actual figure before revising the deck unasked.
