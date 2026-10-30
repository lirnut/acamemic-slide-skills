# Reproducible production from a fresh task

## 1. Establish inputs without a prior project

Record a compact working brief: audience/background, talk purpose, topic/question, requested language and format, supplied sources, user-specified constraints, and unresolved decisions. Do not invent a duration when none is provided.

| Available input | Next action |
|---|---|
| Topic only | Search candidate papers, obtain authorized full texts, verify selection against the common question. |
| Papers | Inspect exact versions, methods, captions, results, conclusions, and relevant supplements. |
| Existing deck | Read source and render the original before editing; preserve intentional user layout/content. |
| Dataset plus findings | Verify provenance, definitions, units, and calculations; mark newly calculated results as presenter analysis. |
| Inaccessible source | State the gap; request access or draft only a clearly incomplete structure. |

Create project-local `papers/` and `assets/` only as needed. Do not assume old files or a personal research library exist.

## 2. Build an evidence-backed page plan

For each planned page record:

| ID | Study/role | Question or takeaway | Supporting source/panel | Necessary setup | Audience visual/text | Notes must explain |
|---|---|---|---|---|---|---|

Require every empirical takeaway to have evidence before layout. Use neutral question/setup titles when a result is not yet established. Decide page boundaries based on conceptual load, not a quota. Keep essential method definitions beside or immediately before their results.

Choose layouts by the content's job: task/process, original figure with explanation, comparison table, equation with variable definitions, or separate conclusions. Do not reuse title-plus-bullets merely because it is easy. Do not add decorative visuals to satisfy an image quota.

## 3. Write from the audit, then lay out

Use `assets/source-audit-template.md` as a blank schema. For a result, write the supported observation with its conditions, attach its source, then decide how little text can appear without losing meaning. Keep detailed reading instructions and interpretation boundaries in speaker notes. Native tables/equations remain editable; paper figures remain unchanged.

For complex figures, select legible panels, preserve their identities, and explain the selection. Split across pages rather than showing a full-page paper screenshot with unreadable labels. Do not change data or redraw empirical figures from memory.

## 4. Apply three independent acceptance gates

**Evidence gate**
- Every borrowed figure, number, quotation, and substantive claim has a verified source/version/location.
- Units, denominators, baselines, uncertainty definitions, and conditions are correct.
- Observations, assumptions, author interpretations, and fitted explanations remain distinct.

**Communication gate**
- A listener can understand the task before interpreting the result.
- Each page has one explanatory job and an identifiable evidence-supported takeaway where appropriate.
- Notes explain the figure rather than merely translating bullets.
- Transitions do not assert an unsupported shared mechanism.

**Artifact gate**
- Final build passes structural checks without draft bypasses.
- Every page has been visually inspected; no placeholders, clipped labels, overlap, note leakage, or unreadable figures remain.
- Source, PDF, notes, citations, and page numbering agree.
- No timed schedule is added unless requested; a supplied duration constraint is addressed honestly.

## 5. Repair and report

For each defect identify its page and gate, fix the underlying source, and rebuild. Recheck scientific wording after layout shortening and note/page alignment after insertions. Do not fix a count failure by redefining the expected page count to match unintended overflow. Do not hide a content defect with clipping or tiny text.

If a gate cannot pass, state the blocker and deliver an explicitly unfinished draft. Never promise uniformly excellent outcomes from instructions alone: the workflow improves repeatability, but source access, evidence quality, rendering, and actual review remain necessary.

## Skill maintenance check

Run `scripts/self_test.py` with the documented dependencies to test the bundled template, synthetic PDF crop/provenance, and failure guards without any previous slides or real paper. This tests tooling, not the scientific/visual merit of a future talk. Re-run after script/template changes.
