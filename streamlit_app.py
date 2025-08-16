\
import streamlit as st
from typing import List
from app.engine import lookup_by_number, lookup_by_prefix, lookup_by_theme, top_k_for_query
from app.llm import generate_answer
from app.indexer import build_index

# Ensure index exists on first run
build_index(force=False)

st.set_page_config(page_title="Tirukural Chatbot", page_icon="📜")

st.title("📜 Tirukural Chatbot")

st.sidebar.header("Mode")
mode = st.sidebar.selectbox(
    "Choose interaction mode",
    [
        "Kural Lookup",
        "Theme-based Inspiration",
        "Conversational Advice",
        "Kural in Context",
    ],
)

def show_kural(k):
    with st.container():
        st.markdown(f"### Kural {k['kural_number']}")
        st.markdown(f"**Tamil**: {k['tamil']}")
        st.markdown(f"**Translation**: {k['translation']}")
        if k.get("explanation"):
            with st.expander("Meaning / Explanation"):
                st.write(k["explanation"])
        st.caption(f"Section: {k.get('section','')} | Chapter: {k.get('chapter','')}")

if mode == "Kural Lookup":
    st.subheader("Find a Kural by number, first words, or theme")

    lookup_type = st.radio("Lookup type", ["By Number", "By First Words", "By Theme"], horizontal=True)

    if lookup_type == "By Number":
        num = st.number_input("Kural number", min_value=1, max_value=1330, step=1, value=1)
        if st.button("Find Kural"):
            try:
                k = lookup_by_number(int(num))
                show_kural(k)
            except Exception as e:
                st.error(str(e))

    elif lookup_type == "By First Words":
        prefix = st.text_input("Enter the first few Tamil words (e.g., 'இன்னா')")
        if st.button("Search by prefix"):
            results = lookup_by_prefix(prefix, top_k=5)
            if not results:
                st.warning("No matches. Try fewer characters from the start.")
            for k in results:
                show_kural(k)

    else:  # By Theme
        theme = st.text_input("Theme keyword (e.g., 'friendship', 'self-control', 'justice')")
        if st.button("Search by theme"):
            results = lookup_by_theme(theme, top_k=5)
            if not results:
                st.warning("No matches for that theme.")
            for k in results:
                show_kural(k)

elif mode == "Theme-based Inspiration":
    st.subheader("Ask for a theme (e.g., 'self-control', 'friendship')")
    theme = st.text_input("Your theme")
    if st.button("Inspire me"):
        kurals = lookup_by_theme(theme, top_k=3)
        if not kurals:
            st.warning("No matches found.")
        else:
            for k in kurals:
                show_kural(k)
            st.markdown("---")
            st.markdown("### Answer")
            st.write(generate_answer(theme, kurals))

elif mode == "Conversational Advice":
    st.subheader("Tell me what you're going through")
    user_q = st.text_area("Example: 'I feel betrayed by a friend. What does Thirukkural say?'")
    if st.button("Get advice"):
        kurals = top_k_for_query(user_q, top_k=3)
        if not kurals:
            st.warning("No relevant kurals found.")
        else:
            for k in kurals:
                show_kural(k)
            st.markdown("---")
            st.markdown("### Answer")
            st.write(generate_answer(user_q, kurals))

else:  # Kural in Context
    st.subheader("Describe your modern-day scenario")
    scenario = st.text_area("Example: 'Should I forgive someone who cheated me?'")
    if st.button("Apply a Kural"):
        kurals = top_k_for_query(scenario, top_k=3)
        if not kurals:
            st.warning("No relevant kurals found.")
        else:
            for k in kurals:
                show_kural(k)
            st.markdown("---")
            st.markdown("### Answer")
            st.write(generate_answer(scenario, kurals))

st.markdown("---")
st.caption("Tip: Add an OpenAI API key in a `.env` file to unlock richer LLM responses.")
