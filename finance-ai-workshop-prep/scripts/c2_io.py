#!/usr/bin/env python3
"""Read and write the Finance AI C2 engagement workbook and read the A2 intake.

Commands
  read <c2.xlsx> [--tab TAB]          Print records as JSON {tab_key: [records]} (+ "engagement": {field: value})
  summary <c2.xlsx>                   Print counts, hours and quadrants as JSON (values as last calculated in Excel)
  append <c2.xlsx> <records.json> [--out OUT.xlsx]
                                      Append records. JSON: {"process": [{...}], "engagement": {...}, ...}
                                      Keys must match row 2 of the tab. record_status defaults to "Draft (AI)".
                                      Engagement values are written only into empty cells (use --overwrite to replace).
  update <c2.xlsx> <updates.json> [--out OUT.xlsx] [--overwrite]
                                      Fill fields on existing records by ID: {"process": {"P-01": {"volume": 770}}}.
                                      Fills empty cells only unless --overwrite; reports conflicts.
  intake <a2.xlsx>                    Print answered intake questions and document responses as JSON.
  blank <c2.xlsx>                     List required fields still empty per record (uses F0 schema next to this script).

Rows: row 1 labels, row 2 field keys, row 3 example (ignored), records from row 4.
openpyxl drops charts on save, so the Matrix chart is rebuilt on every write.
"""
import json, os, sys, argparse
from openpyxl import load_workbook
from openpyxl.chart import ScatterChart, Reference, Series

TABS = {"attendee": "Attendees", "system": "Systems", "data_flow": "Data flows", "process": "Processes",
        "pain_point": "Pain points", "evidence": "Evidence", "use_case": "Use cases", "score": "Scoring",
        "readiness": "Readiness", "build_requirement": "Build requirements", "open_question": "Open questions",
        "document": "Documents"}
FIRST = 4
HERE = os.path.dirname(os.path.abspath(__file__))


def keys_of(ws):
    return {c.value: c.column for c in ws[2] if c.value}


def records(ws):
    k = keys_of(ws)
    out = []
    for r in range(FIRST, ws.max_row + 1):
        rec = {key: ws.cell(row=r, column=col).value for key, col in k.items()}
        inputs = {kk: v for kk, v in rec.items() if v not in (None, "") and not str(ws.cell(row=r, column=k[kk]).value).startswith("=")}
        if inputs:
            rec["_row"] = r
            out.append(rec)
    return out


def first_empty(ws):
    k = keys_of(ws)
    inputs = [col for key, col in k.items() if not str(ws.cell(row=FIRST, column=col).value or "").startswith("=")]
    r = FIRST
    while any(ws.cell(row=r, column=c).value not in (None, "") and not str(ws.cell(row=r, column=c).value).startswith("=") for c in inputs):
        r += 1
    return r


def rebuild_chart(wb):
    if "Matrix" not in wb.sheetnames or "Scoring" not in wb.sheetnames:
        return
    mx, s = wb["Matrix"], wb["Scoring"]
    mx._charts = []
    k = keys_of(s)
    ch = ScatterChart()
    ch.title = "Use cases: value vs feasibility"; ch.style = 13
    ch.x_axis.title = "Feasibility (weighted, 1-5)"; ch.y_axis.title = "Value (weighted, 1-5)"
    ch.x_axis.scaling.min = 1; ch.x_axis.scaling.max = 5; ch.y_axis.scaling.min = 1; ch.y_axis.scaling.max = 5
    last = max(s.max_row, FIRST + 99)
    ser = Series(Reference(s, min_col=k["value_score"], min_row=3, max_row=last),
                 Reference(s, min_col=k["feasibility_score"], min_row=3, max_row=last), title="Use cases")
    ser.marker.symbol = "circle"; ser.marker.size = 9; ser.graphicalProperties.line.noFill = True
    ch.series.append(ser); ch.legend = None; ch.height = 12; ch.width = 18
    mx.add_chart(ch, "A4")


