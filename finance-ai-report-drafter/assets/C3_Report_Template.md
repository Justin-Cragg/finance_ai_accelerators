# Finance AI – Discovery & Design Report (Template)

Nov 4, 2026 · @Justin

## How to use this template

This is the client deliverable issued after the discovery workshops. It records the current state, identifies AI use cases, and recommends what to build first.

- **[Square brackets]** = placeholder to replace with client content.
- *Guidance:* lines in italics are drafting notes. Delete them before issue.
- **Source tags** show where each field is captured. They match the F0 engagement data model, and each section draws on the matching tab of the C2 engagement workbook:
  - **Intake** = pre-workshop questionnaire and documents the client sends
  - **Workshop** = workshop transcripts, notes and whiteboard photos
  - **Analysis** = Deloitte assessment after the workshops
- IDs link the sections together: processes (P-01), pain points (PP-01), use cases (UC-01), build requirements (BR-01).

*Guidance: target 15–25 pages plus appendices. Issue within [5] working days of the final workshop. Skill S3 drafts this report from the C2 workbook; every AI-drafted section must be reviewed before issue (D3).*

## 1. Executive summary

*Guidance: one page. Write it last. Lead with the recommendation and the value, not the method.*

**Recommendation:** [Client] should start with [UC-01 name] and [UC-02 name], which together could release about [X] hours a year in [process area] within [N] weeks of starting.

**What we did:** [N] workshops with [N] people across [finance functions] between [date] and [date].

**What we found:**

- [Headline finding 1, e.g. month-end close takes X days, with Y% of effort in manual reconciliation]
- [Headline finding 2]
- [Headline finding 3]

**Priority use cases**

| ID | Use case | Process | Delivery tier | Est. hours saved / yr | Feasibility | Recommended phase |
| --- | --- | --- | --- | --- | --- | --- |
| UC-01 | [Name] | [P-0x] | [T1 / T2 / T3] | [X] | [High / Med / Low] | [Quick win] |
| UC-02 | [Name] | [P-0x] | [T1 / T2 / T3] | [X] | [High / Med / Low] | [Quick win] |
| UC-03 | [Name] | [P-0x] | [T1 / T2 / T3] | [X] | [High / Med / Low] | [Phase 2] |

**Readiness:** [One sentence on the biggest enabler or blocker, e.g. data access via the ERP API is in place; data quality in the vendor master needs work first.]

**Next step:** [Decision requested from the client and by when.]

*Source: Analysis.*

## 2. Scope and approach

**Objective:** Identify where AI can reduce effort, improve accuracy or strengthen control in [Client]'s finance function, and design the priority use cases to a point where they can be built.

**Scope**

| In scope | Out of scope |
| --- | --- |
| [e.g. Record-to-report, month-end close] | [e.g. Payroll] |
| [e.g. Purchase-to-pay] | [e.g. Tax compliance] |
| [e.g. Management reporting] | [e.g. Subsidiaries outside NZ] |

**Workshops held** *(Source: Intake)*

| Date | Workshop | Process areas | Client attendees (roles) | Duration |
| --- | --- | --- | --- | --- |
| [dd/mm] | [Kick-off and systems walkthrough] | [All] | [CFO, FC] | [1.5 h] |
| [dd/mm] | [Close and reconciliations] | [P-01, P-02] | [FC, accountants] | [2 h] |
| [dd/mm] | [Payables] | [P-03] | [AP lead] | [1.5 h] |

**Approach**

1. Intake questionnaire and document request before the workshops
2. Process walkthroughs, with screens shared where possible
3. Pain point and opportunity capture during each session
4. Use case identification against Deloitte's Finance AI use case library
5. Scoring, prioritisation and design of the priority use cases
6. Playback and validation with [sponsor]

**Limitations:** Findings are based on workshop discussion and the documents listed in Appendix F. Volumes and effort estimates are as reported by attendees and have not been audited.

*Guidance: list any process owners who were unavailable and how that affects confidence in the findings.*

## 3. Current-state systems landscape

[Client] runs finance on [ERP], supported by [N] other systems and [N] critical spreadsheets. [One sentence on the main integration gap, e.g. bank and AP data are re-keyed into the ERP.]

