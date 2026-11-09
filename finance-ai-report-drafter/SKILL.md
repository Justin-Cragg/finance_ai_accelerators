---
name: finance-ai-report-drafter
description: Draft the Finance AI Discovery & Design Report and the playback deck from a reviewed C2 engagement workbook. Checks the workbook is ready (evidence, scores, tiers, build requirements), then writes report sections 1-11 and the appendices, including the Appendix H build specification for each priority use case, with value workings shown and every claim traced to evidence. Use when someone says "draft the report", "write up the design document", "build the playback deck" for a Finance AI engagement.
---

# Finance AI report drafter (S3)

Drafts the client deliverable after the last workshop. The output is a **draft for review**: the engagement lead edits and approves it, and the QA checklist (D2) is completed before issue.

## Inputs to ask for (if not already given)

1. The C2 engagement workbook, with records reviewed (`record_status` Reviewed or Confirmed) and the Scoring tab complete
2. The Process Mapper (B6) JSON exports for each process, for Appendix B
3. Output format: a Claude Docs doc (default, exports to Word or PDF), or a .docx if the user names Word
4. Whether to draft the playback deck too (default yes)

**All templates are in this skill.** Never ask the user to supply them.

## What's in the skill

| Path | What it is |
| --- | --- |
| `assets/C3_Report_Template.md` | The report template. Follow its section order, tables and source tags exactly; delete guidance lines in the draft |
| `references/playback_deck_outline.md` | Slide-by-slide structure of the C4 playback deck (hosted template: https://claude.ai/artifact/9D7Ne8Vmrm2T4be4UFL3Zs) |
| `references/F0_data_model.md` | Which tab and field feeds each section |
| `references/use_case_library.md` | Tier definitions, typical controls, human-in-the-loop and build steps for sections 6, 9 and Appendix H |
| `references/D3_data_protocol.md` | Data handling rules |
| `scripts/c2_io.py` | `read` for all records, `summary` for totals and quadrants, `blank` for missing required fields |
| `scripts/map_to_c2.py` | `--mermaid` turns a process map export into a Mermaid flowchart for Appendix B |

## Rules

- **Numbers come only from the workbook.** Hours, volumes, scores and counts are read from C2, never estimated in prose. If the workbook was edited by openpyxl and not recalculated, recalculate before reading (calculated cells otherwise read empty).
- **Show the value workings**: volume × minutes per item × automation share ÷ 60, with the inputs, for every use case in sections 6 and 9.
- **Trace every finding.** Each pain point in section 5 shows its evidence reference (session + timestamp, or document). Any statement you can't trace gets an inline `[CHECK: no evidence]` flag; never drop the flag silently.
- **Configure first.** Present T1 options as recommendations in their own right, not as lesser options.
- **Roles, not names**, except Appendix A. No personal data anywhere.
- **Drafts only from reviewed data.** Records still `Draft (AI)` may be used but must be listed in the review notes.
- **Don't decide for the client.** Fees, option choice and dates stay as placeholders unless the workbook or the user gives them.

## Steps

1. **Read.** `python3 scripts/c2_io.py read <C2.xlsx>` and `summary`. Note counts by tab and by record status.
2. **Readiness check before drafting.** List blockers and stop to ask the user if any of these fail:
   - Every pain point has at least one evidence ID
   - Every use case has a delivery tier, a library ref and value inputs
   - Every use case has a Scoring row with all seven scores
   - Every priority use case (quadrant Quick win, or phase Quick win) has Build requirements rows covering access, mapping or configuration, test data and acceptance criteria
   - A run-state owner role is named for each priority use case
   Otherwise list the gaps as review notes and carry on.
3. **Draft sections 2 to 11** from the template, each from its tab: 2 Engagement and Attendees · 3 Systems and Data flows · 4 Processes (one process card each) · 5 Pain points with evidence · 6 Use cases (summary table and one card each) · 7 Scoring, with a value × feasibility matrix drawn from the weighted scores · 8 Readiness · 9 one target-state design per priority use case, with the default RACI from the template · 10 risks from the template, adjusted to the use cases · 11 roadmap and options with fee placeholders.
4. **Draft the appendices.** A attendees · B one process map per process, followed by its sub-process maps: render them with `python3 scripts/map_to_c2.py <export.json> --mermaid` (or use the images the team exported from the mapper), then the numbered steps from `process.steps` and the step descriptions from the export (each node's `description`); note linked processes (`process.linked_processes`) under each map; if a process has no map, use `process.steps` alone and note it · C full scoring workings · D backlog (use cases not prioritised, with the reason) · E assumptions, limitations and open questions not yet closed · F documents received · H one build specification per priority use case from its Build requirements rows; anything Requested or Blocked is also listed as a readiness action in section 8.
5. **Write the executive summary last**: the recommendation and the value first, three headline findings, the priority table, readiness in one sentence, and the decision requested.
6. **Playback deck.** If the Slides artifact type is available, create a deck following `playback_deck_outline.md`, filled with the same numbers as the report. Otherwise produce a .pptx with the pptx skill.
7. **Self-check.** Every number in the executive summary and deck matches the workbook; every UC, PP and BR ID cited exists; no `[CHECK]` flags remain unlisted.

## Output

1. The draft report
2. The draft playback deck
3. Review notes: blockers found in step 2, `[CHECK]` flags, records still Draft (AI), and the D2 QA items the reviewer must complete (independence clearance, data handling, partner review)
