# Project Clarity AI — Test Suite

## How to run
- For each test: paste input → click **Create Daily Brief** → record results.
- Save key outputs (copy/paste) into `/test_runs/YYYY-MM-DD/` if needed.
- Mark Pass/Fail and add comments.

## Legend
- **Pass criteria** = must be true to pass.
- **Fail signals** = common failure modes.

---

## Core Behaviour & Trust Tests

| ID | Test name | Test input | Pass criteria | Actual result | Pass/Fail | Comments / Actions |
|---:|---|---|---|---|---|---|
| T01 | Baseline creation | Baseline project state… | Stable structured output; no invented urgency; Memory shows ON |  |  |  |
| T02 | Meeting-safe tone | Real email (redacted) | Summary is factual/defensible; no absolutes |  |  |  |
| T03 | Decision support appears | Same email | Has Decision + Options + Recommended posture |  |  |  |
| T04 | Risk hygiene | Same email | Risks are “could go wrong”, not activities |  |  |  |
| T05 | Evidence quoting | Same email | 1–3 verbatim quotes, no hallucinated quotes |  |  |  |
| T06 | Stasis lock | No new updates… | No new actions/assumptions; TODAY can be “No action required” |  |  |  |
| T07 | No escalation without timing | Still awaiting… | No timeline-impact claim unless deadline exists |  |  |  |
| T08 | Contradiction reconciliation | Confirmed + evidence pending | Output resolves contradiction cleanly |  |  |  |
| T09 | Noise resistance | Long chain + fluff | Ignores signatures; focuses on signal |  |  |  |
| T10 | Bad input tolerance | Messy bullets | Still structured; flags missing info calmly |  |  |  |

---

## Memory & Persistence Tests (Streamlit Cloud)

| ID | Test name | Test input | Pass criteria | Actual result | Pass/Fail | Comments / Actions |
|---:|---|---|---|---|---|---|
| M01 | Memory writes | Any prompt | Memory shows ON; yesterday.txt viewable |  |  |  |
| M02 | Memory reads next run | Delta update | Output reflects continuity & changes |  |  |  |
| M03 | Survives refresh | Refresh browser | Memory remains ON |  |  |  |
| M04 | Survives redeploy | Push trivial commit | Memory remains ON |  |  |  |

---

## Test Run Log

| Date | Tester | Run type | Notes | Link/Location |
|---|---|---|---|---|
|  |  | Alpha / Private Beta |  |  |
