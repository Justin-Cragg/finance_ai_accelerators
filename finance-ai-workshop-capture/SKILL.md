---
name: finance-ai-workshop-capture
argument-hint: "[create-process-map | update-process-map] [process, sources, session]"
description: Run and capture a Finance AI discovery workshop session. Sets up the live Process Mapper (B6) and scribe sheet (B3) bundled in this skill, then turns the session's process map export, Teams transcript, scribe notes and photos into structured records in the C2 engagement workbook, each with an evidence reference, checks the session against the exit checklist, and drafts the gap list and client follow-up. Use for "set up the mapping session", "capture the session", "process the transcript", "load the process map" or "what did we miss in W2".
---

# Finance AI workshop capture (S2)

Used before a session (set-up), between sessions (for example at the break, to spot gaps for the second half) and after each session. Everything it writes to C2 is a **draft for review** (`record_status` = `Draft (AI)`).

**All templates and tools are in this skill.** Never ask the user to supply them.

## What's in the skill

| Path | What it is |
| --- | --- |
| `assets/process_mapper.html` | B6 Process Mapper: live swimlane mapping (steps with descriptions and systems, decisions, AND/OR, sub-processes, links between processes, comments, flags). Opens in any browser, no install, no network needed. Hosted copy: https://claude.ai/artifact/X2aDGZEPKkpi4wFndP8Jf7 |
| `assets/B3_Scribe_Capture_Sheet.md` | Scribe sheet template |
| `assets/C2_Engagement_Workbook.xlsx` | Blank workbook, only if the engagement has none yet (normally use the client's C2 from S1) |
| `references/B1_Facilitator_Guide.md` | Session flow and roles |
| `references/exit_checklist.md` | B4 build-ready minimum per module (GEN for a process without its own module) |
| `references/question_bank.csv` | Module and SOL questions, mapped to fields |
| `references/F0_data_model.md` | Fields, source tags, required-for |
| `references/use_case_library.md` | To tag ideas raised in the room to a library entry |
| `references/D3_data_protocol.md` | Data handling rules |
| `scripts/map_to_c2.py` | Turns a Process Mapper JSON export (one map with its sub-processes, or all maps in the engagement) into C2 records, and Mermaid with `--mermaid` |
| `references/process_map_outline.md` | The outline format Claude writes to draft a process map |
| `scripts/draft_map.py` | Lays out and checks an outline and writes a file the mapper imports |
| `scripts/update_map.py` | Turns an existing map into an outline, and merges a revised outline back into it |
| `scripts/transcript.py` | Normalises a Teams transcript to `[hh:mm:ss] Speaker: text` |
| `scripts/c2_io.py` | Reads and writes C2 safely (`append`, `update`, `blank`, `read`) |

## Rules

- **The process map is the record of the flow.** Steps, sequence, branches and who does what come from the map the client watched being drawn and agreed. Use the transcript and notes for what the map doesn't hold: volumes, timings, rules, reasons, exceptions. If they contradict the map, report the conflict; don't silently change either.
- **Evidence for everything.** Map-derived records cite the map node (`map_to_c2.py` does this). Transcript-derived records cite session + timestamp (e.g. `W2 00:14:32`) with a short paraphrase or a quote under 15 words. No source, no record.
- **Only what was said or drawn.** No values from general knowledge or the library. Estimates are recorded as estimates. Conflicting numbers → an open question.
- **Roles, not names**, in every record except Attendees. Swimlanes should already be roles.
- **Personal data (D3):** leave out names of employees discussed, card numbers and personal spending details.
- **Don't overwrite reviewed data.** `update` fills empty fields only and reports conflicts; don't use `--overwrite` unless the user says so.
- **Confidence:** High = drawn on the map and confirmed, or stated clearly and confirmed; Medium = stated once; Low = implied or unclear audio.

## Before the session: set-up

1. Give the team the mapper: the hosted link above, or copy `assets/process_mapper.html` to the engagement folder and open it in a browser (it saves in that browser and exports files).
2. From the hypothesis pack (A5), list the swimlanes (roles, plus a lane for each key system if useful) and the process ID, so the scribe can click **New map** with them ready.
3. Copy `assets/B3_Scribe_Capture_Sheet.md` for the session and fill its header.

## After the session (or at the break)

1. **Collect inputs:** the map export JSON (Export → "Download JSON: all maps in this engagement" is simplest; it carries every process, its sub-processes and the links between them), the Teams transcript (.vtt or .docx), the B3 sheet, photos, and the client's current C2.
2. **Load the map:** `python3 scripts/map_to_c2.py <map.json> --c2 <C2.xlsx>`. It writes `_append.json`, `_update.json` and `_summary.md` beside the map. Each top-level map is one C2 process; sub-process steps are folded under their parent step with nested numbering (2.1, 2.2). It fills the process fields (steps, participants, manual touchpoints, controls, decision rules, systems, rework loops, linked processes in both directions), creates a pain point per flagged node and an open question per unresolved comment, and lists step descriptions, notes, ideas and candidate data flows in the summary for you to place. It is safe to re-run; it skips records it already created.
3. **Normalise the transcript:** `python3 scripts/transcript.py <file> --session W2 > W2.txt`. Read it in full with the B3 sheet and the map summary beside it. Look at each photo.
4. **Read the current state:** `python3 scripts/c2_io.py read <C2.xlsx>`, so you know existing records and the next IDs.
5. **Add what the map doesn't hold**, from the transcript and notes:
   - Volume and unit, seasonality, hours per cycle, cycles per year, manual share, timing → `update` on the process
   - Impact, frequency and the raising role for each pain point from the map; any pain point said but not flagged on the map → new Pain points row
   - Systems or data flows not yet recorded (use the map summary's candidate data flows) → Systems / Data flows rows
   - SOL answers: unused features → `system.unused_features`; admin and change speed → `system.admin`; appetite and spend → `engagement.constraints` (append, don't replace); run-state owner and human review → notes for the use case; access and sample data → Build requirements rows
   - Decisions and follow-ups → Open questions rows with owner role and due date if agreed
6. **Write:** run `c2_io.py append` with the map's `_append.json` and your own new records, then `c2_io.py update` with the map's `_update.json` and your own updates, using `--out <C2_W2.xlsx>`. Fix errors and re-run.
7. **Exit checklist:** for the module and SOL in `references/exit_checklist.md`, mark each item Captured (with evidence ID), Partly, or Missing; `python3 scripts/c2_io.py blank <C2_W2.xlsx>` confirms what is still empty.
8. **Follow-ups:** missing and partly captured items become client questions (plain language, grouped by role) and, if run at the break, a short list for the facilitator.

## Output

1. The updated C2 workbook, with counts of records appended and fields filled by tab
2. A session summary: what was captured, the exit checklist status, conflicts between map, transcript and existing data, and ideas raised (with library refs)
3. The gap list for the next session or the second half
4. A follow-up email draft to the client (not sent)
5. The maps' Mermaid text (`map_to_c2.py <export.json> --mermaid`, one flowchart per map and sub-process) for the report's Appendix B

End by reminding the reviewer to check the drafts against the map and recording, and to set `record_status` to `Reviewed`.

## Optional argument: `create-process-map`

Use this mode when the skill is invoked with `create-process-map` (for example `/finance-ai-workshop-capture create-process-map P-02 Goods receipt from the AP procedure and intake`), or whenever someone asks Claude to create, draft or generate a process map. Everything after the argument is the brief: which process or processes, the sources to use, the session code and any roles to use as swimlanes. If no sources are named, ask for them: the Teams transcript (run `scripts/transcript.py` first), the B3 scribe notes and photos, and any earlier map export of the process.

1. **Read the sources** in full. Note where each step comes from (document and page, or session and timestamp).
2. **Write an outline** in the format in `references/process_map_outline.md`: one process per process asked for, lanes as roles, every step with its `lane`, `next` and `source`, decisions as `xor`/`and`/`or` nodes with labelled branches, `subprocess` where a step holds several steps, and `link` where the work continues in another process. Put anything inferred, unclear or contradictory in `confirm`. Never invent volumes, minutes, limits or owners.
3. **Lay it out and check it:** `python3 scripts/draft_map.py outline.json --out <ENGAGEMENT>_<PROCESS-ID>_draft_map.json` (add `--existing <earlier export>.json` so links can point at maps already drawn). Fix every warning it prints (a step with no next step, a decision with one branch, a link that doesn't resolve) and re-run.
4. **Show it:** give a short summary per map (steps, decisions, sub-processes, links, items to confirm) and the Mermaid preview from `python3 scripts/map_to_c2.py <draft_map>.json --mermaid`.
5. **Deliver the file** and tell the user how to open it: in the Process Mapper (hosted: https://claude.ai/artifact/X2aDGZEPKkpi4wFndP8Jf7, or `assets/process_mapper.html` opened in a browser), click **Import** and choose the file. Every map starts with a comment saying it is a Claude draft, and every `confirm` item is an open comment marked AI.

The draft is not written to the C2 workbook. The workshop confirms or corrects the map on screen, and the confirmed export is loaded into C2 afterwards with `map_to_c2.py` (skill S2).

In this skill the mode is mainly for a session that wasn't mapped live, or to check a live map against what was said: draft from the transcript, give every step its timestamp as `source`, and list where the draft and the live map differ.

## Optional argument: `update-process-map`

Use this mode when the skill is invoked with `update-process-map` (for example `/finance-ai-workshop-capture update-process-map P-01 add the three-way match the AP lead described`), or whenever someone asks Claude to change, correct or extend a map that already exists. You need the map as an export from the mapper (**Export → Download JSON**); if you don't have it, ask for it. You also need what to change: an instruction, notes or a transcript.

1. `python3 scripts/update_map.py outline <export>.json [--map <process ID>] --out current.json`
2. Revise the outline per "Updating an existing map" in `references/process_map_outline.md`: keep the ids of kept steps, use `new1`, `new2`… for new ones, list every change in `changes`, and answer open comments in `resolve` only where the source clearly does.
3. `python3 scripts/update_map.py apply <export>.json revised.json --out <ENGAGEMENT>_<PROCESS-ID>_update.json`. Fix any warnings and re-run.
4. Report what changed (from the script's summary) and give the Mermaid preview from `python3 scripts/map_to_c2.py <update>.json --mermaid`.
5. Deliver the file. In the mapper, **Import** replaces the map in place, and the changes are listed in a comment on the start node. In the hosted mapper the same thing can be done directly with **Draft with Claude → Update this map**.

After a session, this is how to fold in answers to open questions, or corrections from the transcript, into the map the room confirmed.

