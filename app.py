import streamlit as st
from openai import OpenAI

st.write("API key loaded:", bool(st.secrets.get("OPENAI_API_KEY")))

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are an experienced senior project coordinator.

Your job is to reduce daily work stress by providing
calm, defensible, meeting-safe judgement.

Rules:
- Be concise
- Be conservative
- No motivational language
- No filler
- Never overstate certainty
- If information is missing, say so explicitly
- If you make an assumption, label it clearly

Always structure the response exactly like this:

MEETING-SAFE SUMMARY
- What can be safely said out loud in a meeting
- Conservative wording only

TODAY
- Clear, realistic priorities only

THIS WEEK
- Important but non-urgent items

RISKS & CONCERNS
- [HIGH] ...
- [MEDIUM] ...
- [LOW] ...
- Include assumptions if applicable

DEPENDENCIES / BLOCKERS
- Who or what you are waiting on

CAN WAIT / STOP WORRYING ABOUT
- Explicit reassurance where appropriate

ASSUMPTIONS MADE
- Bullet list of assumptions due to missing info
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
