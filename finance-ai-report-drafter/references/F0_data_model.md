# F0 – Engagement Data Model (v1.0)

The single field list every Finance AI accelerator and skill uses. Each entity is a tab in the C2 engagement workbook and an object in `F0_engagement_data_model.json`.

**Source:** Intake = questionnaire and documents · Workshop = sessions, transcripts, notes · Analysis = Deloitte assessment.  
**Required for:** Report, Build, Report and build, or Optional.  
**Questions:** the B2 question-bank IDs that fill the field. A required field with no question is filled in analysis.

Every record also carries `evidence_ids`, `confidence` (High / Medium / Low, set by S2) and `record_status` (Draft (AI) / Reviewed / Confirmed with client).

## Engagement (`engagement`)

Report section: 1, 2

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `client` | Client | text | Intake | Report | Client legal or trading name |  | CORE-01 |
| `industry` | Industry | text | Intake | Optional | Client industry, in the client's words |  |  |
| `sponsor_role` | Sponsor role | text | Intake | Report | Role of the engagement sponsor (e.g. CFO) |  |  |
| `objectives` | Objectives | text | Intake | Report | What the client wants from AI and automation, in their words |  | KO-01, KO-02, CORE-03, CFF-01 |
| `success_measures` | Success measures | text | Intake | Report | How the sponsor will judge success |  | KO-03, CORE-04 |
| `processes_in_scope` | Processes in scope | list | Intake | Report | Process modules selected at kick-off |  | KO-04 |
| `out_of_scope` | Out of scope | list | Intake | Report | Areas explicitly excluded |  | KO-05 |
| `constraints` | Constraints | text | Intake | Report and build | Stated limits, e.g. no new infrastructure, licence budget, IT capacity |  | KO-07, KO-08, CORE-05, CORE-16, SOL-03 |
| `workshop_dates` | Workshop dates | list | Intake | Report | Date of each workshop session |  | KO-15 |
| `planned_system_changes` | Planned system changes | text | Intake | Report and build | System changes planned in the next 12 months (e.g. ERP upgrade, new expense tool) that could affect a design |  | KO-06 |
| `recording_consent` | Recording consent | enum | Intake | Report | Consent to record sessions in Teams and parse transcripts with an approved tool (D3) | Yes - all sessions, Yes - some sessions, No, Not yet asked | KO-13 |
| `audit_client` | Deloitte audit client or related entity | enum | Intake | Report | Drives independence clearance before issue | Yes, No, To confirm |  |

## Attendees (`attendee`)

Report section: 2, Appendix A · ID prefix: AT-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Intake | Report | AT-01 onward |  |  |
| `name` | Name | text | Intake | Report | Attendee name |  |  |
| `role` | Role | text | Intake | Report | Job title or role |  | KO-10, CORE-02 |
| `sessions` | Sessions attended | list | Workshop | Report | Workshop sessions attended |  |  |
| `decision_rights` | Decision rights | text | Workshop | Optional | What this person can approve (e.g. process change, spend, system access) |  |  |
| `can_share_screen` | Can share screen with live logins | enum | Intake | Optional | Whether the attendee can show live systems in the session | Yes, No, To arrange | KO-11 |

## Systems (`system`)

Report section: 3, 8 · ID prefix: SY-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | SY-01 onward |  |  |
| `name` | System | text | Intake | Report and build | Product name (e.g. NetSuite, Expensify) |  | CORE-07, CORE-12, CFF-03, GEN-04 |
| `type` | Type | enum | Intake | Report | System category | ERP / GL, Expense management, Banking, Payments, Close management, Reporting / BI, Forecasting / FP&A, Spreadsheet, Productivity / M365, AI tool, Integration platform, Other |  |
| `used_for` | Used for | text | Intake | Report | Processes and tasks it supports |  |  |
| `edition_modules` | Edition and modules licensed | text | Intake | Build | Edition, plan or tier, plus add-on modules held |  | CORE-08, CORE-11, EXP-03, BNK-03 |
| `unused_features` | Licensed but unused features | text | Workshop | Build | Features the client pays for but has not switched on |  | SOL-01 |
| `business_owner` | Business owner (role) | text | Intake | Report | Role accountable for the system |  |  |
| `admin` | Administered by | enum | Intake | Build | Who changes configuration | In-house, Implementation partner, Vendor, Mixed, Unknown | CORE-09, SOL-02 |
| `admin_contact_role` | Admin contact (role) | text | Intake | Build | Role or firm that grants access and makes changes |  | KO-12 |
| `users` | Number of users | number | Intake | Optional | Named users |  |  |
| `api_access` | API / integration access | enum | Intake | Report and build | How data can be read or written programmatically | REST / SOAP API available, Native connector only, File import/export only, None, Unknown | CORE-10 |
| `sandbox` | Sandbox available | enum | Intake | Build | Non-production environment for testing | Yes, No, Can be requested, Unknown |  |
| `key_person_risk` | Key-person risk | enum | Workshop | Optional | Only one person understands or maintains it | Yes, No |  |
| `notes` | Notes | text | Workshop | Optional | Anything else relevant |  |  |

