# D3 – Data Handling and AI Tool Protocol

How client data is captured, processed, stored and retained on a Finance AI engagement. Every team member follows it, and it must be confirmed before any skill runs on client material.

*Guidance: internal. Confirm the approved-tool list against current Deloitte NZ policy at the start of each engagement and record that check in D2.*

## 1. Approved tools

| Activity | Approved tool | Notes |
| --- | --- | --- |
| Recording and transcription of workshops | Microsoft Teams (recording and transcript) | Recording starts only after consent is confirmed in the session |
| Parsing transcripts and drafting notes | Microsoft Copilot or Claude, in Deloitte-approved environments only | No personal or consumer accounts. Client data is not used for model training |
| Engagement workbook (C2) during the engagement | Shared online workbook in the Deloitte M365 environment | Access limited to the engagement team |
| Final deliverables and retained records | iManage | Moved once the engagement is finalised |
| Receiving client files | Secure share link issued by Deloitte | Not email attachments |

Any other tool requires approval from the engagement director before use, and the approval is recorded in D2.

## 2. Consent to record

- Ask for consent in the kick-off call (A1, KO-13) and again in writing with the pre-read (A4). Record the answer in C2 (`engagement.recording_consent`).
- At the start of each recorded session, the facilitator confirms consent before recording.
- If a client or attendee declines, the scribe's notes (B3) are the only record of that session. Skill S2 runs on the notes alone.

## 3. Personal data

Expense data in particular holds employee names, card numbers and spending details.

- Ask clients to remove or mask employee names and card numbers in sample files where they can (A3 asks them to flag personal data).
- Record whether each file contains personal data in the Documents tab of C2 (`document.personal_data`).
- Do not screenshot personal data shown on screen during sessions.
- Before running a skill on a file containing personal data, remove fields the task doesn't need, such as names or full card numbers.
- Never put personal data in report examples. Use roles and anonymised values.

## 4. Running the skills (S1, S2, S3)

- Run skills only in the approved Claude or Copilot environment, on files stored in the engagement folder.
- Every skill output is a **draft** (`record_status` = Draft (AI)). A consultant reviews it and changes the record status to Reviewed before it is used or shared.
- Nothing produced by a skill goes to the client without that review.
- Every finding in the report must trace to evidence (`evidence_ids`). S3 flags any claim without it.

## 5. Storage and retention

| Item | During the engagement | At finalisation |
| --- | --- | --- |
| Recordings and transcripts | Teams / engagement folder | Kept with retained records under Deloitte policy, or deleted if the client's consent required it |
| C2 engagement workbook | Shared online workbook | Final version moved to iManage |
| Client documents and sample data | Engagement folder | Moved to iManage or deleted, per the engagement letter |
| Final report and playback deck | Engagement folder | iManage (final deliverable) |

## 6. Audit clients

If the client or a related entity is a Deloitte audit client, independence clearance must be confirmed before the engagement starts and again before the report is issued (D2).

## Checklist for each engagement

- [ ] Approved-tool list confirmed against current policy
- [ ] Recording consent obtained and recorded
- [ ] Secure share link issued to the client
- [ ] Personal-data files flagged in C2
- [ ] All skill outputs reviewed before use
- [ ] Final records moved to iManage and working copies cleared