*Guidance: insert a landscape diagram here showing each system as a box and each data flow as an arrow labelled automated, file upload or manual re-key. Mark spreadsheets that act as systems.*

**Systems inventory** *(Source: Intake, confirmed in Workshop)*

| System | Type | Used for | Owner | Users | Integration / API access | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| [NetSuite] | ERP / GL | [GL, AP, AR] | [FC] | [12] | [REST API available] | [] |
| [FloQast / BlackLine / none] | Close management | [Checklist, recs] | [] | [] | [] | [] |
| [Bank portal] | Banking | [Statements, payments] | [] | [] | [Daily file] | [] |
| [Power BI] | Reporting | [Mgmt reports] | [] | [] | [] | [] |
| [Rec workbook.xlsx] | Spreadsheet | [Bank rec] | [] | [] | [Manual] | [Key-person risk] |

**Data flows** *(Source: Workshop)*

| From | To | Data | Method | Frequency | Issues |
| --- | --- | --- | --- | --- | --- |
| [Bank] | [ERP] | [Transactions] | [Manual CSV upload] | [Daily] | [] |
| [Supplier email] | [ERP] | [Invoices] | [Manual keying] | [Ongoing] | [] |

## 4. Process inventory

We documented [N] processes that together consume about [X] hours a month, [Y]% of it manual.

**Process summary** *(Source: Workshop)*

| ID | Process | Owner | Frequency | Hours / cycle | Hours / yr | Manual share | Maturity (1–5) | Pain points |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P-01 | [Bank reconciliation] | [] | [Daily] | [] | [] | [%] | [] | [PP-01, PP-02] |
| P-02 | [Month-end close] | [] | [Monthly] | [] | [] | [%] | [] | [] |
| P-03 | [Supplier invoice processing] | [] | [Ongoing] | [] | [] | [%] | [] | [] |

*Guidance: maturity 1 = ad hoc and manual, 3 = documented and partly automated, 5 = automated with exception-only review.*

### Process card template (one per process)

| Field | Content | Source |
| --- | --- | --- |
| Process ID and name | [P-01 Bank reconciliation] | Workshop |
| Start and end trigger | [Starts when statement is available; ends when rec is reviewed] | Workshop |
| Owner and participants | [Role, not name, e.g. Financial Accountant; reviewer FC] | Workshop |
| Frequency and timing | [Daily; also WD+2 at month end] | Workshop |
| Volumes | [e.g. 1,200 transactions / month across 4 accounts] | Intake |
| Effort | [Hours per cycle × people] | Workshop |
| Systems and files | [ERP, bank portal, rec workbook] | Workshop |
| Inputs and outputs | [Bank file in; signed rec out] | Workshop |
| Key steps | [Numbered steps, max 10] | Workshop |
| Manual touchpoints | [Re-keying, copy-paste, lookups, emails chasing] | Workshop |
| Key controls | [Review and sign-off, segregation of duties] | Workshop |
| Exceptions and rework | [What goes wrong, how often, how it is fixed] | Workshop |
| Pain points | [PP-IDs, see section 5] | Workshop |
| Maturity rating | [1–5 with one-line rationale] | Analysis |

*Guidance: put the full step-by-step process map in Appendix B. Keep the card to one page.*

## 5. Pain point and opportunity register

We captured [N] pain points. [N] of them trace to [the top root cause, e.g. manual data movement between systems].

| ID | Process | Pain point | Category | Root cause | Impact | Frequency | Raised by (role) | Evidence | Linked use case |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PP-01 | [P-01] | [Unmatched items cleared by hand] | [Manual effort] | [No matching rules] | [8 h / month] | [Monthly] | [Accountant] | [W2, 00:14:32] | [UC-01] |
| PP-02 | [] | [] | [] | [] | [] | [] | [] | [] | [] |

**Categories:** manual effort · data quality · timeliness · control gap · visibility / reporting · key-person dependency · system limitation.

*Guidance: every pain point needs evidence, either a transcript timestamp, a document reference or a named example. This lets the client verify it and lets us trace AI-drafted entries back to source. Impact should be in hours, errors or risk where possible.*