## Data flows (`data_flow`)

Report section: 3 · ID prefix: DF-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | DF-01 onward |  |  |
| `from_system` | From | ref:system | Workshop | Report and build | Source system ID |  |  |
| `to_system` | To | ref:system | Workshop | Report and build | Target system ID |  |  |
| `data` | Data | text | Workshop | Report and build | What moves (e.g. card transactions, statement lines) |  |  |
| `method` | Method | enum | Workshop | Report and build | How it moves today | Automated integration, Native connector, File upload, Manual re-key, Email / copy-paste | EXP-04, EXP-05, BNK-02, CFF-05, GEN-05 |
| `frequency` | Frequency | enum | Workshop | Report | How often | Real time, Daily, Weekly, Monthly, Ad hoc |  |
| `issues` | Issues | text | Workshop | Report | Failures, delays, errors |  |  |

## Processes (`process`)

Report section: 4, Appendix B · ID prefix: P-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | P-01 onward |  |  |
| `name` | Process | text | Intake | Report | Process name |  |  |
| `module` | Module | enum | Analysis | Report | Question-bank module the process maps to (GEN for any process without its own module) | EXP, BNK, CFF, GEN |  |
| `owner_role` | Owner (role) | text | Workshop | Report and build | Role accountable for the process |  |  |
| `participants` | Participants (roles) | text | Workshop | Report | Roles that perform or review steps |  |  |
| `trigger_start` | Start trigger | text | Workshop | Report and build | What starts the process |  | GEN-06 |
| `trigger_end` | End trigger | text | Workshop | Report and build | What marks it complete |  |  |
| `frequency` | Frequency | enum | Workshop | Report | How often it runs | Daily, Weekly, Fortnightly, Monthly, Quarterly, Ongoing | CFF-02 |
| `timing` | Timing | text | Workshop | Report | Deadlines and calendar, e.g. WD+2 at month end |  | EXP-14, BNK-10, GEN-03 |
| `volume` | Volume per month | number | Intake | Report and build | Transactions or items per month (state the unit) |  | EXP-01, BNK-01, GEN-01 |
| `volume_unit` | Volume unit | text | Intake | Report and build | What is counted (claims, statement lines, forecast refreshes) |  |  |
| `seasonality` | Seasonality | text | Workshop | Build | Peaks and troughs in volume |  | EXP-02, GEN-02 |
| `hours_per_cycle` | Hours per cycle | number | Workshop | Report | Total people-hours per cycle |  | EXP-12, CFF-08, GEN-11 |
| `cycles_per_year` | Cycles per year | number | Workshop | Report | Number of cycles in a year |  |  |
| `manual_share` | Manual share (%) | percent | Workshop | Report | Share of effort that is manual |  |  |
| `systems` | Systems and files | list | Workshop | Report and build | System IDs and key spreadsheets used |  |  |
| `linked_processes` | Linked processes | text | Workshop | Report | Upstream and downstream processes linked in the process map (→ continues in, ← comes from) |  |  |
| `inputs` | Inputs | text | Workshop | Report and build | What comes in |  | CFF-04 |
| `outputs` | Outputs | text | Workshop | Report and build | What goes out |  | CFF-10, CFF-11 |
| `steps` | Key steps | text | Workshop | Report and build | Numbered steps, max 10 (full map in Appendix B) |  | EXP-11, BNK-05, CFF-07, GEN-07 |
| `manual_touchpoints` | Manual touchpoints | text | Workshop | Report | Re-keying, copy-paste, lookups, chasing |  | BNK-08, GEN-12 |
| `business_rules` | Business rules | text | Workshop | Build | Coding, matching, approval or policy rules applied |  | EXP-06, EXP-08, BNK-06, CFF-06, GEN-08 |
| `controls` | Key controls | text | Workshop | Report and build | Reviews, approvals, segregation of duties |  | EXP-07, EXP-13, BNK-09, GEN-09 |
| `exceptions` | Exceptions and rework | text | Workshop | Report and build | What goes wrong, how often, how it is fixed |  | EXP-10, EXP-15, BNK-07, CFF-09, GEN-10 |
| `maturity` | Maturity (1-5) | score | Analysis | Report | 1 ad hoc and manual, 3 documented and partly automated, 5 automated with exception-only review | 1, 2, 3, 4, 5 |  |
| `maturity_rationale` | Maturity rationale | text | Analysis | Report | One line |  |  |

