#!/usr/bin/env python3
"""Turn a process map outline (references/process_map_outline.md) into a Process Mapper file.

Usage: draft_map.py <outline.json> --out <maps.json> [--existing <mapper_export.json>]
  --existing  an earlier mapper export, so link_to can point at maps already drawn
Validates the outline, lays each map out (left to right by flow, one row per lane), turns
`confirm` items into open comments, keeps `source` as evidence in the node notes, and writes
a bundle the mapper imports (Import button) and map_to_c2.py reads. Prints warnings to fix.
"""
import argparse, json, random, string, sys
from datetime import datetime, timezone

X0, COL = 200, 210
SIZE = {"task": (170, 62), "start": (44, 44), "end": (44, 44), "xor": (58, 58), "and": (58, 58), "or": (58, 58), "link": (170, 56)}
TYPES = set(SIZE)
FLAGS = {"manual", "control", "pain", "idea"}
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds")
warnings = []


def uid(p):
    return p + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))


def layout(m):
    nodes = {n["id"]: n for n in m["nodes"]}
    out = {k: [] for k in nodes}
    for e in m["edges"]:
        out[e["from"]].append(e["to"])
    # drop back edges (DFS) so loops don't break layering
    state, forward = {}, []

    def visit(i):
        state[i] = 1
        for t in out[i]:
            if state.get(t) == 1:
                continue
            forward.append((i, t))
            if not state.get(t):
                visit(t)
        state[i] = 2
    order = [n["id"] for n in m["nodes"]]
    starts = [i for i in order if nodes[i]["type"] == "start"] + [i for i in order if not any(e["to"] == i for e in m["edges"])]
    for i in starts + order:
        if not state.get(i):
            visit(i)
    indeg = {k: 0 for k in nodes}
    fwd = {k: [] for k in nodes}
    for a, b in dict.fromkeys(forward):
        fwd[a].append(b); indeg[b] += 1
    layer = {k: 0 for k in nodes if indeg[k] == 0}
    q = list(layer)
    deg = dict(indeg)
    while q:
        i = q.pop(0)
        for t in fwd[i]:
            layer[t] = max(layer.get(t, 0), layer[i] + 1)
            deg[t] -= 1
            if deg[t] == 0:
                q.append(t)
    used = {}
    for n in sorted(m["nodes"], key=lambda n: layer.get(n["id"], 0)):
        L = layer.get(n["id"], 0)
        n["x"] = X0 + L * COL + (0 if n["type"] == "task" else (SIZE["task"][0] - SIZE[n["type"]][0]) // 2)
        key = (n["lane"], L)
        n["slot"] = used.get(key, 0)
        used[key] = n["slot"] + 1


def build(outline_proc, engagement, session, source, parent=None, label_path=""):
    lanes_in = list(dict.fromkeys(outline_proc.get("lanes") or []))
    steps = outline_proc.get("steps") or []
    for s in steps:  # lanes used but not declared
        if s.get("lane") and s["lane"] not in lanes_in:
            lanes_in.append(s["lane"]); warnings.append(f"{label_path}: lane '{s['lane']}' used but not listed; added")
    if not lanes_in:
        lanes_in = ["Process owner"]
    lanes = [{"id": uid("l-"), "name": n} for n in lanes_in]
    lane_id = {l["name"]: l["id"] for l in lanes}
    m = {"schema": "finance-ai-process-map/2", "id": uid("map-"), "engagement": engagement, "session": session,
         "process_id": outline_proc.get("process_id", ""), "module": outline_proc.get("module", "GEN"),
         "process_name": outline_proc.get("process_name", "Untitled process"), "example": False, "parent": parent,
         "created": NOW, "updated": NOW, "generated": {"by": "Claude", "at": NOW, "from": source}, "lanes": lanes, "nodes": [], "edges": []}
    if not steps:
        steps = [{"id": "start", "type": "start", "label": "Start", "lane": lanes_in[0]}]
        warnings.append(f"{label_path}: no steps; created an empty map with a start")
    ids = {}
    children = []
    for k, s in enumerate(steps, 1):
        sid = str(s.get("id") or f"s{k}")
        if sid in ids:
            warnings.append(f"{label_path}: duplicate step id '{sid}'; renamed"); sid = f"{sid}_{k}"
        ids[sid] = f"n{k}"
        t = s.get("type", "task")
        if t not in TYPES:
            warnings.append(f"{label_path} {sid}: unknown type '{t}'; used task"); t = "task"
        flags = {f: True for f in (s.get("flags") or []) if f in FLAGS}
        bad = [f for f in (s.get("flags") or []) if f not in FLAGS]
        if bad:
            warnings.append(f"{label_path} {sid}: unknown flags {bad} ignored")
        notes = s.get("notes", "") or ""
        if s.get("source"):
            notes = (notes + "\n" if notes else "") + f"Source: {s['source']}"
        comments = []
        if s.get("confirm"):
            comments.append({"id": uid("c-"), "by": "AI", "at": NOW, "text": "To confirm: " + s["confirm"], "resolved": False})
        n = {"id": f"n{k}", "type": t, "label": s.get("label", "") or ("" if t == "link" else t.title()), "description": s.get("description", ""),
             "lane": lane_id[s.get("lane") or lanes_in[0]], "slot": 0, "x": 0, "system": s.get("system", "") or "",
             "minutes": s.get("minutes", "") if t == "task" else "", "flags": flags, "pain": s.get("pain", "") or "",
             "idea": s.get("idea", "") or "", "notes": notes, "comments": comments, "subprocess": None, "link": None,
             "_link_to": s.get("link_to")}
        if flags.get("pain") and not n["pain"]:
            n["pain"] = n["description"] or n["label"]
        m["nodes"].append(n)
        if s.get("subprocess"):
            if t != "task":
                warnings.append(f"{label_path} {sid}: only tasks can have a sub-process; ignored")
            else:
                children.append((n, s["subprocess"]))
    for k, s in enumerate(steps, 1):
        for nx in s.get("next") or []:
            to, lab = (nx, "") if isinstance(nx, str) else (str(nx.get("to")), nx.get("label", "") or "")
            if to not in ids:
                warnings.append(f"{label_path} {s.get('id')}: next '{to}' not found; skipped"); continue
            m["edges"].append({"id": uid("e-"), "from": f"n{k}", "to": ids[to], "label": lab})
    starts = [n for n in m["nodes"] if n["type"] == "start"]
    if len(starts) != 1:
        warnings.append(f"{label_path}: {len(starts)} start nodes (expected 1)")
    for n in m["nodes"]:
        if n["type"] not in ("end", "link") and not any(e["from"] == n["id"] for e in m["edges"]):
            warnings.append(f"{label_path}: '{n['label']}' has no next step")
        if n["type"] in ("xor", "or", "and"):
            outs = sum(1 for e in m["edges"] if e["from"] == n["id"]); ins = sum(1 for e in m["edges"] if e["to"] == n["id"])
            if outs < 2 and ins < 2:
                warnings.append(f"{label_path}: gateway '{n['label']}' has fewer than two branches")
    if starts:  # first comment on the start: this is a draft
        starts[0]["comments"].insert(0, {"id": uid("c-"), "by": "AI", "at": NOW, "resolved": False,
                                        "text": f"Draft generated by Claude from: {source or 'the sources provided'}. Review every step, owner, system and branch with the client."})
    layout(m)
    out = [m]
    for n, sub in children:
        child_def = dict(sub)
        child_def.setdefault("process_id", (m["process_id"] or "P") + "." + n["id"][1:])
        child_def.setdefault("process_name", n["label"])
        child_def.setdefault("module", m["module"])
        if not child_def.get("lanes"):
            child_def["lanes"] = lanes_in
        sub_maps = build(child_def, engagement, session, source, {"map_id": m["id"], "node_id": n["id"]}, f"{label_path} › {n['label']}")
        n["subprocess"] = sub_maps[0]["id"]
        out += sub_maps
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("outline"); ap.add_argument("--out", required=True); ap.add_argument("--existing")
    a = ap.parse_args()
    o = json.load(open(a.outline))
    if "processes" not in o and "steps" in o:
        o = {"processes": [o], **{k: o.get(k) for k in ("engagement", "session", "source")}}
    maps = []
    for p in o.get("processes", []):
        maps += build(p, o.get("engagement") or "", o.get("session") or "", o.get("source") or "", None, p.get("process_id") or p.get("process_name", "?"))
    existing = []
    if a.existing:
        d = json.load(open(a.existing)); existing = d["maps"] if isinstance(d, dict) and "maps" in d else [d]
    pool = maps + existing
    for m in maps:
        for n in m["nodes"]:
            ref = n.pop("_link_to", None)
            if n["type"] != "link":
                continue
            tgt = next((x for x in pool if not x.get("parent") and ref and (x.get("process_id") == ref or x.get("process_name", "").lower() == str(ref).lower())), None)
            if tgt:
                n["link"] = {"map_id": tgt["id"]}
                n["label"] = n["label"] or ((tgt.get("process_id", "") + " " + tgt.get("process_name", "")).strip())
            else:
                n["label"] = n["label"] or str(ref or "Linked process")
                warnings.append(f"{m['process_id']}: link to '{ref}' not found in this outline or --existing; label kept, choose the map in the mapper")
    bundle = {"schema": "finance-ai-process-map-bundle/2", "exported": NOW, "scope": "draft generated by Claude", "engagement": o.get("engagement") or "",
              "root_ids": [m["id"] for m in maps if not m.get("parent")], "maps": maps}
    json.dump(bundle, open(a.out, "w"), indent=1)
    print(json.dumps({"maps": [{"process_id": m["process_id"], "name": m["process_name"], "steps": sum(1 for n in m["nodes"] if n["type"] == "task"),
                                "sub_process": bool(m.get("parent"))} for m in maps], "warnings": warnings, "out": a.out}, indent=1))


if __name__ == "__main__":
    main()
