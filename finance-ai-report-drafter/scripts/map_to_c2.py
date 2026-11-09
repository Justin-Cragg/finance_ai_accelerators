#!/usr/bin/env python3
"""Turn a Process Mapper export (B6) into C2 records for c2_io.py.

Accepts a single map (schema finance-ai-process-map/1 or /2) or a bundle
(finance-ai-process-map-bundle/2: one map with its sub-processes, or all maps in an engagement).

Usage: map_to_c2.py <export.json> [--c2 C2.xlsx] [--outdir DIR]
       map_to_c2.py <export.json> --mermaid        Mermaid flowcharts (one per map) for the report
Writes to DIR (default: next to the export):
  <base>_append.json   new records: processes not yet in C2, pain points, evidence, open questions
  <base>_update.json   fields to fill on processes already in C2 (by process ID)
  <base>_summary.md    per process: fields, step descriptions, linked processes, ideas, candidate data flows
Then:  c2_io.py append C2.xlsx <base>_append.json --out C2_new.xlsx
       c2_io.py update C2_new.xlsx <base>_update.json
Each top-level map is one C2 process. Sub-process steps are folded into their parent step with
nested numbering (3.1, 3.2). Links between maps become the process's linked_processes field.
Safe to re-run: records it already created are skipped. Everything is Draft (AI); nothing is invented.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TYPE_WORD = {"xor": "Decision", "and": "All of", "or": "One or more of"}


def load(path):
    d = json.load(open(path))
    maps = d["maps"] if isinstance(d, dict) and isinstance(d.get("maps"), list) else [d]
    for m in maps:
        if not all(k in m for k in ("nodes", "edges", "lanes")):
            sys.exit("Not a Process Mapper export (each map needs nodes, edges, lanes).")
        m.setdefault("parent", None)
        for n in m["nodes"]:
            for k, v in (("description", ""), ("system", ""), ("subprocess", None), ("link", None), ("flags", {}), ("comments", [])):
                n.setdefault(k, v)
    return maps


def label_of(m):
    return ((m.get("process_id") or "") + " " + (m.get("process_name") or "")).strip()


def ordered_nodes(m):
    nodes = {n["id"]: n for n in m["nodes"]}
    out = {k: [] for k in nodes}
    for e in m["edges"]:
        if e["from"] in nodes and e["to"] in nodes:
            out[e["from"]].append(e)
    starts = sorted([n for n in m["nodes"] if n["type"] == "start"], key=lambda n: n["x"]) or sorted(m["nodes"], key=lambda n: n["x"])[:1]
    indeg = {k: 0 for k in nodes}
    for e in m["edges"]:
        if e["from"] in nodes and e["to"] in nodes and nodes[e["to"]]["x"] > nodes[e["from"]]["x"]:
            indeg[e["to"]] += 1
    seen, order, ready = set(), [], [s["id"] for s in starts]
    while ready:
        ready.sort(key=lambda i: nodes[i]["x"])
        i = ready.pop(0)
        if i in seen:
            continue
        seen.add(i); order.append(i)
        for e in out[i]:
            t = e["to"]
            if nodes[t]["x"] > nodes[i]["x"]:
                indeg[t] -= 1
            if indeg[t] <= 0 and t not in seen:
                ready.append(t)
    order += [n["id"] for n in sorted(m["nodes"], key=lambda n: n["x"]) if n["id"] not in seen]
    return [nodes[i] for i in order], out, nodes


def walk(m, byid, prefix="", path=None, depth=0):
    """Yield (number, node, map, path) for every non start/end node, descending into sub-processes."""
    seq, out, nodes = ordered_nodes(m)
    path = path or [m.get("process_name") or ""]
    k = 0
    for n in seq:
        if n["type"] in ("start", "end"):
            continue
        k += 1
        num = f"{prefix}{k}"
        yield num, n, m, path, out, nodes
        child = byid.get(n.get("subprocess") or "")
        if child and depth < 6:
            yield from walk(child, byid, num + ".", path + [n.get("label") or ""], depth + 1)


def mermaid(m, byid):
    safe = lambda s: re.sub(r'[\[\]{}()<>|]', ' ', str(s or '').replace('"', "'")).strip() or ' '
    L = [f"%% {safe(label_of(m))}{' (sub-process)' if m.get('parent') else ''}", "flowchart LR"]
    for l in m["lanes"]:
        L += [f'  subgraph {re.sub(r"[^A-Za-z0-9_]", "_", l["id"])}["{safe(l["name"])}"]', "    direction LR"]
        for n in [n for n in m["nodes"] if n["lane"] == l["id"]]:
            lab = safe(n.get("label")) + (f"<br/><small>{safe(n['system'])}</small>" if n.get("system") else "")
            tgt = byid.get((n.get("link") or {}).get("map_id", ""))
            shape = {"task": f'[["{lab} ⊞"]]' if n.get("subprocess") else f'["{lab}"]',
                     "start": f'(["{safe(n.get("label")) or "Start"}"])', "end": f'(["{safe(n.get("label")) or "End"}"])',
                     "xor": f'{{"X {lab}"}}', "and": f'{{{{"AND {lab}"}}}}', "or": f'{{{{"OR {lab}"}}}}',
                     "link": f'>"→ {safe(label_of(tgt) if tgt else n.get("label"))}"]'}[n["type"]]
            L.append(f"    {n['id']}{shape}")
        L.append("  end")
    for e in m["edges"]:
        L.append(f"  {e['from']} -->{'|' + safe(e['label']) + '|' if e.get('label') else ''} {e['to']}")
    L += ["  classDef manual fill:#fbf0dd,stroke:#b26b00", "  classDef control fill:#e3edf9,stroke:#2a63a8", "  classDef pain stroke:#c0392b,stroke-width:3px"]
    for c in ("manual", "control", "pain"):
        ids = [n["id"] for n in m["nodes"] if (n.get("flags") or {}).get(c)]
        if ids:
            L.append(f"  class {','.join(ids)} {c}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("export"); ap.add_argument("--c2"); ap.add_argument("--outdir"); ap.add_argument("--mermaid", action="store_true")
    a = ap.parse_args()
    maps = load(a.export)
    byid = {m["id"]: m for m in maps}
    if a.mermaid:
        print("\n\n".join(mermaid(m, byid) for m in maps)); return
    roots = [m for m in maps if not m.get("parent") or m["parent"].get("map_id") not in byid]

    existing = {}
    if a.c2:
        from openpyxl import load_workbook
        import c2_io
        wb = load_workbook(a.c2, data_only=True)
        for key, tab in c2_io.TABS.items():
            existing[key] = c2_io.records(wb[tab])

    def gen(prefix, key, extra=()):
        nums = [int(x) for x in re.findall(rf"\b{prefix}-(\d+)\b", " ".join([str(r.get("id", "")) for r in existing.get(key, [])] + list(extra)))]
        n = max(nums) if nums else 0
        while True:
            n += 1
            yield f"{prefix}-{n:02d}"

    ev_ids, pp_ids, oq_ids = gen("EV", "evidence"), gen("PP", "pain_point"), gen("OQ", "open_question")
    taken_p = [m.get("process_id") or "" for m in roots]
    p_ids = gen("P", "process", taken_p)
    seen_refs = {str(e.get("reference")) for e in existing.get("evidence", [])}
    seen_qs = {str(q.get("question")) for q in existing.get("open_question", [])}
    existing_p = {p.get("id") for p in existing.get("process", [])}

    append = {"process": [], "pain_point": [], "evidence": [], "open_question": []}
    update = {"process": {}}
    md = [f"# Process map capture: {os.path.basename(a.export)}", ""]
    pid_of = {}
    for r in roots:
        pid_of[r["id"]] = r.get("process_id") or next(p_ids)

    for r in roots:
        pid, session = pid_of[r["id"]], r.get("session") or "MAP"
        lanes = {}
        tree = [r]
        for _, n, m, _, _, _ in walk(r, byid):
            pass
        stack = [r]
        while stack:
            x = stack.pop()
            for n in x["nodes"]:
                c = byid.get(n.get("subprocess") or "")
                if c and c not in tree:
                    tree.append(c); stack.append(c)
        for x in tree:
            lanes.update({l["id"]: l["name"] for l in x["lanes"]})
        ref = lambda n, path: f"{session} process map {pid}, {' › '.join(p for p in path[1:] if p) + ' › ' if len(path) > 1 else ''}node {n['id']} ({n.get('label') or n['type']})"

        steps, manual, controls, rules, descs, ideas, hops, notes, links = [], [], [], [], [], [], [], [], []
        for num, n, m, path, out, nodes in walk(r, byid):
            lane = lanes.get(n["lane"], ""); fl = n.get("flags") or {}
            indent = "   " * num.count(".")
            sys_ = f", {n['system']}" if n.get("system") else ""
            if n["type"] == "task":
                mins = f", {n['minutes']} min" if n.get("minutes") not in ("", None) else ""
                steps.append(f"{indent}{num}. {n.get('label','')} ({lane}{sys_}{mins}){' [sub-process]' if n.get('subprocess') else ''}")
            elif n["type"] == "link":
                tgt = byid.get((n.get("link") or {}).get("map_id", ""))
                name = label_of(tgt) if tgt else (n.get("label") or "(not chosen)")
                steps.append(f"{indent}{num}. Continues in linked process: {name} ({lane}{sys_})")
                links.append(f"→ {name}")
            else:
                br = "; ".join(f"{e['label'] + ': ' if e.get('label') else ''}{nodes[e['to']].get('label') or nodes[e['to']]['type']}" for e in out[n["id"]])
                steps.append(f"{indent}{num}. {TYPE_WORD[n['type']]}: {n.get('label','')} ({lane}{sys_}) → {br}")
                if out[n["id"]]:
                    rules.append(f"{n.get('label') or TYPE_WORD[n['type']]}{' [' + n['system'] + ']' if n.get('system') else ''}: " +
                                 "; ".join(f"{e['label'] + ' → ' if e.get('label') else '→ '}{nodes[e['to']].get('label','')}" for e in out[n["id"]]))
            where = f"{lane}{', ' + str(n['minutes']) + ' min' if n.get('minutes') not in ('', None) else ''}"
            if fl.get("manual"):
                manual.append(f"{n.get('label')} ({where})")
            if fl.get("control"):
                controls.append(f"{n.get('label')} ({lane})")
            if n.get("description"):
                descs.append(f"- **{num} {n.get('label') or n['type']}:** {n['description']}")
            if n.get("notes"):
                notes.append(f"- **{num} {n.get('label') or n['type']}:** {n['notes']}")
            if fl.get("idea"):
                ideas.append(f"- {num} {n.get('label')} ({lane}): {n.get('idea') or 'idea flagged, no detail'}")
            for e in out[n["id"]]:
                t = nodes[e["to"]]
                if n.get("system") and t.get("system") and n["system"] != t["system"]:
                    hops.append(f"- {n['system']} → {t['system']} (between '{n.get('label','')}' and '{t.get('label','')}'{'; manual step' if fl.get('manual') or (t.get('flags') or {}).get('manual') else ''})")
            if fl.get("pain") and ref(n, path) not in seen_refs:
                ev = next(ev_ids)
                append["evidence"].append({"id": ev, "source_type": "Process map", "reference": ref(n, path),
                                           "summary": (n.get("pain") or n.get("description") or n.get("label") or "")[:200], "supports": [pid], "confidence": "Medium"})
                append["pain_point"].append({"id": next(pp_ids), "process_id": pid, "description": n.get("pain") or f"Pain point at step {num}: {n.get('label','')}",
                                             "impact": n.get("pain") if re.search(r"\d", n.get("pain") or "") else "", "raised_by_role": "",
                                             "evidence_ids": [ev], "confidence": "Medium"})
            for c in n.get("comments") or []:
                q = f"[{pid} {num} {n.get('label') or n['type']}] {c.get('text','')}"
                if not c.get("resolved") and q not in seen_qs:
                    append["open_question"].append({"id": next(oq_ids), "question": q, "field_ref": f"process {pid}", "owner_role": "", "status": "Open"})
        # incoming links from other maps in the export
        for x in maps:
            for n in x["nodes"]:
                if n["type"] == "link" and (n.get("link") or {}).get("map_id") in [t["id"] for t in tree] and x not in tree:
                    src_root = x
                    while src_root.get("parent") and src_root["parent"].get("map_id") in byid:
                        src_root = byid[src_root["parent"]["map_id"]]
                    links.append(f"← from {pid_of.get(src_root['id'], '')} {src_root.get('process_name','')}".replace("  ", " "))

        systems = sorted({n["system"] for x in tree for n in x["nodes"] if n.get("system")})
        starts = [n.get("label") for n in r["nodes"] if n["type"] == "start" and n.get("label") not in (None, "", "Start")]
        ends = [n.get("label") for n in r["nodes"] if n["type"] == "end" and n.get("label") not in (None, "", "End")]
        nodes_r = {n["id"]: n for n in r["nodes"]}
        rework = [f"{nodes_r[e['from']].get('label','')} → back to {nodes_r[e['to']].get('label','')}{' (' + e['label'] + ')' if e.get('label') else ''}"
                  for e in r["edges"] if e["from"] in nodes_r and e["to"] in nodes_r and nodes_r[e["to"]]["x"] < nodes_r[e["from"]]["x"]]

        map_ref = f"{session} process map {pid} ({os.path.basename(a.export)})"
        prior = [e for e in existing.get("evidence", []) if str(e.get("reference")) == map_ref]
        map_ev = prior[0]["id"] if prior else next(ev_ids)
        if not prior:
            append["evidence"].append({"id": map_ev, "source_type": "Process map", "reference": map_ref,
                                       "summary": f"{r.get('process_name','')} mapped live in session {session}: {sum(1 for s in steps if '(' in s)} steps incl. {len(tree) - 1} sub-process(es).",
                                       "supports": [pid], "confidence": "High"})
        fields = {"steps": "\n".join(steps), "participants": ", ".join(dict.fromkeys(lanes.values())),
                  "manual_touchpoints": "; ".join(manual), "controls": "; ".join(controls), "business_rules": "; ".join(rules),
                  "systems": ", ".join(systems), "trigger_start": "; ".join(starts), "trigger_end": "; ".join(ends),
                  "linked_processes": "; ".join(dict.fromkeys(links))}
        if rework:
            fields["exceptions"] = "Rework loops: " + "; ".join(rework)
        fields = {k: v for k, v in fields.items() if v}
        if pid in existing_p:
            update["process"][pid] = fields
        else:
            append["process"].append(dict(id=pid, name=r.get("process_name", ""), module=r.get("module") or "GEN", evidence_ids=[map_ev], confidence="High", **fields))

        md += [f"## {pid} {r.get('process_name','')} ({session})", "",
               f"{len(tree) - 1} sub-process(es); {len(manual)} manual, {len(controls)} controls. Process {'exists in C2: fields go to the update file (empty cells only).' if pid in existing_p else 'is new: a Processes row is in the append file.'}", "",
               "**Steps**", "", "```", fields.get("steps", ""), "```", ""] + \
              [f"- **{k}:** {v}" for k, v in fields.items() if k != "steps"] + \
              ["", "**Step descriptions** (for Appendix B and the process card)", ""] + (descs or ["- None"]) + \
              ["", "**Step notes** (may hold volumes, rules or exceptions to place in C2)", ""] + (notes or ["- None"]) + \
              ["", "**Automation ideas raised**", ""] + (ideas or ["- None"]) + \
              ["", "**Candidate data flows** (system changes along the flow; confirm before adding)", ""] + (sorted(set(hops)) or ["- None"]) + [""]

    append = {k: v for k, v in append.items() if v}
    update = {k: v for k, v in update.items() if v}
    base = os.path.splitext(os.path.basename(a.export))[0]
    outdir = a.outdir or os.path.dirname(os.path.abspath(a.export))
    json.dump(append, open(os.path.join(outdir, base + "_append.json"), "w"), indent=1)
    json.dump(update, open(os.path.join(outdir, base + "_update.json"), "w"), indent=1)
    open(os.path.join(outdir, base + "_summary.md"), "w").write("\n".join(md))
    print(json.dumps({"processes": {pid_of[r["id"]]: r.get("process_name") for r in roots},
                      "append": {k: len(v) for k, v in append.items()}, "update": {k: list(v) for k, v in update.items()},
                      "files": [base + s for s in ("_append.json", "_update.json", "_summary.md")]}, indent=1))


if __name__ == "__main__":
    main()
