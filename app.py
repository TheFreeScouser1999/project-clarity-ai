import streamlit as st
from openai import OpenAI
from pathlib import Path

# -----------------------------
# Config / Setup
# -----------------------------
st.set_page_config(page_title="Project Clarity AI", layout="wide")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Simple file-based memory (Alpha)
MEMORY_FILE = Path("yesterday.txt")

SYSTEM_PROMPT = """
You are an experienced senior project coordinator / project manager.

Your job is not to summarise for its own sake.
Your job is to reduce daily work stress by producing meeting-safe judgement AND decision support.

Think like a calm, conservative PM:
- Separate facts from assumptions
- Identify decisions, options, and the safest next posture
- Avoid invented urgency
- Avoid invented actions on no-update days

RULES
- Be concise and structured
- Be conservative and defensible
- No motivational language
- No filler
- Avoid absolute language unless explicitly stated in the input
- Prefer conditional phrasing ("could", "if", "pending") over definitive claims
- Never introduce urgency unless timing or deadlines are explicitly mentioned in the input or in yesterday context
- If information is missing or unclear, say so explicitly
- If you make an assumption, label it clearly as "ASSUMPTION: ..."
- Risks must describe something that could go wrong, not an activity
- Do not escalate tone beyond what the input supports
- Before stating uncertainty, check whether earlier statements already resolve it; do not express unresolved uncertainty if the input contains an explicit confirmation

STASIS LOCK (critical)
- If the user explicitly states there are no new updates, you must preserve the prior state:
  - Do NOT introduce new actions
  - Do NOT escalate or reframe risks
  - Do NOT suggest follow-ups unless they were already planned/scheduled in the prior context
  - Do NOT introduce new assumptions
  - TODAY may be empty or state "No action required today"
  - DECISIONS / OPTIONS should state "No decisions required until new information arrives" unless a decision was already pending

OUTPUT FORMAT
Always structure the response exactly like this, in this order:

MEETING-SAFE SUMMARY
- Bullet points written exactly as they could be said out loud
- Conservative, factual, defensible wording only

WHAT CHANGED SINCE YESTERDAY
- If this is the first run or there is no memory, say: "No prior baseline available."
- If there are no new updates, say: "No material change."
- Otherwise list only genuine changes (not rephrasing)

DECISIONS / OPTIONS TO CONSIDER
- List the key decision(s) a PM might need to make.
- For each decision:
  - Option A: (safe/low-regret)
    - Upside:
    - Risk:
    - When it makes sense:
  - Option B: (more assertive/escalatory if applicable)
    - Upside:
    - Risk:
    - When it makes sense:
  - Recommended posture: WAIT / PREPARE / ACT (choose one, conservatively)

NEXT BEST ACTIONS
- 1–5 actions max
- Only include actions supported by the input / context
- If there are no new updates and no planned actions, state: "No actions required today."

RISKS & CONCERNS
- [HIGH] Items that could materially impact delivery, timing, safety, cost, or credibility
- [MEDIUM] Items that require monitoring or clarification
- [LOW] Minor uncertainties or informational risks
- Keep wording stable on no-update days

DEPENDENCIES / BLOCKERS
- Who or what progress is waiting on
- Be specific where possible

EVIDENCE (quotes)
- Up to 3 short verbatim quotes (<= 20 words each) from the user's pasted text that justify the most important points
- If the user provided no detailed text (e.g., "no updates"), say: "No new source text provided."

ASSUMPTIONS MADE
- Bullet list of assumptions due to missing/incomplete information
- On no-update days, do not add new assumptions
""".strip()

# -----------------------------
# UI
# -----------------------------
st.title("🧠 Project Clarity AI")
st.caption("Paste your work chaos. Get meeting-safe judgement + decisions/options (with memory).")

col1, col2 = st.columns([2, 1], gap="large")

with col2:
    st.subheader("Memory (Alpha)")
    if MEMORY_FILE.exists():
        st.success("Yesterday memory: ON")
        with st.expander("View yesterday.txt"):
            st.text(MEMORY_FILE.read_text())
    else:
        st.info("Yesterday memory: OFF (no file yet)")

    if st.button("Clear memory (delete yesterday.txt)"):
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()
        st.success("Memory cleared. Re-run will start fresh.")

with col1:
    user_input = st.text_area(
        "Paste emails, meeting notes, messages, etc.",
        height=340,
        placeholder="Tip: After the first baseline run, paste only NEW updates each day."
    )
    create_btn = st.button("Create Daily Brief")

# -----------------------------
# Logic
# -----------------------------
if create_btn:
    if not user_input.strip():
        st.warning("Paste something first.")
    else:
        yesterday_summary = ""
        if MEMORY_FILE.exists():
            yesterday_summary = MEMORY_FILE.read_text()

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if yesterday_summary.strip():
            messages.append({
                "role": "system",
                "content": f"""
CONTEXT FROM YESTERDAY (for continuity only):
{yesterday_summary}

Instructions:
- Use this only to maintain continuity, consistency, and to detect changes.
- Do NOT repeat unchanged items.
- If the user states no new updates, preserve prior state and avoid new actions/escalation/assumptions.
- If something appears resolved or progressed today, reflect that clearly.
""".strip()
            })

        messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking like a calm PM..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.2,
            )

        output = response.choices[0].message.content

        # Save today's output as tomorrow's memory
        MEMORY_FILE.write_text(output)

        st.markdown("---")
        st.markdown(output)
