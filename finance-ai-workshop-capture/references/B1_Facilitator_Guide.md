# B1 – Facilitator Guide

How to run a Finance AI discovery session. Written so a finance SME can lead a half-day process session without the engagement director in the room.

*Guidance: read this with the tailored question bank S1 produces for the client, and the hypothesis pack (A5) for the process.*

## Roles

| Role | Who | Job in the room |
| --- | --- | --- |
| Facilitator | Finance SME | Runs the agenda, asks the questions, keeps time, owns the exit checklist |
| Scribe / mapper | Second SME or consultant | Draws the process live in the Process Mapper (B6) on the shared screen; notes in B3 what the map doesn't hold (volumes, rules, quotes) with timestamps |
| Technical listener | Director or tech lead (optional) | Listens for system access, API and data issues; asks the SOL questions |

With only two people, the facilitator also covers the technical listener's SOL questions.

## The day before

- [ ] Hypothesis pack (A5) read: draft process card, suspected pain points, candidate use cases, gap list
- [ ] Tailored question bank printed or open, with the gap questions marked
- [ ] B3 capture sheet created for the session, header filled in
- [ ] Process Mapper open (hosted link, or `process_mapper.html` from skill S1 or S2), with the draft map for the process imported (from S1 `create-process-map`, or **Draft with Claude** in the mapper). If there's no draft, create a new map with the process ID, session code and the swimlanes (roles) listed in A5
- [ ] Draft map reviewed: open AI comments (Claude's "To confirm" items) noted as questions for the session
- [ ] Mapper practised: Enter adds a step, Shift+Enter adds one in the lane below, X adds a decision, ? shows all shortcuts
- [ ] B4 exit checklist printed for the process module
- [ ] Teams meeting set to record and transcribe; consent confirmed (D3)
- [ ] Two or three art-of-the-possible cards (B5) chosen for this process

## Session flow (half day, about 3.5 hours with a break)

| # | Block | Time | Goal | Questions |
| --- | --- | --- | --- | --- |
| 1 | Confirm the draft | 15 min | Correct the draft process card from A5 rather than start blank | Intake answers for this module |
| 2 | Live walkthrough | 60 min | Follow one real transaction from start to end, on screen | Walkthrough question (EXP-11, BNK-05, CFF-07) |
| 3 | Exceptions and controls | 30 min | What goes wrong, how it's caught, who signs off | Module questions on exceptions, controls, timing |
| – | Break | 15 min | Scribe and facilitator check gaps; optionally run S2 on the transcript so far | – |
| 4 | Pain points and ideas | 30 min | Pain points with impact; show B5 cards to spark ideas | CORE-18 confirmations, module effort questions |
| 5 | Solution fit | 30 min | Can it be built with what they have, and who owns it | SOL-01 to SOL-06 |
| 6 | Close-out | 15 min | Every B4 box ticked or logged as an open question | B4 checklist |

### 1. Confirm the draft (15 min)

Put the draft process card on screen. Ask "What's wrong or missing here?" rather than "Tell us about the process". People correct a draft faster than they describe from scratch.

If Claude drafted the map, put the map on screen instead of the card and walk the open AI comments: confirm or correct each one, then resolve the comment. Before the map is exported for S2, the Claude-draft comment on the start node and every "To confirm" comment should be resolved or turned into an open question.

### 2. Live walkthrough (60 min)

- Ask for **one real, recent transaction**, not a description of the process in general.
- **Map it live where everyone can see it.** Share the Process Mapper screen (or put it beside the client's screen) and draw each step as it's described, in the lane of the role who does it:
    - a step for each action (record the system and minutes per item in the side panel)
    - a **decision (X)** where the path splits either/or, with each connector labelled ("Yes", "Over $500")
    - **AND** where several things must all happen; **OR** where one or more may happen
    - a connector back to an earlier step for rework loops
    - a **sub-process (S)** when a step turns out to hold several steps of its own: it opens a new map under that step; **U** takes you back up
    - a **link (J)** where the flow continues in another process (e.g. purchase order → goods receipt), so the processes connect and you can click through
    - a **description** for any step that needs more than its name, and the **system** for any node, including decisions
    - flag **manual work (M)**, **controls (K)** and **pain points (!)** as you go, and add a comment for anything to confirm
- At each decision, ask the room "Is this right? What else can happen here?" Correcting the map on screen removes the ambiguity of describing a process aloud.
- At each step ask: who does this, in which system, how long does it take, and what do you check?
- Ask them to say volumes and times out loud, e.g. "So that's about 20 minutes a day?". The transcript needs the number.
- Note every copy-paste, re-key, lookup and email; these are manual touchpoints.
- Don't solve problems yet. Write ideas down and park them for block 4.

### 3. Exceptions and controls (30 min)

- "What went wrong last month?" works better than "What can go wrong?"
- For each exception, get how often it happens, how it's found, and how long it takes to fix.
- Confirm who reviews and approves, at what limit, and how sign-off is evidenced. Watch for the same person preparing and reviewing.

### 4. Pain points and ideas (30 min)

- Read back the pain points heard so far, then ask "What else would you fix if you could?"
- For each pain point, push for impact in hours, errors or risk, and who raised it.
- Show two or three B5 cards and ask "Would something like this help here? What would stop it working?"

### 5. Solution fit (30 min)

Ask SOL-01 to SOL-06. These questions decide the delivery tier, so don't skip them.

- **Tier 1, configure existing tool:** licensed features not switched on, rules not set up.
- **Tier 2, low-code AI in the client's tools:** Copilot, Copilot Studio, Power Automate, Claude skills and connectors.
- **Tier 3, custom build:** only where tiers 1 and 2 cannot do the job and the client accepts the cost and maintenance.

If no one can say who would own and fix the automation (SOL-04), log it as a readiness gap. Don't recommend the use case for the first phase until it's resolved.

### 6. Close-out (15 min)

Show the finished map once in presentation mode (P) and ask the process owner to confirm it. Then go through the B4 checklist out loud. For each gap, agree who will answer and by when, and read the list back before ending the recording.

## Handling common moments

| When | Do |
| --- | --- |
| "Can AI just do all of this?" | "Possibly some of it. Let's first get exactly how it works today, then look at options together in the report." Don't commit to a solution in the room. |
| A side-topic takes over | Park it on the scribe's open questions list and move on. |
| Only one person knows the process | Note key-person risk (`system.key_person_risk`) and ask who covers when they're away. |
| A number is a guess | Capture it as an estimate. Ask for the report or export that would confirm it, and log that as a document request. |
| Personal data appears on screen | Ask to filter or move on. Don't screenshot it. |
| A senior person dominates | Ask the person who does the work directly: "Is that how it works on a normal day?" |

## After the session (same day)

- [ ] Export the process map (Export → Download JSON, plus an image) and save it with the session code (e.g. W2) in the engagement folder
- [ ] Download the Teams transcript and save it the same way
- [ ] Run S2 with the map export, the transcript, the B3 sheet and any whiteboard photos
- [ ] Review S2's output in C2: correct errors, then set status to Reviewed
- [ ] When answers or corrections come in, fold them into the map with **Draft with Claude → Update this map** (or S2 `update-process-map`) rather than redrawing it, then review the changes listed on the start node
- [ ] Send the client the open questions with owners and due dates
- [ ] Update the gap list for the next session
