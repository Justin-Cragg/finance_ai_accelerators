#!/usr/bin/env python3
"""Build the client-tailored question bank for the workshop facilitator.

Usage: tailor_bank.py <question_bank.csv> <intake.json> <plan.json> <out.xlsx>
  intake.json : output of `c2_io.py intake`
  plan.json   : {"client": "...", "modules": ["EXP", "BNK"],
                 "status": {"EXP-08": "Confirm", "EXP-10": "Ask"},          # optional overrides
                 "probes": {"EXP-08": "Intake says finance codes all lines; confirm the recode rate"},
                 "draft_values": {"EXP-08": "Finance recodes ~80% (intake)"}}
Status per question: Answered (intake answer present, not workshop-only), Confirm (answered but asked in the
workshop too, or overridden), Ask (no answer). CORE and SOL are always included.
"""
import csv, json, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

bank, intake, plan, out = sys.argv[1:5]
qs = list(csv.DictReader(open(bank, encoding="utf-8")))
ans = {a["id"]: a for a in json.load(open(intake))["answers"] if a.get("answer") not in (None, "")}
p = json.load(open(plan))
mods = set(["CORE", "SOL"] + p.get("modules", []))
FILL = {"Ask": "FCE4D6", "Confirm": "FFF2CC", "Answered": "E2EFDA"}
thin = Side(style="thin", color="BFBFBF"); B = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook(); ws = wb.active; ws.title = "Tailored questions"
ws["A1"] = f"Tailored question bank – {p.get('client', '[Client]')}"; ws["A1"].font = Font(name="Arial", size=14, bold=True)
ws["A2"] = "Ask = not answered in the intake · Confirm = answered, check live · Answered = covered; skip unless the walkthrough contradicts it. Draft (AI): review before the session."
ws["A2"].font = Font(name="Arial", size=10, italic=True)
hdr = ["Status", "ID", "Module", "Section", "Question", "Intake answer", "Probe for this client", "Follow-up probes", "Good answer looks like", "Who answers (role)", "Required for", "F0 field"]
ws.append([]); ws.append(hdr)
for c in ws[4]:
    c.font = Font(name="Arial", bold=True, color="FFFFFF", size=10); c.fill = PatternFill("solid", fgColor="1F1F1F"); c.alignment = Alignment(wrap_text=True)
order = {"Ask": 0, "Confirm": 1, "Answered": 2}
rows = []
for q in qs:
    if q["Module"] not in mods:
        continue
    a = ans.get(q["ID"])
    st = "Ask" if not a else ("Confirm" if q["Asked"] != "Intake" else "Answered")
    st = p.get("status", {}).get(q["ID"], st)
    rows.append([st, q["ID"], q["Module"], q["Section"], q["Question"],
                 (a or {}).get("answer") or p.get("draft_values", {}).get(q["ID"], ""),
                 p.get("probes", {}).get(q["ID"], ""), q["Follow-up probes"], q["Good answer looks like"],
                 q["Who answers (role)"], q["Required for"], q["F0 field"]])
rows.sort(key=lambda r: (r[2] not in ("SOL",) and r[2] != "CORE", r[2], order[r[0]], r[1]))
for r in rows:
    ws.append(r)
    for c in ws[ws.max_row]:
        c.font = Font(name="Arial", size=10, bold=(c.column == 2)); c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = B
    ws.cell(row=ws.max_row, column=1).fill = PatternFill("solid", fgColor=FILL[r[0]])
for i, w in enumerate([11, 9, 8, 16, 46, 34, 34, 30, 28, 18, 14, 22], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "C5"; ws.auto_filter.ref = f"A4:L{ws.max_row}"
wb.save(out)
print(json.dumps({k: sum(1 for r in rows if r[0] == k) for k in order}))