## 6. AI use case catalogue

We identified [N] use cases from the pain points. [N] are recommended for design now (section 9); the rest stay in the backlog.

**Configure first.** We recommend the simplest option that solves each problem: first a setting or feature in a tool [Client] already licenses (T1), then low-code AI in tools [Client] already has (T2), and a custom build (T3) only where those can't do the job. Some recommendations are therefore configuration changes rather than AI builds.

**Use case summary** *(Source: Analysis)*

| ID | Use case | Process | Pain points addressed | Solution pattern | Delivery tier | Est. hours saved / yr | Value score | Feasibility score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UC-01 | [Automated bank matching with exception review] | [P-01] | [PP-01, PP-02] | [Matching / reconciliation] | [T1] | [] | [] | [] |
| UC-02 | [] | [] | [] | [] | [] | [] | [] | [] |

**Solution patterns** (from the Deloitte Finance AI use case library): document extraction · matching and reconciliation · anomaly and variance detection · commentary and narrative generation · agentic transaction posting · finance Q&A assistant · forecasting · workflow and configuration.

**Delivery tiers:** T1 configure existing tool · T2 low-code AI in client tools · T3 custom build.

### Use case card template (one per use case)

| Field | Content |
| --- | --- |
| ID and name | [UC-01 Automated bank matching] |
| Problem statement | [One sentence: who, what, cost today] |
| Pain points addressed | [PP-IDs] |
| Solution pattern | [From the list above] |
| Delivery tier and tools | [T1 / T2 / T3, the tools used, and why this tier] |
| How it works | [3–5 steps of the future process] |
| Systems and integration points | [Reads from bank feed; posts to ERP via API] |
| Data required and availability | [What data, where it lives, quality today] |
| Human in the loop | [What a person reviews or approves, and when] |
| Controls and audit trail | [How every AI action is logged and evidenced] |
| Proposed solution owner (run state) | [Role accountable once live; full RACI in section 9] |
| Value | [Hours saved = volume × minutes per item × automation %; plus quality and risk benefits] |
| Feasibility | [Score and main constraint] |
| Risks and dependencies | [] |
| Indicative effort | [Weeks, team mix] |

*Guidance: show the value calculation inputs so the client can challenge them. Use the client's own volumes from the intake.*

## 7. Prioritisation

Each use case is scored 1–5 on value and feasibility. [N] use cases fall in the quick-win quadrant and are recommended for the first phase.

**Scoring criteria** *(Source: Analysis)*

| Dimension | Criterion | Weight | 1 = | 5 = |
| --- | --- | --- | --- | --- |
| Value | Effort released | [40%] | [< 50 h / yr] | [> 1,000 h / yr] |
| Value | Accuracy and quality | [30%] | [No change] | [Removes a recurring error] |
| Value | Control and risk reduction | [30%] | [No change] | [Closes a known control gap] |
| Feasibility | Data availability and quality | [35%] | [Data missing or poor] | [Clean, structured, accessible] |
| Feasibility | System access and integration | [35%] | [No API, manual only] | [API in place] |
| Feasibility | Process stability | [15%] | [Changing or undocumented] | [Stable and standard] |
| Feasibility | Change impact on people | [15%] | [Major role change] | [Minor change] |

*Guidance: insert the value × feasibility matrix from the C2 Matrix tab, with each use case labelled by ID. Quadrants: quick win (high value, high feasibility), plan for phase 2 (high value, low feasibility), opportunistic (low value, high feasibility), backlog. Full workings go in Appendix C.*

## 8. Data and AI readiness assessment

[Client] is [ready / partly ready / not yet ready] to build the priority use cases. The main gap is [e.g. vendor master data quality].

| Dimension | Rating (1–5) | Evidence | Gap | Action before build |
| --- | --- | --- | --- | --- |
| Data quality | [] | [e.g. 15% duplicate vendors] | [] | [] |
| Data access and APIs | [] | [e.g. ERP REST API enabled, integration role exists] | [] | [] |
| Systems and integration | [] | [] | [] | [] |
| Security and privacy | [] | [e.g. approved AI tools policy in place] | [] | [] |
| Governance and controls | [] | [] | [] | [] |
| People and skills | [] | [] | [] | [] |
| Change readiness | [] | [] | [] | [] |

