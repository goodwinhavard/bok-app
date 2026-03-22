import streamlit as st

if "books" not in st.session_state:
    st.session_state["books"] = {}

st.title("View Books")

books = st.session_state["books"]

if not books:
    st.info("No books added yet. Use the **Add New Book** page to get started.")
else:
    st.subheader(f"Your books ({len(books)})")
    for book in books.values():
        with st.expander(f"{book['title']} — {book['author'] or 'Unknown author'}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Year:** {book['year'] or '—'}")
                st.write(f"**Genre:** {book['genre']}")
            with col2:
                st.write(f"**Status:** {book['status']}")
                if book["status"] == "Read":
                    st.write(f"**Rating:** {'★' * book['rating']}{'☆' * (5 - book['rating'])}")
            if book["notes"]:
                st.write(f"**Notes:** {book['notes']}")
