# C1 – Finance AI Use Case Library

Deloitte internal. Configure first: prefer T1, then T2; T3 only where T1 and T2 can't do the job.
Hours saved / yr = volume per year × minutes per item today × automation share ÷ 60, using the client's own numbers. Effort is indicative build weeks.

## Delivery tiers

- **T1 Configure existing tool:** Switch on or configure features the client already licenses. Cheapest, lowest risk, maintained by the client's own admin.
- **T2 Low-code AI in client tools:** Add AI or automation using tools in the client's environment: Copilot, Copilot Studio, Power Automate, Claude skills and connectors. No new infrastructure.
- **T3 Custom build:** Code or infrastructure built for the client. Only where T1 and T2 cannot do the job and the client accepts the cost and maintenance.

## Solution patterns

- **Document extraction:** Read receipts, invoices, remittances or statements and turn them into structured data.
- **Matching and reconciliation:** Pair records across two sources (bank to ledger, card to claims) and surface what doesn't match.
- **Anomaly and variance detection:** Flag items that break a rule or look unusual against history.
- **Commentary and narrative generation:** Draft explanations of results, variances or forecasts for a person to edit.
- **Agentic transaction posting:** Prepare and post transactions to the ERP after a person approves them.
- **Finance Q&A assistant:** Answer questions about finance data, policy or process in plain language.
- **Forecasting:** Produce or refresh projections from drivers and data.
- **Workflow and configuration:** Set up rules, feeds, approvals and reminders in existing tools.

## Employee expenses and corporate cards

### L-EXP-01 Card feed and receipt capture set-up

- **Problem:** Card transactions arrive late or incomplete and receipts are matched by hand.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** Expense tool card feeds, receipt scanning and auto-matching (e.g. Expensify card feeds and SmartScan); mobile app
- **How it works:** 1. Move cards to the most reliable feed type the bank and tool support. 2. Turn on receipt scanning by photo and email forwarding. 3. Auto-match receipts to card lines. 4. Report unmatched lines daily.
- **Prerequisites:** Expense tool plan that includes card feeds and receipt scanning; card issuer supports the feed; admin access to the expense tool
- **Value driver:** Minutes per card line spent finding and attaching receipts (volume basis: Card transactions per year)
- **Human in the loop:** Employee confirms the matched receipt; finance reviews unmatched lines only
- **Controls:** Feed status monitored daily; unmatched list reviewed weekly; change log of feed settings
- **Indicative effort:** 1-2 weeks
- **Outline build steps:** Confirm plan features; configure feeds in test or with a pilot group; enable scanning; train submitters; roll out by team
- **Known risks:** Bank feed limits by card type; staff not using the mobile app

### L-EXP-02 Expense coding rules

- **Problem:** Finance recodes a large share of expense lines because categories don't map cleanly to the ledger.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** Expense tool category, merchant and tax rules; ERP integration mapping (e.g. Expensify to NetSuite connector)
- **How it works:** 1. Clean the category list. 2. Map each category to GL account, tax code and default dimensions. 3. Add merchant rules for frequent suppliers. 4. Default department or project from the employee record. 5. Sync mapping with the ERP.
- **Prerequisites:** Category-to-GL and tax mapping (A3 DR-09); admin access to the expense tool and integration settings
- **Value driver:** Minutes per line spent recoding (volume basis: Expense lines per year)
- **Human in the loop:** Finance reviews lines with no rule match
- **Controls:** Mapping table owned by finance and changed only through the admin; sample check of coding monthly
- **Indicative effort:** 1-2 weeks
- **Outline build steps:** Analyse a month of coding corrections; agree mapping with FC; configure rules; test with sample data; monitor recode rate
- **Known risks:** Chart of accounts or dimensions change; rules drift without an owner

### L-EXP-03 AI coding suggestion with exception review

- **Problem:** Lines that rules can't code (new merchants, mixed spend, project work) still take finance time every month.
- **Pattern / tier:** Anomaly and variance detection · T2 Low-code AI in client tools
- **Typical tools:** Claude skill with ERP and expense tool connectors, or Copilot Studio agent; expense tool API or export
- **How it works:** 1. Pull uncoded or low-confidence lines. 2. AI proposes account, tax code and dimensions from the receipt, merchant and coding history, with a confidence score and reason. 3. Finance accepts or edits in a review list. 4. Accepted coding is written back. 5. Accepted edits feed new rules.
- **Prerequisites:** API or export access to the expense tool; 6-12 months of coding history; approved AI tool (D3)
- **Value driver:** Minutes per uncoded line (volume basis: Lines not coded by rules per year)
- **Human in the loop:** Finance approves every suggestion below the agreed confidence threshold; sample above it
- **Controls:** Every suggestion logged with confidence and reviewer; no write-back without approval; monthly accuracy check
- **Indicative effort:** 3-5 weeks
- **Outline build steps:** Extract history; define confidence threshold with FC; build skill or agent; test on a past month; run in parallel for one cycle; go live
- **Known risks:** Poor history quality; personal data in receipts (D3); over-reliance on high-confidence suggestions