def norm(v):
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return v


def engagement_rows(ws):
    return {ws.cell(row=r, column=1).value: r for r in range(2, ws.max_row + 1) if ws.cell(row=r, column=1).value}


def cmd_read(a):
    wb = load_workbook(a.workbook, data_only=True)
    out = {}
    if not a.tab or a.tab == "engagement":
        eg = wb["Engagement"]
        out["engagement"] = {eg.cell(row=r, column=1).value: eg.cell(row=r, column=3).value for r in range(2, eg.max_row + 1) if eg.cell(row=r, column=1).value}
    for key, tab in TABS.items():
        if a.tab and a.tab != key:
            continue
        out[key] = records(wb[tab])
    print(json.dumps(out, indent=1, default=str))


def cmd_summary(a):
    wb = load_workbook(a.workbook, data_only=True)
    s = {t: len(records(wb[TABS[t]])) for t in TABS}
    procs = records(wb["Processes"])
    ucs = records(wb["Use cases"])
    sc = records(wb["Scoring"])
    num = lambda x: x if isinstance(x, (int, float)) else 0
    res = {"counts": s,
           "process_hours_per_year": sum(num(p.get("hours_per_year")) for p in procs),
           "use_case_hours_saved": {u.get("id"): u.get("hours_saved") for u in ucs},
           "quadrants": {x.get("use_case_id"): x.get("quadrant") for x in sc},
           "record_status": {t: {st: sum(1 for r in records(wb[TABS[t]]) if r.get("record_status") == st) for st in ("Draft (AI)", "Reviewed", "Confirmed with client")} for t in TABS},
           "note": "Calculated values are as last saved by Excel or LibreOffice; recalculate after writing."}
    print(json.dumps(res, indent=1, default=str))


def cmd_append(a):
    data = json.load(open(a.records))
    wb = load_workbook(a.workbook)
    report = {"appended": {}, "skipped_engagement": [], "errors": []}
    if "engagement" in data:
        eg = wb["Engagement"]; rows = engagement_rows(eg)
        for k, v in data["engagement"].items():
            if k not in rows:
                report["errors"].append(f"engagement.{k}: unknown field"); continue
            c = eg.cell(row=rows[k], column=3)
            if c.value not in (None, "") and not a.overwrite:
                report["skipped_engagement"].append(k); continue
            c.value = norm(v)
            if eg.cell(row=rows[k], column=8).value in (None, ""):
                eg.cell(row=rows[k], column=8).value = "Draft (AI)"
    for key, recs in data.items():
        if key == "engagement":
            continue
        if key not in TABS:
            report["errors"].append(f"{key}: unknown tab"); continue
        ws = wb[TABS[key]]; k = keys_of(ws)
        n = 0
        for rec in recs:
            bad = [f for f in rec if f not in k]
            if bad:
                report["errors"].append(f"{key} {rec.get('id', '')}: unknown fields {bad}"); continue
            r = first_empty(ws)
            for f, v in rec.items():
                cell = ws.cell(row=r, column=k[f])
                if str(cell.value or "").startswith("="):
                    continue  # never overwrite formulas
                cell.value = norm(v)
            if "record_status" in k and not rec.get("record_status"):
                ws.cell(row=r, column=k["record_status"]).value = "Draft (AI)"
            n += 1
        report["appended"][key] = n
    rebuild_chart(wb)
    wb.save(a.out or a.workbook)
    print(json.dumps(report, indent=1))