*Source: Intake and Workshop for evidence; Analysis for rating.*

*Guidance: 1 = blocker that must be fixed first, 3 = workable with mitigation, 5 = ready. Only list actions that gate a priority use case.*

## 9. Target-state design for priority use cases

*Guidance: repeat this section for each priority use case (typically 2–4). This is the part the client signs off before any build, so it must be specific enough to scope implementation. The detailed build specification for each use case sits in Appendix H; refer to it rather than repeating it here.*

### 9.1 [UC-01 name]

**Outcome:** [e.g. Bank reconciliation moves from 2 days to same day, with staff reviewing exceptions only.]

**Current vs future process**

| Step | Today | Future | Performed by |
| --- | --- | --- | --- |
| 1 | [Download statement, paste into workbook] | [Bank feed loads automatically] | [System] |
| 2 | [Match line by line] | [AI matches using agreed rules; scores confidence] | [AI] |
| 3 | [Investigate differences] | [Review exceptions below confidence threshold] | [Accountant] |
| 4 | [Sign off workbook] | [Approve rec in tool with full audit log] | [FC] |

*Guidance: insert a before/after flow diagram if the process branches.*

**Solution components:** [Delivery tier, AI model / agent, data sources, integration method, where outputs are stored, user interface.]

**Controls:** [Approval points, confidence thresholds, segregation of duties, what is logged and where.]

**Exception handling:** [What happens when the AI cannot complete or confidence is low.]

**Build specification:** See Appendix H.[1] for the configuration, mappings, access, test data, acceptance criteria and cut-over plan for this use case.

**Solution ownership (run state, RACI)**

*Guidance: this is who owns and operates the solution once it is live. It is separate from the implementation team's RACI, which sits in the engagement letter. Agree one Accountable owner per activity with the client before design sign-off.*

| Activity | Business owner [e.g. FC] | Process users [e.g. accountants] | Finance systems / IT | Data owner | Risk / internal audit |
| --- | --- | --- | --- | --- | --- |
| Review and approve AI outputs | A | R | I | I | I |
| Handle exceptions the AI cannot resolve | A | R | C | C | I |
| Monitor accuracy and performance against targets | A | R | C | I | I |
| Maintain rules, prompts and configuration | A | C | R | C | I |
| Manage system access, credentials and integration | I | I | A / R | I | C |
| Maintain quality of source data | C | C | C | A / R | I |
| Approve changes to the solution | A | C | R | C | C |
| Respond to incidents and outages | A | I | R | I | I |
| Periodic review of controls and AI use | A | C | C | C | R |
| Manage vendor and licence | A | I | R | I | I |

*R = Responsible, A = Accountable, C = Consulted, I = Informed. Assignments above are a starting point; confirm with the client. Source: Workshop for proposed owners; Analysis for the draft.*

**Success measures**

| Measure | Baseline | Target | How measured |
| --- | --- | --- | --- |
| [Hours per month] | [] | [] | [] |
| [Auto-match rate] | [] | [] | [] |
| [Errors found in review] | [] | [] | [] |

**Design decisions and assumptions:** [List decisions agreed with the client, and open questions with owners.]

## 10. Risk, controls and AI governance

Every recommended use case keeps a person accountable for the financial outcome, and every AI action is logged.

| Risk | Likelihood | Impact | Mitigation | Owner |
| --- | --- | --- | --- | --- |
| Incorrect AI output posted or relied on | [] | [] | Confidence thresholds, human approval before posting, sample testing | [] |
| Sensitive or personal data sent to an unapproved tool | [] | [] | Approved tools only, data minimisation, access controls | [] |
| Over-reliance; reviewers stop checking | [] | [] | Defined review steps, periodic re-performance | [] |
| System access too broad for the AI integration | [] | [] | Least-privilege integration role, credentials in a vault | [] |
| Process changes break the solution | [] | [] | Named owner, change log, monitoring of match and error rates | [] |
| Low adoption by the team | [] | [] | Involve users in design, training, quick wins first | [] |
| Vendor or model dependency | [] | [] | Document configuration, exit plan | [] |
| Ongoing maintenance and further development not resourced or funded after go-live (solution degrades, enhancements stall) | [] | [] | Agree run-state owner and support model before build (section 9 RACI); budget for maintenance and enhancements; document configuration and change process; option of a Deloitte support arrangement | [] |

