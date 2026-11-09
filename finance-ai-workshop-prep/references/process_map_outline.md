# Process map outline format

Claude writes this outline; `scripts/draft_map.py` validates it, lays it out and turns it into a Process Mapper (B6) file to import. The in-mapper "Draft with Claude" button uses the same format. Write structure only: no coordinates.

```json
{
  "engagement": "TRD-2026",
  "session": "W2",
  "source": "AP procedure v3 (DOC-04); W2 transcript",
  "processes": [
    {
      "process_id": "P-01",
      "process_name": "Purchase orders",
      "module": "GEN",
      "lanes": ["Requester", "Purchasing", "NetSuite"],
      "steps": [
        { "id": "s1", "type": "start", "label": "Need identified", "lane": "Requester", "next": ["s2"] },
        { "id": "s2", "type": "task", "label": "Raise requisition", "lane": "Requester",
          "system": "NetSuite", "minutes": 5,
          "description": "Requester creates a purchase requisition with item, quantity and cost centre.",
          "flags": ["manual"], "source": "DOC-04 p2", "next": ["s3"] },
        { "id": "s3", "type": "xor", "label": "Over $5k?", "lane": "Purchasing", "system": "NetSuite approval routing",
          "next": [ { "to": "s4", "label": "Yes" }, { "to": "s5", "label": "No" } ] },
        { "id": "s4", "type": "task", "label": "FC approves", "lane": "Purchasing", "flags": ["control"],
          "confirm": "Approval limit stated as $5k in the policy but $10k in the workshop", "next": ["s5"] },
        { "id": "s5", "type": "task", "label": "Issue PO to supplier", "lane": "Purchasing",
          "subprocess": {
            "lanes": ["Purchasing"],
            "steps": [
              { "id": "a1", "type": "start", "label": "Start", "lane": "Purchasing", "next": ["a2"] },
              { "id": "a2", "type": "task", "label": "Choose supplier", "lane": "Purchasing", "next": ["a3"] },
              { "id": "a3", "type": "task", "label": "Email PO", "lane": "Purchasing", "flags": ["manual"], "next": ["a4"] },
              { "id": "a4", "type": "end", "label": "PO sent", "lane": "Purchasing" }
            ]
          },
          "next": ["s6"] },
        { "id": "s6", "type": "link", "lane": "Purchasing", "link_to": "P-02" }
      ]
    },
    { "process_id": "P-02", "process_name": "Goods receipt", "lanes": ["Warehouse"], "steps": [] }
  ]
}
```

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `processes[]` | Yes | One per top-level process. Each becomes a map, and one C2 process in S2 |
| `process_id`, `process_name` | Yes | Use the C2 process ID when it exists |
| `module` | No | EXP, BNK, CFF or GEN (default GEN) |
| `lanes` | Yes | Roles (and a lane per key system if useful), in top-to-bottom order. Roles, never people's names |
| `steps[].id` | Yes | Any short unique ID within the process (or sub-process) |
| `steps[].type` | Yes | `start`, `task`, `xor` (either/or decision), `and` (all paths happen), `or` (one or more paths), `link` (continues in another process), `end` |
| `steps[].label` | Yes, except `link` | Short name, verb first for tasks ("Approve invoice"); a question for `xor` ("Over $5k?") |
| `steps[].lane` | Yes | One of `lanes`; the role that does the step |
| `steps[].next` | No | Following steps: IDs, or `{ "to": id, "label": "Yes" }` to label a branch. Leave out on `end` and `link`. A `next` that points back to an earlier step is a rework loop |
| `description` | No | The fuller explanation of what happens |
| `system`, `minutes` | No | System used (any node type); manual minutes per item (tasks) |
| `flags` | No | Any of `manual`, `control`, `pain`, `idea` |
| `pain`, `idea`, `notes` | No | Text for a pain point, an automation idea, or rules and volumes |
| `source` | No | Where this came from (document ID and page, or session + timestamp). Kept in the node's notes as evidence |
| `confirm` | No | Anything inferred or uncertain. Becomes an open comment for the workshop to resolve |
| `subprocess` | No | Tasks only: `{ "lanes": [...], "steps": [...] }`, the same format, one level down (can nest) |
| `link_to` | `link` only | The `process_id` (or name) of another process in this outline, or of an existing map |

## Rules for drafting

- Use only what the sources say. If a step, owner, system or branch is inferred, add `confirm` with what to check. Never invent volumes, minutes or limits.
- One `start`. Every non-`end` step has a `next` unless it is a `link`.
- Put every decision as an `xor`, `and` or `or` node with labelled branches, not inside a task's name.
- Break a step into a `subprocess` when the source describes several steps inside it.
- Use `link` where the source says the work continues in another process; draft that process too if the source covers it.
- Roles, not names. No personal data.

## Updating an existing map

To change a map that already exists, don't redraw it: edit its outline so the team's comments, sub-processes and links survive.

1. `python3 scripts/update_map.py outline <mapper export>.json [--map P-01] --out current.json` writes the map in this format. Each step's `id` is its node id (`n1`, `n2`…). Steps also carry `open_comments` (`[{id, text}]`, read-only) and `keep_subprocess: true` where the step has a sub-process.
2. Edit `current.json` into a revised outline and save it as a new file:
    - **Return every step.** Keep the `id` of each step you keep, even when you change it. Give new steps new ids starting with `new` (`new1`, `new2`…). Leave a step out only to remove it.
    - **Change only what the instruction or source supports.** Leave every other field, lane and connector as it is. To clear a field, set it to `""`. Don't edit `open_comments`.
    - **`confirm`** on a step adds a new "To confirm" comment, as in drafting.
    - **`"changes"`** (top level): one short sentence per change. These go into a comment on the start node so the team can review them.
    - **`"resolve"`** (top level): `[{ "comment_id": "c-…", "answer": "…" }]` where the source clearly answers an open comment. The comment is marked resolved with the answer added.
3. `python3 scripts/update_map.py apply <mapper export>.json revised.json --out <ENGAGEMENT>_<PROCESS-ID>_update.json` merges and re-lays out the map. It prints what was kept, added and removed, the comments answered and any warnings. Fix the warnings and re-run.

The output is marked as an update, so the mapper's **Import** replaces the map in place (same map ID, Ctrl+Z to undo) instead of adding a copy. Removing a step that has a sub-process detaches the sub-process but doesn't delete it.
