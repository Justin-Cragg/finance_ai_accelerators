---
name: finance-ai-workshop-prep
argument-hint: "[create-process-map | update-process-map] [process, sources, session]"
description: Run the pre-workshop stage of a Finance AI discovery engagement. After the kick-off call it creates the client's engagement workbook (C2), a tailored intake questionnaire (A2) and the workshop pre-read (A4) from the templates bundled in this skill. When the intake comes back it loads the answers into C2, drafts a process card per process, matches candidate use cases, lists the gaps, and produces the hypothesis pack (A5), a tailored question bank and a follow-up request. Use for "set up the engagement", "prepare the intake", "the intake is back", "prep the workshop" or "build the hypothesis pack" on a Finance AI engagement.
---

# Finance AI workshop prep (S1)

Two stages, run at different times. Everything this skill writes is a **draft for review**: records are set to `Draft (AI)`, and nothing goes to the client until a consultant has reviewed it.

**All templates are in this skill's `assets/` folder.** Never ask the user to supply a template, and never look for one elsewhere. Copy from `assets/`, don't edit the files in it.

## What's in the skill

| Path | What it is |
| --- | --- |
| `assets/C2_Engagement_Workbook.xlsx` | Engagement workbook template (one tab per data-model entity, scoring, matrix) |
| `assets/A2_Intake_Questionnaire.xlsx` | Client intake template (About you, EXP, BNK, CFF, Other process, Documents) |
| `assets/A4_Workshop_Agenda_and_Preread.md` | Client agenda and pre-read template |
| `assets/A5_Hypothesis_Pack_Template.md` | Hypothesis pack structure |
| `references/A1_Kickoff_Call_Guide.md` | Kick-off questions (KO) and the C2 field each answer goes to |
| `references/F0_data_model.md` | Every field, its source tag and whether the report or the build needs it |
| `references/question_bank.csv` | B2 master; the `F0 field` column says where each answer goes |
| `references/use_case_library.md` | C1 entries with tier, prerequisites and value drivers |
| `references/B5_cards.md` | Art-of-the-possible cards to choose for each session |
| `references/D3_data_protocol.md` | Data handling rules that apply to everything below |
| `scripts/new_engagement.py` | Creates the client's C2 and tailored A2 from the templates |
| `scripts/c2_io.py` | Reads the intake; reads and writes C2 safely (`-h` for commands) |
| `scripts/tailor_bank.py` | Builds the tailored question bank .xlsx |
| `assets/process_mapper.html` | B6 Process Mapper, to open draft maps (hosted copy: https://claude.ai/artifact/X2aDGZEPKkpi4wFndP8Jf7) |
| `references/process_map_outline.md` | The outline format Claude writes to draft a process map |
| `scripts/draft_map.py` | Lays out and checks an outline and writes a file the mapper imports |
| `scripts/update_map.py` | Turns an existing map into an outline, and merges a revised outline back into it |
| `scripts/map_to_c2.py` | `--mermaid` previews a drafted map |

## Rules (both stages)

- **Never invent a number, a system, a feature or a fact.** If a source doesn't say it, leave the field empty and add it to the gap list. A client estimate is recorded as their estimate.
- **Every record needs evidence**: an Evidence record (`source_type` Intake answer or Document; `reference` = question ID or document name) listed in the record's `evidence_ids`. Kick-off answers use `source_type` Scribe note with `reference` = the KO question ID.
- **Roles, not names**, in processes, pain points and use cases. Names belong only on the Attendees tab.
- **Personal data (D3):** don't copy employee names, card numbers or personal spending details from sample files. Summarise patterns instead.
- **Configure first:** when matching use cases, list T1 library entries before T2, and T3 only if nothing else fits.
- **Confidence:** High = stated plainly; Medium = inferred from a document or sample data; Low = an indirect hint (goes in the gap list as "Confirm").
- If C2 lives in SharePoint or OneDrive, work on a downloaded copy and tell the user to upload the result.

## Stage 1: kick-off pack (after the kick-off call)

Inputs: the kick-off notes (or the filled A1 guide), the client name, a short engagement code, the processes in scope, the intake return date and the Deloitte contact.

1. **Map scope to modules.** Expenses → EXP, bank statements → BNK, cash flow forecasting → CFF. Every other process (e.g. AP invoices, month-end close) uses the generic module, one "Other process" tab each.
2. **Create the files:** `python3 scripts/new_engagement.py --client "<name>" --code <CODE> --modules EXP,BNK --other "AP invoices;Month-end close" --return-by <date> --contact "<name, email>" --outdir <folder>`.
3. **Load the kick-off answers into C2.** Use `references/A1_Kickoff_Call_Guide.md` to place each KO answer in its field (objectives, success measures, scope, constraints, planned system changes, recording consent, workshop dates; attendees and their roles on the Attendees tab). Write a records JSON and run `python3 scripts/c2_io.py append <C2> records.json`.
4. **Draft the A4 pre-read** from `assets/A4_Workshop_Agenda_and_Preread.md`: fill client, dates, sessions in scope (delete the others), attendees by role, and the Deloitte contact. Leave anything not known in [brackets].
5. **Output:** the C2 workbook, the A2 intake (check the tab list printed by the script matches scope), the A4 draft, and a list of kick-off questions still unanswered. Flag at once if recording consent is No or Not yet asked, or if a planned system change could affect a process in scope.

## Stage 2: workshop prep (when the intake comes back)

Inputs: the returned A2, the documents and sample data the client sent, and the client's C2 from stage 1. If there is no C2 yet, run stage 1 first.

1. **Read the intake.** `python3 scripts/c2_io.py intake <A2.xlsx> > intake.json`. Answers come grouped by tab. "Other process" tabs carry the process name as their tab title; GEN question IDs repeat across them, so keep answers grouped by tab.
2. **Read the documents.** Pull out facts that fill fields (policy limits, approval matrix, category mapping, account list, statement formats, forecast inputs). For sample data, measure what you can (volumes per month, share of lines with missing receipts or recoding, statement formats) and say how you measured it.
3. **Map answers to records** using the question bank's `F0 field` column:
   - CORE-07 to CORE-12 → Systems rows (`edition_modules`, `admin`, `api_access`, `sandbox`)
   - Module answers → one Processes row per process (`P-01` onward; `module` = EXP, BNK, CFF or GEN; for GEN the name comes from the tab title)
   - "How does X get into Y" answers → Data flows rows
   - CORE-18 and any pain point mentioned → Pain points rows
   - Documents tab → Documents rows (`personal_data` from the client's answer)
   - Unanswered required questions → Open questions rows (owner = the "Who answers" role)
4. **Write to C2:** build a records JSON using only row-2 field keys, then `python3 scripts/c2_io.py append <C2> records.json --out <C2_prep.xlsx>`. Fix any errors it reports and re-run.
5. **Find the gaps:** `python3 scripts/c2_io.py blank <C2_prep.xlsx>` lists required fields still empty, with the questions that fill them. Build-required gaps come first.
6. **Match candidate use cases** from `references/use_case_library.md`. Keep an entry only if something in the intake points to it. For each, state what must be true for it to work and whether the intake already confirms it. Pick two or three cards per session from `references/B5_cards.md`.
7. **Tailor the question bank:** write a plan JSON (client, modules, status overrides, a client-specific probe for each gap, draft values), then `python3 scripts/tailor_bank.py references/question_bank.csv intake.json plan.json <Tailored_Question_Bank.xlsx>`.
8. **Draft the process maps (recommended):** run the `create-process-map` mode below for each process in scope, from the intake answers and the procedures the client sent, so each session opens with a draft on screen.
9. **Write the hypothesis pack** from `assets/A5_Hypothesis_Pack_Template.md`, using only pre-workshop sources. Fill every table from the C2 records you wrote, with confidence and evidence IDs. Leave a cell blank when no source covers it; it then appears in the priority gaps. For each process, also list the swimlanes (roles) to set up in the Process Mapper (B6) before the session.
10. **Draft the follow-up request** to the client: unanswered questions and missing documents, grouped by the role who should answer. Do not send it.

**Stage 2 output:** the updated C2 (`*_prep.xlsx`) with a count of records by tab, the draft process maps, the hypothesis pack, the tailored question bank, the follow-up draft, and anything you couldn't place.

## Optional argument: `create-process-map`

Use this mode when the skill is invoked with `create-process-map` (for example `/finance-ai-workshop-prep create-process-map P-02 Goods receipt from the AP procedure and intake`), or whenever someone asks Claude to create, draft or generate a process map. Everything after the argument is the brief: which process or processes, the sources to use, the session code and any roles to use as swimlanes. If no sources are named, ask for them: the intake answers for the process, any procedures, checklists or policies the client sent (DR-06, DR-19), and sample data.

1. **Read the sources** in full. Note where each step comes from (document and page, or session and timestamp).
2. **Write an outline** in the format in `references/process_map_outline.md`: one process per process asked for, lanes as roles, every step with its `lane`, `next` and `source`, decisions as `xor`/`and`/`or` nodes with labelled branches, `subprocess` where a step holds several steps, and `link` where the work continues in another process. Put anything inferred, unclear or contradictory in `confirm`. Never invent volumes, minutes, limits or owners.
3. **Lay it out and check it:** `python3 scripts/draft_map.py outline.json --out <ENGAGEMENT>_<PROCESS-ID>_draft_map.json` (add `--existing <earlier export>.json` so links can point at maps already drawn). Fix every warning it prints (a step with no next step, a decision with one branch, a link that doesn't resolve) and re-run.
4. **Show it:** give a short summary per map (steps, decisions, sub-processes, links, items to confirm) and the Mermaid preview from `python3 scripts/map_to_c2.py <draft_map>.json --mermaid`.
5. **Deliver the file** and tell the user how to open it: in the Process Mapper (hosted: https://claude.ai/artifact/X2aDGZEPKkpi4wFndP8Jf7, or `assets/process_mapper.html` opened in a browser), click **Import** and choose the file. Every map starts with a comment saying it is a Claude draft, and every `confirm` item is an open comment marked AI.

The draft is not written to the C2 workbook. The workshop confirms or corrects the map on screen, and the confirmed export is loaded into C2 afterwards with `map_to_c2.py` (skill S2).

## Optional argument: `update-process-map`

Use this mode when the skill is invoked with `update-process-map` (for example `/finance-ai-workshop-prep update-process-map P-01 add the three-way match the AP lead described`), or whenever someone asks Claude to change, correct or extend a map that already exists. You need the map as an export from the mapper (**Export → Download JSON**); if you don't have it, ask for it. You also need what to change: an instruction, notes or a transcript.

1. `python3 scripts/update_map.py outline <export>.json [--map <process ID>] --out current.json`
2. Revise the outline per "Updating an existing map" in `references/process_map_outline.md`: keep the ids of kept steps, use `new1`, `new2`… for new ones, list every change in `changes`, and answer open comments in `resolve` only where the source clearly does.
3. `python3 scripts/update_map.py apply <export>.json revised.json --out <ENGAGEMENT>_<PROCESS-ID>_update.json`. Fix any warnings and re-run.
4. Report what changed (from the script's summary) and give the Mermaid preview from `python3 scripts/map_to_c2.py <update>.json --mermaid`.
5. Deliver the file. In the mapper, **Import** replaces the map in place, and the changes are listed in a comment on the start node. In the hosted mapper the same thing can be done directly with **Draft with Claude → Update this map**.


End either stage by reminding the reviewer to change `record_status` from `Draft (AI)` to `Reviewed` once checked.
