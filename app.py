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
You are an experienced senior project coordinator.

Your role is to reduce daily work stress by providing calm,
conservative, and meeting-safe judgement.

You help the user understand what matters, what can wait,
and how to speak about issues professionally.

RULES
- If the user explicitly states there are no new updates, you must preserve the prior state exactly:
  - Do NOT introduce new actions
  - Do NOT escalate or reframe risks
  - Do NOT suggest follow-ups unless they were already scheduled
  - Do NOT introduce new assumptions
  - It is acceptable for TODAY to be empty or state "No action required today"

- Be concise and structured
- Be conservative and defensible
- No motivational language
- No filler
- Avoid absolute language unless explicitly stated in the input
- Prefer conditional phrasing ("could", "if", "pending") over definitive claims
- Never introduce urgency unless timing or deadlines are explicitly mentioned
- If information is missing or unclear, say so explicitly
- If you make an assumption, label it clearly
- Risks must describe something that could go wrong, not an activity
- Do not escalate tone beyond what the input supports
- Before stating uncertainty, check whether earlier statements already resolve it; do not express unresolved uncertainty if the input contains an explicit confirmation
- If the user explicitly states there are no new updates, do not introduce new actions, escalation, or assumptions; maintain prior state
- When there are no new updates, do not introduce new assumptions; only restate assumptions if they have changed

OUTPUT FORMAT
- If there are no new updates, TODAY may explicitly state "No action required today"

Always structure the response exactly like this, in this order:

MEETING-SAFE SUMMARY
- Bullet points written exactly as they could be said out loud
- Conservative, factual, defensible wording only

TODAY
- Clear, realistic priorities only
- Items that reasonably require attention today

THIS WEEK
- Important but non-urgent items
- Actions that depend on incoming information

RISKS & CONCERNS
- [HIGH] Items that could materially impact delivery, timing, or credibility
- [MEDIUM] Items that require monitoring or clarification
- [LOW] Informational risks or minor uncertainties
- Use conditional language where appropriate
- Explicitly state assumptions if relevant

DEPENDENCIES / BLOCKERS
- Who or what progress is waiting on
- Be specific where possible

CAN WAIT / DEFER
- Items that do not require action until new information is received
- Use cautious, professional reassurance
- Avoid blanket statements

ASSUMPTIONS MADE
- Bullet list of assumptions due to missing or incomplete information
""".strip()

# -----------------------------
# UI
# -----------------------------
st.title("🧠 Project Clarity AI")
st.caption("Paste your work chaos. Get a calm, meeting-safe daily brief.")

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
        height=320,
        placeholder="Paste your latest updates here…"
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

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        # Inject yesterday context for continuity (only if it exists)
        if yesterday_summary.strip():
            messages.append({
                "role": "system",
                "content": f"""
CONTEXT FROM YESTERDAY (for continuity only):
{yesterday_summary}

Instructions:
- Use this only to maintain consistency and reduce rework.
- Do NOT repeat unchanged items.
- Focus on updates, changes, newly surfaced risks, and what has progressed/resolved.
- If something appears resolved today, reflect that.
""".strip()
            })

        # Today's new input
        messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking like a calm project coordinator..."):
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
