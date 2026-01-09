import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are an experienced senior project coordinator.

Your job is to reduce daily work stress by turning messy information
into calm, prioritised clarity.

Rules:
- Be concise
- Be decisive
- No motivational language
- No filler
- If something is unclear, flag it as a risk
- If something can wait, say so explicitly

Always structure the response exactly like this:

TODAY
- Bullet points

THIS WEEK
- Bullet points

RISKS & CONCERNS
- Bullet points

DEPENDENCIES / BLOCKERS
- Bullet points

CAN WAIT / STOP WORRYING ABOUT
- Bullet points
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
