import json
import streamlit as st

SAVE_FILE = "books.json"

if "books" not in st.session_state:
    st.session_state["books"] = {}

st.title("Håvard's Book Tracker")

st.write("Use the sidebar to add or view your books.")

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Save books to file"):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state["books"], f, ensure_ascii=False, indent=2)
        st.success(f"Saved {len(st.session_state['books'])} books to `{SAVE_FILE}`.")

with col2:
    if st.button("📂 Load books from file"):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            # JSON keys are always strings — convert back to int
            st.session_state["books"] = {int(k): v for k, v in loaded.items()}
            st.success(f"Loaded {len(st.session_state['books'])} books from `{SAVE_FILE}`.")
        except FileNotFoundError:
            st.error(f"`{SAVE_FILE}` not found. Save first.")