## Pain points (`pain_point`)

Report section: 5 · ID prefix: PP-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | PP-01 onward |  |  |
| `process_id` | Process | ref:process | Workshop | Report | Process ID |  |  |
| `description` | Pain point | text | Workshop | Report | What goes wrong, in plain words |  | CORE-18 |
| `category` | Category | enum | Analysis | Report | Pain point category | Manual effort, Data quality, Timeliness, Control gap, Visibility / reporting, Key-person dependency, System limitation |  |
| `root_cause` | Root cause | text | Analysis | Report | Why it happens |  |  |
| `impact` | Impact | text | Workshop | Report | Hours, errors or risk, quantified where possible |  |  |
| `impact_hours_per_year` | Impact (hours / year) | number | Analysis | Optional | Quantified effort where available |  |  |
| `frequency` | Frequency | text | Workshop | Report | How often it happens |  |  |
| `raised_by_role` | Raised by (role) | text | Workshop | Report | Role of the person who raised it |  |  |
| `evidence_ids` | Evidence | list | Workshop | Report | Evidence IDs |  |  |
| `use_case_ids` | Linked use cases | list | Analysis | Report | Use case IDs |  |  |

## Evidence (`evidence`)

Report section: 5, traceability · ID prefix: EV-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | EV-01 onward |  |  |
| `source_type` | Source type | enum | Workshop | Report | Where it came from | Intake answer, Document, Transcript, Scribe note, Process map, Whiteboard photo, Sample data |  |
| `reference` | Reference | text | Workshop | Report | Question ID, document name, or session code + timestamp (e.g. W2 00:14:32) |  |  |
| `summary` | Summary or short quote | text | Workshop | Report | What the source says (keep quotes short) |  |  |
| `supports` | Supports | list | Analysis | Report | IDs of records this evidence supports |  |  |

## Use cases (`use_case`)

Report section: 6, 9 · ID prefix: UC-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | UC-01 onward |  |  |
| `name` | Use case | text | Analysis | Report | Short name |  |  |
| `library_id` | Library pattern | ref:library | Analysis | Report | C1 library entry it is based on |  |  |
| `process_id` | Process | ref:process | Analysis | Report | Process ID |  |  |
| `pain_point_ids` | Pain points addressed | list | Analysis | Report | PP IDs |  |  |
| `solution_pattern` | Solution pattern | enum | Analysis | Report | From the Deloitte Finance AI use case library | Document extraction, Matching and reconciliation, Anomaly and variance detection, Commentary and narrative generation, Agentic transaction posting, Finance Q&A assistant, Forecasting, Workflow and configuration |  |
| `delivery_tier` | Delivery tier | enum | Analysis | Report and build | Configure-first tiering | T1 Configure existing tool, T2 Low-code AI in client tools, T3 Custom build |  |
| `tools` | Tools | text | Analysis | Report and build | Tools the solution uses |  |  |
| `problem_statement` | Problem statement | text | Analysis | Report | Who, what, cost today, in one sentence |  |  |
| `how_it_works` | How it works | text | Analysis | Report and build | 3-5 steps of the future process |  |  |
| `human_in_loop` | Human in the loop | text | Analysis | Report and build | What a person reviews or approves, and when |  | SOL-05 |
| `controls_audit` | Controls and audit trail | text | Analysis | Report and build | How every AI action is logged and evidenced |  |  |
| `runstate_owner_role` | Run-state owner (role) | text | Workshop | Report and build | Role accountable once live |  | KO-09, CORE-17, SOL-04 |
| `volume` | Volume / year | number | Analysis | Report | Items per year (from process volume) |  |  |
| `minutes_per_item` | Minutes per item today | number | Workshop | Report | Manual minutes per item |  |  |
| `automation_share` | Automation share (%) | percent | Analysis | Report | Share of items handled without manual work |  |  |
| `hours_saved` | Est. hours saved / yr | formula | Analysis | Report | volume x minutes per item x automation share / 60 |  |  |
| `indicative_effort_weeks` | Indicative effort (weeks) | number | Analysis | Report | Build effort |  |  |
| `phase` | Recommended phase | enum | Analysis | Report | Roadmap phase | Quick win, Phase 2, Backlog |  |
| `risks` | Risks and dependencies | text | Analysis | Report | Main risks |  |  |

## Scoring (`score`)

