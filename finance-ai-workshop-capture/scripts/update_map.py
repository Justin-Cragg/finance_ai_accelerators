#!/usr/bin/env python3
"""Update an existing Process Mapper map with Claude, without redrawing it.

Step 1  update_map.py outline <export.json> [--map P-01] --out current_outline.json
        Writes the map as an outline (references/process_map_outline.md, "Updating an
        existing map"): every step keeps its node id, with its open comments listed.
Step 2  Claude edits that outline: changes steps, adds steps with new ids, leaves out
        steps to remove, and lists what it changed in "changes".
Step 3  update_map.py apply <export.json> <revised_outline.json> --out <updated.json>
        Merges the revised outline into the map: kept steps keep their comments,
        sub-processes and links; new steps get "To confirm" comments; removed steps go;
        answered comments are resolved with the answer. Re-lays out the map and writes
        a bundle marked "update", which the mapper's Import replaces in place.
"""
import argparse, copy, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draft_map import layout, build, uid, TYPES, FLAGS, NOW, warnings  # noqa: E402

FIELDS = ("description", "system", "minutes", "pain", "idea", "notes")


def load_maps(path):
    d = json.load(open(path))
    return d["maps"] if isinstance(d, dict) and "maps" in d else [d]


def pick(maps, ref):
    tops = [m for m in maps if not m.get("parent")]
    if ref:
        hit = [m for m in maps if ref in (m.get("id"), m.get("process_id")) or (m.get("process_name", "").lower() == ref.lower())]
        if not hit:
            sys.exit(f"No map matches '{ref}'. Maps in the file: " + ", ".join(f"{m.get('process_id')} {m.get('process_name')}" for m in maps))
        return hit[0]
    if len(tops) != 1:
        sys.exit("The file holds several maps; say which with --map (process ID or name): " + ", ".join(f"{m.get('process_id')} {m.get('process_name')}" for m in tops))
    return tops[0]


def to_outline(m, maps):
    lane = {l["id"]: l["name"] for l in m["lanes"]}
    steps = []
    for n in m["nodes"]:
        s = {"id": n["id"], "type": n["type"], "label": n.get("label", ""), "lane": lane.get(n["lane"], "")}
        nxt = [{"to": e["to"], "label": e["label"]} if e.get("label") else e["to"] for e in m["edges"] if e["from"] == n["id"]]
        if nxt:
            s["next"] = nxt
        for f in FIELDS:
            if n.get(f) not in (None, ""):
                s[f] = n[f]
        fl = [f for f, v in (n.get("flags") or {}).items() if v]
        if fl:
            s["flags"] = fl
        oc = [{"id": c["id"], "text": c["text"]} for c in n.get("comments") or [] if not c.get("resolved")]
        if oc:
            s["open_comments"] = oc
        if n.get("subprocess"):
            s["keep_subprocess"] = True
        if n["type"] == "link" and n.get("link"):
            t = next((x for x in maps if x["id"] == n["link"].get("map_id")), None)
            s["link_to"] = (t.get("process_id") or t.get("process_name")) if t else n.get("label")
        steps.append(s)
    return {"map_id": m["id"], "engagement": m.get("engagement", ""), "session": m.get("session", ""),
            "processes": [{"process_id": m.get("process_id", ""), "process_name": m.get("process_name", ""), "module": m.get("module", "GEN"),
                           "lanes": [l["name"] for l in m["lanes"]], "steps": steps}],
            "changes": [], "resolve": []}