def cmd_update(a):
    data = json.load(open(a.records))
    wb = load_workbook(a.workbook)
    report = {"filled": [], "conflicts": [], "not_found": []}
    for key, by_id in data.items():
        ws = wb[TABS[key]]; k = keys_of(ws)
        idk = "id" if "id" in k else ("use_case_id" if "use_case_id" in k else "dimension")
        index = {ws.cell(row=r, column=k[idk]).value: r for r in range(FIRST, ws.max_row + 1) if ws.cell(row=r, column=k[idk]).value}
        for rid, fields in by_id.items():
            if rid not in index:
                report["not_found"].append(f"{key} {rid}"); continue
            r = index[rid]
            for f, v in fields.items():
                if f not in k:
                    report["not_found"].append(f"{key} {rid}.{f}"); continue
                c = ws.cell(row=r, column=k[f])
                if str(c.value or "").startswith("="):
                    continue
                if c.value not in (None, "") and str(c.value) != str(norm(v)) and not a.overwrite:
                    report["conflicts"].append({"record": f"{key} {rid}", "field": f, "current": c.value, "proposed": norm(v)}); continue
                c.value = norm(v); report["filled"].append(f"{key} {rid}.{f}")
    rebuild_chart(wb)
    wb.save(a.out or a.workbook)
    print(json.dumps(report, indent=1, default=str))


def cmd_intake(a):
    wb = load_workbook(a.workbook, data_only=True)
    out = {"answers": [], "documents": [], "tabs_present": wb.sheetnames}
    for ws in wb.worksheets:
        hdr = {ws.cell(row=4, column=c).value: c for c in range(1, ws.max_column + 1) if ws.cell(row=4, column=c).value}
        if "Your answer" in hdr:
            for r in range(5, ws.max_row + 1):
                qid = ws.cell(row=r, column=hdr["ID"]).value
                ans = ws.cell(row=r, column=hdr["Your answer"]).value
                if qid:
                    out["answers"].append({"id": qid, "tab": ws.title, "question": ws.cell(row=r, column=hdr["Question"]).value,
                                           "answer": ans, "file_ref": ws.cell(row=r, column=hdr["Document or file reference"]).value if "Document or file reference" in hdr else None})
        if "Can you share it?" in hdr:
            for r in range(5, ws.max_row + 1):
                if ws.cell(row=r, column=1).value:
                    out["documents"].append({h: ws.cell(row=r, column=c).value for h, c in hdr.items()})
    out["unanswered"] = [x["id"] for x in out["answers"] if x["answer"] in (None, "")]
    print(json.dumps(out, indent=1, default=str))


def cmd_blank(a):
    schema = json.load(open(os.path.join(HERE, "F0_engagement_data_model.json")))
    wb = load_workbook(a.workbook, data_only=True)
    out = {}
    eg = schema["properties"]["engagement"]["properties"]
    egws = wb["Engagement"]
    vals = {egws.cell(row=r, column=1).value: egws.cell(row=r, column=3).value for r in range(2, egws.max_row + 1)}
    out["engagement"] = [{"field": f, "required_for": p["x-required-for"], "questions": p["x-questions"]}
                         for f, p in eg.items() if p["x-required-for"] != "Optional" and vals.get(f) in (None, "")]
    for key, tab in TABS.items():
        props = schema["properties"][key]["items"]["properties"]
        gaps = []
        for rec in records(wb[tab]):
            missing = [{"field": f, "required_for": p["x-required-for"], "questions": p["x-questions"]}
                       for f, p in props.items()
                       if p["x-required-for"] != "Optional" and p.get("x-source") != "Analysis" and rec.get(f) in (None, "")]
            if missing:
                gaps.append({"record": rec.get("id") or rec.get("use_case_id") or rec.get("dimension"), "missing": missing})
        if gaps:
            out[key] = gaps
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    for name in ("read", "summary", "intake", "blank"):
        s = sp.add_parser(name); s.add_argument("workbook")
        if name == "read":
            s.add_argument("--tab")
    for name in ("append", "update"):
        s = sp.add_parser(name); s.add_argument("workbook"); s.add_argument("records")
        s.add_argument("--out"); s.add_argument("--overwrite", action="store_true")
    a = p.parse_args()
    {"read": cmd_read, "summary": cmd_summary, "append": cmd_append, "update": cmd_update, "intake": cmd_intake, "blank": cmd_blank}[a.cmd](a)
