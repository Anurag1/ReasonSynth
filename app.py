"""
ReasonSynth — Where intent becomes provable code.
App entry point: Streamlit UI for the symbolic program synthesizer.
"""

import streamlit as st
from synthesizer import ReasonSynth

st.set_page_config(page_title="ReasonSynth", layout="centered")
st.title("🧠 ReasonSynth — Where intent becomes provable code.")
st.markdown("_Turn natural language into verified, provable code._")

rs = ReasonSynth()

spec_input = st.text_area(
    "Describe the function you want:",
    "Write a function that returns the square of a number greater than 0."
)

if st.button("Synthesize & Verify"):
    res = rs.run(spec_input)
    st.subheader("📜 Parsed Specification")
    st.json(res["spec"])
    st.subheader("🧩 Synthesized Code")
    st.code(res["code"], language="python")
    st.subheader("🔎 Proof Result")
    if "✅" in res["proof"]:
        st.success(res["proof"])
    else:
        st.error(res["proof"])