def apply(m, rev, maps):
    """Merge a revised outline into map m in place. Returns (changes, new_sub_maps)."""
    p = rev["processes"][0] if "processes" in rev else rev
    steps = p.get("steps") or []
    old = {n["id"]: n for n in m["nodes"]}
    # lanes: keep ids by name, follow the outline's order, add new ones, keep unused old lanes only if still used
    lane_by_name = {l["name"]: l for l in m["lanes"]}
    names = list(dict.fromkeys((p.get("lanes") or []) + [s.get("lane") for s in steps if s.get("lane")]))
    lanes = [lane_by_name.get(nm) or {"id": uid("l-"), "name": nm} for nm in names] or m["lanes"][:1]
    lane_id = {l["name"]: l["id"] for l in lanes}
    ids, nodes, kids = {}, [], []
    used = set(old)
    nxt_num = 1
    for s in steps:
        sid = str(s.get("id") or "")
        t = s.get("type", "task")
        if t not in TYPES:
            warnings.append(f"{sid}: unknown type '{t}'; used task"); t = "task"
        if sid in old and sid not in ids.values():
            n = old[sid]; ids[sid] = sid; is_new = False
        else:
            while f"n{nxt_num}" in used:
                nxt_num += 1
            nid = f"n{nxt_num}"; used.add(nid); ids[sid] = nid; is_new = True
            n = {"id": nid, "type": t, "label": "", "description": "", "lane": "", "slot": 0, "x": 0, "system": "", "minutes": "",
                 "flags": {}, "pain": "", "idea": "", "notes": "", "comments": [], "subprocess": None, "link": None}
        n["type"] = t
        if "label" in s:
            n["label"] = s["label"] or n["label"]
        n["lane"] = lane_id.get(s.get("lane")) or n.get("lane") or lanes[0]["id"]
        if n["lane"] not in lane_id.values():
            n["lane"] = lanes[0]["id"]
        for f in FIELDS:
            if f in s:
                n[f] = s[f] if s[f] is not None else ""
        if t != "task":
            n["minutes"] = ""
        if "flags" in s:
            bad = [f for f in s["flags"] or [] if f not in FLAGS]
            if bad:
                warnings.append(f"{sid}: unknown flags {bad} ignored")
            n["flags"] = {f: True for f in s["flags"] or [] if f in FLAGS}
        if s.get("source"):
            src = f"Source: {s['source']}"
            if src not in (n.get("notes") or ""):
                n["notes"] = ((n.get("notes") or "") + "\n" + src).strip()
        if s.get("confirm"):
            n.setdefault("comments", []).append({"id": uid("c-"), "by": "AI", "at": NOW, "text": "To confirm: " + s["confirm"], "resolved": False})
        if n.get("flags", {}).get("pain") and not n.get("pain"):
            n["pain"] = n.get("description") or n["label"]
        if t != "task" and n.get("subprocess"):
            warnings.append(f"'{n['label']}' is no longer a step, so its sub-process is detached (still in the file)"); n["subprocess"] = None
        if t == "task" and s.get("subprocess") and not n.get("subprocess"):
            kids.append((n, s["subprocess"]))
        n["_link_to"] = s.get("link_to") if t == "link" else None
        if t != "link":
            n["link"] = None
        n["_new"] = is_new
        nodes.append(n)
    removed = [o for i, o in old.items() if i not in ids.values()]
    edges_old = {(e["from"], e["to"]): e for e in m["edges"]}
    edges = []
    for s in steps:
        frm = ids[str(s.get("id") or "")]
        for nx in s.get("next") or []:
            to, lab = (nx, "") if isinstance(nx, str) else (str(nx.get("to")), nx.get("label", "") or "")
            if to not in ids:
                warnings.append(f"{s.get('id')}: next '{to}' not found; skipped"); continue
            e = edges_old.get((frm, ids[to]))
            edges.append({"id": e["id"] if e else uid("e-"), "from": frm, "to": ids[to], "label": lab})
    # answered comments
    resolved = 0
    by_cid = {c["id"]: c for n in nodes for c in n.get("comments") or []}
    for r in rev.get("resolve") or []:
        c = by_cid.get(r.get("comment_id"))
        if c and not c.get("resolved"):
            c["resolved"] = True; c["text"] += f" | Answer (Claude): {r.get('answer', '').strip()}"; resolved += 1
        elif not c:
            warnings.append(f"resolve: comment '{r.get('comment_id')}' not found")
    changes = [str(c) for c in rev.get("changes") or []]
    if not changes:
        warnings.append("The revised outline lists no 'changes'; describe each change so the team can review it")
    # links
    pool = [x for x in maps if not x.get("parent")]
    for n in nodes:
        ref = n.pop("_link_to", None)
        if n["type"] != "link" or not ref:
            continue
        tgt = next((x for x in pool if x.get("process_id") == ref or x.get("process_name", "").lower() == str(ref).lower()), None)
        if tgt:
            n["link"] = {"map_id": tgt["id"]}; n["label"] = n["label"] or (tgt.get("process_id", "") + " " + tgt.get("process_name", "")).strip()
        elif not n.get("link"):
            n["label"] = n["label"] or str(ref); warnings.append(f"link to '{ref}' not found; choose the map on the link node")
    for n in nodes:
        n.pop("_new", None)
    m["lanes"] = [l for l in lanes if any(n["lane"] == l["id"] for n in nodes) or l["name"] in (p.get("lanes") or [])]
    m["nodes"], m["edges"] = nodes, edges
    if p.get("process_name"):
        m["process_name"] = p["process_name"]
    # record the update on the start node
    st = next((n for n in nodes if n["type"] == "start"), None)
    if st is not None:
        st.setdefault("comments", []).append({"id": uid("c-"), "by": "AI", "at": NOW, "resolved": False,
            "text": "Updated by Claude: " + ("; ".join(changes) if changes else "changes not listed") + (f". Resolved {resolved} comment(s) from the source." if resolved else "") + " Review and resolve."})
    for n in nodes:  # checks
        if n["type"] not in ("end", "link") and not any(e["from"] == n["id"] for e in edges):
            warnings.append(f"'{n['label']}' has no next step")
        if n["type"] in ("xor", "or", "and"):
            if sum(1 for e in edges if e["from"] == n["id"]) < 2 and sum(1 for e in edges if e["to"] == n["id"]) < 2:
                warnings.append(f"gateway '{n['label']}' has fewer than two branches")
    for o in removed:
        if o.get("subprocess"):
            warnings.append(f"removed '{o['label']}' had a sub-process; it stays in the file, detached")
    layout(m)
    m["updated"] = NOW
    m.setdefault("generated", None)
    m["updated_by_claude"] = {"at": NOW, "changes": changes}
    subs = []
    for n, sub in kids:
        d = dict(sub); d.setdefault("process_id", (m.get("process_id") or "P") + "." + n["id"][1:]); d.setdefault("process_name", n["label"])
        d.setdefault("module", m.get("module", "GEN")); d["lanes"] = d.get("lanes") or [l["name"] for l in m["lanes"]]
        made = build(d, m.get("engagement", ""), m.get("session", ""), "update", {"map_id": m["id"], "node_id": n["id"]}, n["label"])
        for x in made:
            for y in x["nodes"]:
                y.pop("_link_to", None)
        n["subprocess"] = made[0]["id"]; subs += made
    summary = {"kept": sum(1 for n in nodes if n["id"] in old), "added": sum(1 for n in nodes if n["id"] not in old),
               "removed": [o["label"] for o in removed], "comments_resolved": resolved, "new_sub_processes": len(subs)}
    return changes, subs, summary


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a1 = sp.add_parser("outline"); a1.add_argument("export"); a1.add_argument("--map"); a1.add_argument("--out", required=True)
    a2 = sp.add_parser("apply"); a2.add_argument("export"); a2.add_argument("revised"); a2.add_argument("--out", required=True)
    a = ap.parse_args()
    maps = load_maps(a.export)
    if a.cmd == "outline":
        m = pick(maps, a.map)
        json.dump(to_outline(m, maps), open(a.out, "w"), indent=1)
        print(json.dumps({"map": f"{m.get('process_id')} {m.get('process_name')}", "steps": len(m["nodes"]),
                          "open_comments": sum(1 for n in m["nodes"] for c in n.get("comments") or [] if not c.get("resolved")), "out": a.out}, indent=1))
        return
    rev = json.load(open(a.revised))
    m = next((x for x in maps if x["id"] == rev.get("map_id")), None) or pick(maps, (rev.get("processes") or [{}])[0].get("process_id"))
    m = copy.deepcopy(m)
    changes, subs, summary = apply(m, rev, maps)
    bundle = {"schema": "finance-ai-process-map-bundle/2", "exported": NOW, "scope": "update by Claude", "update": True,
              "engagement": m.get("engagement", ""), "root_ids": [m["id"]], "maps": [m] + subs}
    json.dump(bundle, open(a.out, "w"), indent=1)
    print(json.dumps({"map": f"{m.get('process_id')} {m.get('process_name')}", **summary, "changes": changes, "warnings": warnings, "out": a.out}, indent=1))


if __name__ == "__main__":
    main()
