import streamlit as st
from openai import OpenAI

st.write("API key loaded:", bool(st.secrets.get("OPENAI_API_KEY")))

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """You are an experienced senior project coordinator.

Your role is to reduce daily work stress by providing calm,
conservative, and meeting-safe judgement.

You help the user understand what matters, what can wait,
and how to speak about issues professionally.

RULES
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

OUTPUT FORMAT  
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
"""

st.set_page_config(page_title="Project Clarity AI", layout="wide")

st.title("🧠 Project Clarity AI")
st.caption("Paste your work chaos. Get a calm plan.")

user_input = st.text_area(
    "Paste emails, notes, messages, meeting minutes — anything:",
    height=300
)

if st.button("Create Daily Brief"):
    if not user_input.strip():
        st.warning("Paste something first.")
    else:
        with st.spinner("Thinking like a calm project coordinator..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.2
            )

        output = response.choices[0].message.content

        st.markdown("---")
        st.markdown(output)