Report section: 7, Appendix C

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `use_case_id` | Use case | ref:use_case | Analysis | Report | UC ID |  |  |
| `v_effort` | Value: effort released (1-5) | score | Analysis | Report | 1 < 50 h/yr, 5 > 1,000 h/yr | 1, 2, 3, 4, 5 |  |
| `v_quality` | Value: accuracy and quality (1-5) | score | Analysis | Report | 1 no change, 5 removes a recurring error | 1, 2, 3, 4, 5 |  |
| `v_control` | Value: control and risk (1-5) | score | Analysis | Report | 1 no change, 5 closes a known control gap | 1, 2, 3, 4, 5 |  |
| `f_data` | Feasibility: data (1-5) | score | Analysis | Report | 1 missing or poor, 5 clean, structured, accessible | 1, 2, 3, 4, 5 |  |
| `f_access` | Feasibility: system access (1-5) | score | Analysis | Report | 1 no API, manual only, 5 API in place | 1, 2, 3, 4, 5 |  |
| `f_stability` | Feasibility: process stability (1-5) | score | Analysis | Report | 1 changing or undocumented, 5 stable and standard | 1, 2, 3, 4, 5 |  |
| `f_change` | Feasibility: change impact (1-5) | score | Analysis | Report | 1 major role change, 5 minor change | 1, 2, 3, 4, 5 |  |
| `rationale` | Rationale | text | Analysis | Report | Why these scores |  |  |

## Readiness (`readiness`)

Report section: 8

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `dimension` | Dimension | enum | Analysis | Report | Readiness dimension | Data quality, Data access and APIs, Systems and integration, Security and privacy, Governance and controls, People and skills, Change readiness |  |
| `rating` | Rating (1-5) | score | Analysis | Report | 1 blocker, 3 workable with mitigation, 5 ready | 1, 2, 3, 4, 5 |  |
| `evidence` | Evidence | text | Workshop | Report | What we saw |  | KO-14, CORE-13, CORE-14, CORE-15 |
| `gap` | Gap | text | Analysis | Report | What is missing |  |  |
| `action` | Action before build | text | Analysis | Report and build | Only actions that gate a priority use case |  |  |
| `gates_use_cases` | Gates use cases | list | Analysis | Report | UC IDs gated |  |  |

## Build requirements (`build_requirement`)

Report section: Appendix H (build specification), referenced from 9 · ID prefix: BR-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Build | BR-01 onward |  |  |
| `use_case_id` | Use case | ref:use_case | Analysis | Build | UC ID |  |  |
| `type` | Type | enum | Analysis | Build | Kind of requirement | Access and roles, Configuration, Field / account mapping, Sample / test data, Acceptance criterion, Cut-over and rollback, Run-state support |  |
| `requirement` | Requirement | text | Workshop | Build | What is needed, specifically |  | SOL-06, EXP-09, BNK-04, BNK-12, GEN-14 |
| `system_id` | System | ref:system | Workshop | Build | System ID it applies to |  |  |
| `owner_role` | Provided by (role) | text | Workshop | Build | Who provides or approves it |  |  |
| `status` | Status | enum | Analysis | Build | Readiness of this requirement | Not started, Requested, Received, Confirmed, Blocked |  |

## Open questions (`open_question`)

Report section: Working list; all closed or listed in Appendix E before issue · ID prefix: OQ-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Analysis | Report | OQ-01 onward |  |  |
| `question` | Question | text | Workshop | Report | The open question |  |  |
| `field_ref` | Field it fills | text | Analysis | Optional | Entity.field the answer fills |  |  |
| `owner_role` | Owner (role) | text | Workshop | Report | Who will answer |  |  |
| `due` | Due | date | Workshop | Report | Date the answer is due |  |  |
| `status` | Status | enum | Workshop | Report | Status | Open, Answered, Closed - not needed |  |
| `answer` | Answer | text | Workshop | Report | The answer once received |  |  |

## Documents received (`document`)

Report section: Appendix F · ID prefix: DOC-

| Field | Label | Type | Source | Required for | Definition | Allowed values | Questions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | ID | id | Intake | Report | DOC-01 onward |  |  |
| `request_id` | Request item | text | Intake | Optional | A3 request list item it answers |  |  |
| `name` | Document | text | Intake | Report | File name or description |  | EXP-16, BNK-11, CFF-12, GEN-13 |
| `received` | Received | date | Intake | Report | Date received |  |  |
| `from_role` | From (role) | text | Intake | Report | Who sent it |  |  |
| `personal_data` | Contains personal data | enum | Intake | Report | Drives handling under D3 | Yes, No, Unknown |  |
| `location` | Stored at | text | Intake | Optional | Where the file is held |  |  |