**Governance principles to agree with [Client]:**

- A named business owner for each use case
- An audit trail for every AI-generated entry, match or commentary
- Periodic review of accuracy against a set threshold
- A register of AI use cases in production

*Guidance: confirm Deloitte independence clearance before issue if the client or any related entity is an audit client. Confirm which tools were used to process workshop recordings.*

## 11. Roadmap and implementation options

We recommend starting with [UC-01] and [UC-02] after a [3]-week foundations phase, with a go/no-go gate before each phase.

*Guidance: insert the implementation roadmap here: phases left to right with durations, and a go/no-go gate between each phase.*

**Implementation options**

| Option | Scope | Duration | Indicative fee (NZD) | Deloitte team |
| --- | --- | --- | --- | --- |
| A. Quick wins | Phases 0–1 | [11 weeks] | [$] | [Manager + consultant] |
| B. Quick wins and scale | Phases 0–2 | [20 weeks] | [$] | [] |
| C. Client-led build | Client builds; Deloitte designs and reviews | [] | [$] | [] |

*Guidance: fees per use case should follow the fixed-fee structure in the offering. Each option links to a separate engagement letter.*

**Next steps**

- [ ] [Client] confirms preferred option by [date]
- [ ] Playback of this report to [sponsor] on [date]
- [ ] Resolve readiness actions in section 8
- [ ] Issue engagement letter for the chosen option

## Appendices

- **A. Workshop attendees:** name, role, workshops attended
- **B. Detailed process maps:** step-level maps for each process card (P-01 onward)
- **C. Full scoring workings:** value and feasibility scores for every use case, including the backlog
- **D. Use case backlog:** use cases not prioritised now, with the reason
- **E. Assumptions and limitations**, including open questions not closed before issue
- **F. Documents and data received:** what the client provided and when
- **G. Glossary**
- **H. Build specification:** one part per priority use case (H.1 for UC-01, H.2 for UC-02 ...), in the format below

### H.[1] Build specification – [UC-01 name]

*Guidance: this is what the implementation team builds from. Source: Build requirements tab of the C2 workbook (BR IDs). Anything still marked Requested or Blocked must be listed as a readiness action in section 8.*

**Delivery tier and tools:** [T1 / T2 / T3; the tools used, and why this tier was chosen over a simpler one]

**Configuration**

| # | System | Setting or component | Configuration | BR ID |
| --- | --- | --- | --- | --- |
| 1 | [Expense tool] | [Category rules] | [Rule set as per mapping in this appendix] | [BR-01] |

**Field and account mappings**

| Source field or value | Target field or value | Rule | BR ID |
| --- | --- | --- | --- |
| [Expense category: Travel – flights] | [GL 6100, GST on purchases, Dept from employee] | [Default unless overridden] | [BR-02] |

**Access and roles**

| System | Access needed | Environment | Granted by (role) | Status |
| --- | --- | --- | --- | --- |
| [ERP] | [Integration role with read on transactions, write on journals] | [Sandbox, then production] | [ERP admin] | [Requested] |

**Test data and test cases**

| # | Scenario | Test data | Expected result |
| --- | --- | --- | --- |
| 1 | [Standard card line with receipt] | [Sample month, DOC-0x] | [Coded correctly with no manual step] |
| 2 | [Line with no rule match] | [] | [Appears in the review list with a suggestion] |

**Acceptance criteria**

- [e.g. At least [X]% of lines coded without manual change across one full month]
- [e.g. Every AI suggestion logged with confidence and reviewer]
- [e.g. Client UAT signed off by [role]]

**Cut-over and rollback:** [Parallel run period, switch-over date, how to revert to the current process if needed.]

**Run-state support:** [Owner, monitoring, support arrangement after go-live, per the section 9 RACI.]
