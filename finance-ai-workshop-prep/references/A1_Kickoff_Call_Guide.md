# A1 – Kick-off Call Guide

A 30–45 minute call with the sponsor before the intake goes out. It does three things: it fills the Engagement and Attendees tabs of the C2 workbook, it decides which intake tabs (A2) to send, and it sets up the sessions (invitations, logins and recording consent).

*Guidance: run it with the sponsor and, if possible, the financial controller. Share no solution ideas yet; the aim is to listen and scope. The questions below are the KO module of the B2 question bank; each answer goes into the F0 field shown.*

## Before the call

- [ ] Engagement letter signed and independence clearance confirmed (D2)
- [ ] C2 engagement workbook created from the template, Engagement tab open
- [ ] List of available process modules to hand (EXP, BNK, CFF; GEN for anything else)

## Agenda

| Time | Topic | Questions |
| --- | --- | --- |
| 5 min | Introductions, purpose, how the next 3–4 weeks run | – |
| 10 min | Objectives and what good looks like | KO-01 to KO-03 |
| 10 min | Scope | KO-04 to KO-06 |
| 5 min | Constraints and appetite | KO-07 to KO-09 |
| 10 min | People and logistics | KO-10 to KO-12, KO-15 |
| 5 min | Recording and data, next steps | KO-13, KO-14 |

## Questions and where the answers go

**Objectives**

| ID | Question | Probe | Answer goes to (C2) |
| --- | --- | --- | --- |
| KO-01 | What made you want to do this now? | A recent incident, a new hire, a board ask? | Engagement: `engagement.objectives` |
| KO-02 | If this goes well, what is different in finance in 12 months? | Push for two or three concrete outcomes | Engagement: `engagement.objectives` |
| KO-03 | How will you judge whether it was worth it? Do we have a baseline today? | Hours, errors, days to close?, Who tracks it today? | Engagement: `engagement.success_measures` |

**Scope**

| ID | Question | Probe | Answer goes to (C2) |
| --- | --- | --- | --- |
| KO-04 | Which processes matter most? | Why those?, Who owns each? | Engagement: `engagement.processes_in_scope` |
| KO-05 | Is there anything we should deliberately leave out (e.g. payroll, tax, overseas entities)? | – | Engagement: `engagement.out_of_scope` |
| KO-06 | Are any systems changing in the next 12 months (e.g. ERP upgrade, new expense tool)? | Dates?, Selected vendor? | Engagement: `engagement.planned_system_changes` |

**Constraints and appetite**

| ID | Question | Probe | Answer goes to (C2) |
| --- | --- | --- | --- |
| KO-07 | Would you rather get more out of the tools you already have, or are you open to adding a new tool if it removes the work? | Spend range? | Engagement: `engagement.constraints` |
| KO-08 | Are there limits on budget, IT time, or busy periods we must avoid? | Year end, audit, other projects? | Engagement: `engagement.constraints` |
| KO-09 | Who would own an automation after go-live? | Do they have time? | Use cases (note until use cases exist): `use_case.runstate_owner_role` |

**People and logistics**

| ID | Question | Probe | Answer goes to (C2) |
| --- | --- | --- | --- |
| KO-10 | Who owns each process day to day, and who owns the ERP and IT? | Names and roles, who decides? | Attendees: `attendee.role` |
| KO-11 | Can attendees share their screens and log in to live systems during the sessions? | Any systems they can't show? | Attendees: `attendee.can_share_screen` |
| KO-12 | Who can grant us read access or a sandbox, if needed later? | In-house or partner? | Systems: `system.admin_contact_role` |
| KO-15 | When can we hold the sessions, and how long can each attendee give? | – | Engagement: `engagement.workshop_dates` |

**Recording and data**

| ID | Question | Probe | Answer goes to (C2) |
| --- | --- | --- | --- |
| KO-13 | Are you comfortable with us recording the sessions in Teams and using the transcript (parsed with Copilot or Claude) to prepare notes? | Any sessions to exclude? | Engagement: `engagement.recording_consent` |
| KO-14 | Does any of the material we will ask for contain personal information, and are there rules on where it may be stored? | Employee data in expense exports? | Readiness (Security and privacy): `readiness.evidence` |

## What the answers decide

| Decision | Based on |
| --- | --- |
| Which A2 tabs to send: About you, plus one tab per process (EXP, BNK, CFF, or Other process for anything else) | KO-04, KO-05 |
| Who is invited to each session, and whether screens can be shared | KO-10, KO-11, KO-15 |
| Whether sessions are recorded; which need scribe notes only | KO-13 (D3) |
| How personal data in documents is handled | KO-14 (D3) |
| Risks to flag early: planned system changes, no run-state owner | KO-06, KO-09 |

## After the call

- [ ] Engagement and Attendees tabs completed in C2 (record status Reviewed)
- [ ] A2 prepared: About you plus one tab per process in scope; unused tabs deleted; Other process copied and renamed for each extra process
- [ ] A2 sent with the secure share link and a return date (about 5 working days before the first workshop)
- [ ] Workshop invitations sent with the A4 pre-read and the consent request