### L-EXP-04 Policy-breach and duplicate flagging

- **Problem:** Approvers miss duplicates, personal spend and limit breaches, which are found late or not at all.
- **Pattern / tier:** Anomaly and variance detection · T1 Configure existing tool
- **Typical tools:** Expense tool policy rules and violation flags (T1); AI review for patterns rules miss, e.g. split transactions (T2)
- **How it works:** 1. Encode policy limits and non-allowable categories as rules. 2. Flag duplicates, weekend or out-of-pattern spend. 3. Route flagged items to the approver with the reason. 4. Monthly summary of breaches to the FC.
- **Prerequisites:** Current written expense policy (DR-07); approval matrix (DR-08)
- **Value driver:** Errors and recoveries avoided; approver minutes per claim (volume basis: Claims per year)
- **Human in the loop:** Approver decides on every flagged item
- **Controls:** Breach log retained; FC reviews monthly summary; policy rule changes approved by FC
- **Indicative effort:** 1-3 weeks
- **Outline build steps:** Translate policy to rules; configure in tool; test against a past month; add AI pattern check if needed
- **Known risks:** Too many false flags cause approvers to ignore them

### L-EXP-05 Card statement reconciliation

- **Problem:** Reconciling the card statement to what was posted is manual and differences sit unresolved.
- **Pattern / tier:** Matching and reconciliation · T2 Low-code AI in client tools
- **Typical tools:** Power Automate or Claude skill reading the card statement file and the ERP; spreadsheet output or ERP reconciliation
- **How it works:** 1. Load the monthly card statement. 2. Match to posted card transactions by card, date and amount. 3. List differences with likely causes. 4. Preparer resolves; reviewer signs off.
- **Prerequisites:** Card statement in a structured file; ERP report of posted card transactions
- **Value driver:** Hours per monthly card reconciliation (volume basis: Card statements per year)
- **Human in the loop:** Preparer resolves differences; reviewer signs off
- **Controls:** Reconciliation and sign-off retained; unresolved items aged
- **Indicative effort:** 2-3 weeks
- **Outline build steps:** Agree matching keys; build match; test on three past months; document sign-off
- **Known risks:** Statement format changes from the issuer

### L-EXP-06 Missing receipt and late submission chasing

- **Problem:** Finance spends hours each month chasing receipts and late claims.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** Expense tool reminders and escalations; Teams or email notifications (Power Automate) where the tool can't
- **How it works:** 1. Automatic reminder after a set number of days. 2. Escalate to the manager after a second period. 3. Weekly list of outstanding items to finance.
- **Prerequisites:** Agreed submission deadlines in policy
- **Value driver:** Minutes spent chasing per item (volume basis: Items chased per year)
- **Human in the loop:** Finance handles escalated items only
- **Controls:** Outstanding list reviewed before month end
- **Indicative effort:** 1 week
- **Outline build steps:** Agree timings; configure reminders; communicate to staff
- **Known risks:** Reminder fatigue

## Bank statements into the ERP

### L-BNK-01 Direct bank feed into the ERP

- **Problem:** Statements are downloaded and uploaded by hand, often days late.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** ERP bank feed feature or bank-provided feed (e.g. NetSuite bank feeds); feed aggregator if the bank requires one
- **How it works:** 1. Confirm which accounts the bank and ERP can connect. 2. Set up the feed for each account. 3. Transactions arrive daily for matching.
- **Prerequisites:** Bank supports a feed to the ERP; ERP edition supports it; bank and ERP admin access
- **Value driver:** Minutes per statement download and import (volume basis: Imports per year (accounts x frequency))
- **Human in the loop:** None for import; matching reviewed as today
- **Controls:** Daily check that every feed updated; feed errors alerted
- **Indicative effort:** 1-2 weeks
- **Outline build steps:** Check feed availability and cost; configure in sandbox if available; run in parallel with manual import for a week; switch over
- **Known risks:** Some accounts or banks not supported; feed authorisation expiry

### L-BNK-02 Automated statement file import

