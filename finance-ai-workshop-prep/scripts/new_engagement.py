#!/usr/bin/env python3
"""Create a client's engagement files from the templates bundled in this skill (assets/).

Usage: new_engagement.py --client "Client Ltd" --code CLI-2026 --modules EXP,BNK,CFF
                         [--other "AP invoices;Month-end close"] [--return-by 2026-12-01]
                         [--contact "Name, email"] [--outdir DIR]
Creates in DIR (default: current folder):
  <code>_C2_Engagement_Workbook.xlsx   the engagement workbook, Engagement tab started
  <code>_A2_Intake_Questionnaire.xlsx  the client intake: About you, one tab per module in scope,
                                       one "Other process" tab per --other process, Documents trimmed to scope
Modules: EXP (expenses), BNK (bank statements), CFF (cash flow forecasting). Anything else goes in --other (GEN).
"""
import argparse, os, re, shutil, sys
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
sys.path.insert(0, HERE)
import c2_io

TAB = {"EXP": "Expenses", "BNK": "Bank statements", "CFF": "Cash flow forecast"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client", required=True); ap.add_argument("--code", required=True)
    ap.add_argument("--modules", default=""); ap.add_argument("--other", default="")
    ap.add_argument("--return-by", default="[date]"); ap.add_argument("--contact", default="[Deloitte contact]")
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args()
    mods = [m.strip().upper() for m in a.modules.split(",") if m.strip()]
    bad = [m for m in mods if m not in TAB]
    if bad:
        sys.exit(f"Unknown module(s) {bad}. Use EXP, BNK, CFF; put other processes in --other.")
    others = [o.strip() for o in a.other.split(";") if o.strip()]
    if not mods and not others:
        sys.exit("Give at least one module or one --other process.")
    os.makedirs(a.outdir, exist_ok=True)
    code = re.sub(r"[^A-Za-z0-9_-]+", "-", a.code)

    # ---- C2 ----
    c2 = os.path.join(a.outdir, f"{code}_C2_Engagement_Workbook.xlsx")
    shutil.copy(os.path.join(ASSETS, "C2_Engagement_Workbook.xlsx"), c2)
    wb = load_workbook(c2)
    eg = wb["Engagement"]
    rows = c2_io.engagement_rows(eg)
    eg.cell(row=rows["client"], column=3).value = a.client
    eg.cell(row=rows["processes_in_scope"], column=3).value = ", ".join(mods + [f"GEN: {o}" for o in others])
    rd = wb["Read me"]
    rd["A2"] = f"{a.client} ({code}) · System of record for the engagement. Shared online during the engagement; final version to iManage."
    c2_io.rebuild_chart(wb)
    wb.save(c2)

    # ---- A2 ----
    a2 = os.path.join(a.outdir, f"{code}_A2_Intake_Questionnaire.xlsx")
    wb = load_workbook(os.path.join(ASSETS, "A2_Intake_Questionnaire.xlsx"))
    wb["Start here"]["A2"] = f"{a.client} · Please return by {a.return_by} to {a.contact}"
    for m, tab in TAB.items():
        if m not in mods and tab in wb.sheetnames:
            del wb[tab]
    gen = wb["Other process"]
    used = set(wb.sheetnames)
    for o in others:
        ws = wb.copy_worksheet(gen)
        name = re.sub(r"[\[\]:*?/\\]", "", o)[:31] or "Other process"
        base, i = name, 2
        while name in used:
            name = f"{base[:28]} {i}"; i += 1
        used.add(name)
        ws.title = name
        ws["A1"] = f"Other process: {o}"
        ws["A2"] = "Please answer for this process only."
        for col, dim in gen.column_dimensions.items():
            ws.column_dimensions[col].width = dim.width
        ws.freeze_panes = gen.freeze_panes
        ws.sheet_view.showGridLines = False
    del wb["Other process"]
    # order: Start here, About you, module tabs, other processes, Documents
    order = ["Start here", "About you"] + [TAB[m] for m in mods] + [s for s in wb.sheetnames if s not in ("Start here", "About you", "Documents", *TAB.values())] + ["Documents"]
    wb._sheets = [wb[s] for s in order if s in wb.sheetnames]
    # trim document requests to scope
    keep = {"All"} | {TAB[m] for m in mods} | ({"Other process"} if others else set())
    docs = wb["Documents"]
    for r in range(docs.max_row, 4, -1):
        v = docs.cell(row=r, column=2).value
        if v and v not in keep:
            docs.delete_rows(r)
    wb.save(a2)
    print(f"Created:\n  {c2}\n  {a2}\nIntake tabs: {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
