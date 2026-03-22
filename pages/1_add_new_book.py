import datetime
import streamlit as st

if "books" not in st.session_state:
    st.session_state["books"] = {}

st.title("Add New Book")

title = st.text_input("Title *")
author = st.text_input("Author")
year = st.number_input("Year published", min_value=1, max_value=2026, value=2024, step=1)
pages = st.number_input("Number of pages", min_value=1, max_value=10000, value=300, step=1)

genre_options = ["Fiction", "Non-fiction", "Sci-Fi", "Fantasy", "Biography", "Custom..."]
genre_select = st.selectbox("Genre", genre_options)
if genre_select == "Custom...":
    genre = st.text_input("Enter genre")
else:
    genre = genre_select

format_ = st.selectbox("Format", ["Physical", "E-book", "Audiobook"])
language = st.text_input("Language", value="English")
goodreads_rating = st.number_input("Goodreads rating", min_value=0.0, max_value=5.0, value=0.0, step=0.01, format="%.2f")
goodreads_link = st.text_input("Goodreads link")
summary = st.text_area("Summary")
status = st.selectbox("Status", ["Want to read", "Read"])
series = st.checkbox("Part of a series")
own_it = st.checkbox("Own it")

if status == "Read":
    date_finished = st.date_input("Date finished", value=datetime.date.today())
    rating = st.slider("Rating", min_value=1, max_value=10, value=5)
    notes = st.text_area("Notes / thoughts")
else:
    date_finished = None
    rating = None
    notes = ""

if st.button("Add Book"):
    if not title.strip():
        st.error("Title is required.")
    elif genre_select == "Custom..." and not genre.strip():
        st.error("Please enter a custom genre.")
    else:
        new_id = len(st.session_state["books"])
        st.session_state["books"][new_id] = {
            "title": title.strip(),
            "author": author.strip(),
            "year": int(year),
            "pages": int(pages),
            "genre": genre.strip() if genre_select == "Custom..." else genre,
            "format": format_,
            "language": language.strip(),
            "goodreads_rating": goodreads_rating if goodreads_rating > 0 else None,
            "goodreads_link": goodreads_link.strip() or None,
            "summary": summary.strip(),
            "status": status,
            "series": series,
            "own_it": own_it,
            "date_finished": str(date_finished) if date_finished else None,
            "rating": rating,
            "notes": notes.strip(),
        }
        st.success(f'"{title.strip()}" added to your collection!')