- **Problem:** No direct feed is available, so file imports are manual and error-prone.
- **Pattern / tier:** Document extraction · T2 Low-code AI in client tools
- **Typical tools:** Power Automate or Claude skill with ERP API; statement parsing for CSV, OFX, CAMT.053 or MT940
- **How it works:** 1. Statement files saved to an agreed folder (by the bank's scheduled export or a person). 2. Automation validates, converts to the ERP's import format and imports. 3. Import log and errors sent to finance.
- **Prerequisites:** Statement files in a structured format (DR-13); ERP import API or CSV import; folder agreed under D3
- **Value driver:** Minutes per import plus rework from import errors (volume basis: Imports per year)
- **Human in the loop:** Finance reviews import errors and the daily log
- **Controls:** Opening and closing balance check against the statement on every import; log retained
- **Indicative effort:** 2-4 weeks
- **Outline build steps:** Collect format samples; build parser and balance check; test on three months; run in parallel; go live
- **Known risks:** Bank two-factor tied to one person blocks scheduled downloads (BNK-12); format changes

### L-BNK-03 Matching rules configuration

- **Problem:** Most bank lines are matched by hand even though many follow clear patterns.
- **Pattern / tier:** Matching and reconciliation · T1 Configure existing tool
- **Typical tools:** ERP bank matching and reconciliation rules (e.g. NetSuite matching rules)
- **How it works:** 1. Analyse three months of matched lines for patterns. 2. Configure rules by reference, amount and date window. 3. Add rules for recurring items (fees, direct debits, payroll). 4. Track auto-match rate monthly.
- **Prerequisites:** Three months of statements and ERP register (DR-13, DR-14); admin access
- **Value driver:** Minutes per manually matched line (volume basis: Bank lines per year)
- **Human in the loop:** Accountant reviews rule-matched lines in the normal reconciliation
- **Controls:** Rule changes logged and approved by FC; auto-match rate tracked
- **Indicative effort:** 1-2 weeks
- **Outline build steps:** Pattern analysis; draft rules; test in sandbox or on a past period; enable; review rate after a month
- **Known risks:** Over-broad rules mismatch; rules not maintained

### L-BNK-04 AI match suggestions for exceptions

- **Problem:** Hard items (batched receipts, settlements, FX, fees) take the most time and rules can't handle them.
- **Pattern / tier:** Matching and reconciliation · T2 Low-code AI in client tools
- **Typical tools:** Claude skill with ERP connector, or Copilot Studio agent, reading unmatched lines and open ERP transactions
- **How it works:** 1. Pull unmatched bank lines and open ledger items. 2. AI proposes one-to-many or many-to-one matches with a reason and confidence. 3. Accountant accepts or rejects. 4. Accepted matches are applied in the ERP.
- **Prerequisites:** ERP API access; history of how hard items were resolved; approved AI tool (D3)
- **Value driver:** Minutes per hard item (volume basis: Hard items per year (BNK-07))
- **Human in the loop:** Accountant approves every suggested match
- **Controls:** Suggestions and decisions logged; no match applied without approval
- **Indicative effort:** 3-5 weeks
- **Outline build steps:** Classify hard-item types; define matching logic with examples; build; test on past months; parallel run
- **Known risks:** Low volume makes the build hard to justify; incorrect many-to-one matches

### L-BNK-05 Cash application from remittances

- **Problem:** Customer receipts without a clear reference are applied to invoices by manual lookup.
- **Pattern / tier:** Document extraction · T2 Low-code AI in client tools
- **Typical tools:** Claude skill or Copilot reading remittance emails or PDFs; ERP connector to apply payments
- **How it works:** 1. Remittances arrive in a shared mailbox. 2. AI extracts customer, invoices and amounts. 3. Proposes payment application against open invoices. 4. AR approves; payment applied.
- **Prerequisites:** Shared remittance mailbox; ERP API access; AR open-items data
- **Value driver:** Minutes per receipt needing lookup (volume basis: Receipts needing lookup per year (BNK-08))
- **Human in the loop:** AR approves every application
- **Controls:** Extraction and application logged; unapplied cash aged
- **Indicative effort:** 3-5 weeks
- **Outline build steps:** Collect remittance samples; build extraction; build application proposal; test; parallel run
- **Known risks:** Remittance formats vary widely; customers pay without remittance

### L-BNK-06 Reconciliation pack and sign-off evidence

- **Problem:** Reconciliation sign-off is inconsistent and hard to evidence for audit.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** ERP reconciliation reports and approval; or a standard reconciliation template with Power Automate sign-off
- **How it works:** 1. Standard reconciliation report per account. 2. Preparer and reviewer sign off in the system. 3. Ageing of reconciling items.
- **Prerequisites:** Agreed preparer and reviewer roles
- **Value driver:** Review effort and audit queries avoided (volume basis: Reconciliations per year)
- **Human in the loop:** Preparer and reviewer sign off
- **Controls:** Segregation of preparer and reviewer; sign-off retained
- **Indicative effort:** 1 week
- **Outline build steps:** Agree template; configure; train
- **Known risks:** Low; mainly adoption

## Cash flow forecasting

### L-CFF-01 Automated forecast data refresh

- **Problem:** Most of each forecast refresh is spent exporting and pasting data.
- **Pattern / tier:** Workflow and configuration · T1 Configure existing tool
- **Typical tools:** ERP saved searches or reports; Excel Power Query or a Power Automate scheduled export
- **How it works:** 1. Build a saved report for each input (AR, AP, payroll, orders). 2. Connect the model to those reports with Power Query. 3. Refresh pulls current data in one step.
- **Prerequisites:** ERP reporting access; model in Excel; inputs available as ERP reports
- **Value driver:** Hours per refresh on data gathering (volume basis: Refreshes per year)
- **Human in the loop:** Forecast owner checks the refreshed inputs against control totals
- **Controls:** Control totals on each input; refresh log
- **Indicative effort:** 1-3 weeks
- **Outline build steps:** List inputs and sources; build reports; connect model; test against a past refresh
- **Known risks:** Report changes break the connection

### L-CFF-02 Driver-based 13-week cash forecast

- **Problem:** The forecast is a fragile spreadsheet with hard-coded assumptions that one person understands.
- **Pattern / tier:** Forecasting · T2 Low-code AI in client tools
- **Typical tools:** Structured Excel model with documented drivers; Copilot in Excel or a Claude skill to apply drivers and roll the forecast
- **How it works:** 1. Agree drivers (debtor days, payment runs, payroll dates, seasonality). 2. Rebuild the model around drivers and refreshed data. 3. Roll forward weekly. 4. Owner reviews and adjusts.
- **Prerequisites:** Current model (DR-16); input reports (CFF-01); agreed drivers with an owner
- **Value driver:** Hours per refresh plus key-person risk removed (volume basis: Refreshes per year)
- **Human in the loop:** Owner approves drivers and the final forecast
- **Controls:** Driver changes logged; version control; actual-versus-forecast tracked
- **Indicative effort:** 3-6 weeks
- **Outline build steps:** Model review; driver workshop; rebuild; back-test on past weeks; handover and training
- **Known risks:** Drivers not maintained; scope creep into full FP&A

### L-CFF-03 Forecast versus actual tracking

- **Problem:** Forecast accuracy isn't measured, so the forecast doesn't improve.
- **Pattern / tier:** Anomaly and variance detection · T1 Configure existing tool
- **Typical tools:** Excel or BI report comparing saved forecasts to actual cash
- **How it works:** 1. Save each forecast version. 2. Compare to actual cash by category. 3. Track accuracy over time and flag large variances.
- **Prerequisites:** Forecast versions kept; actual cash by category from the ERP
- **Value driver:** Better decisions and fewer surprises (qualitative); hours to compile variance (volume basis: Refreshes per year)
- **Human in the loop:** Owner reviews variances
- **Controls:** Saved versions not overwritten
- **Indicative effort:** 1-2 weeks
- **Outline build steps:** Define categories; build comparison; review monthly
- **Known risks:** Low

### L-CFF-04 Forecast and variance commentary drafting

- **Problem:** Writing commentary for the forecast and variances takes the FC hours each cycle.
- **Pattern / tier:** Commentary and narrative generation · T2 Low-code AI in client tools
- **Typical tools:** Copilot in Excel or Word, or a Claude skill reading the model and variance report
- **How it works:** 1. AI reads the forecast, movements and variances. 2. Drafts commentary in the agreed format. 3. FC edits and approves.
- **Prerequisites:** Structured forecast and variance outputs; examples of past commentary; approved AI tool (D3)
- **Value driver:** Hours per cycle writing commentary (volume basis: Commentary cycles per year)
- **Human in the loop:** FC edits and approves every commentary
- **Controls:** Draft and final versions retained; figures in commentary checked against the model
- **Indicative effort:** 2-3 weeks
- **Outline build steps:** Collect past commentary; agree format; build prompt or skill; test on past cycles
- **Known risks:** AI states a figure wrongly; generic commentary

### L-CFF-05 Scenario assistant

- **Problem:** Scenario requests (a customer pays late, a large capex) are slow to model.
- **Pattern / tier:** Finance Q&A assistant · T2 Low-code AI in client tools
- **Typical tools:** Copilot in Excel or a Claude skill working on the driver-based model
- **How it works:** 1. User asks a what-if question in plain language. 2. Assistant changes the relevant drivers in a copy of the model. 3. Shows the cash impact by week. 4. Owner checks before sharing.
- **Prerequisites:** Driver-based model (L-CFF-02)
- **Value driver:** Hours per scenario (volume basis: Scenarios per year)
- **Human in the loop:** Owner checks every scenario before it is shared
- **Controls:** Scenarios run on copies; base model unchanged
- **Indicative effort:** 2-3 weeks
- **Outline build steps:** Agree common scenarios; build; test; train
- **Known risks:** Depends on L-CFF-02 being in place
