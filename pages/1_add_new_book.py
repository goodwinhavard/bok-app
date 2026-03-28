import datetime
import streamlit as st

if "books" not in st.session_state:
    st.session_state["books"] = {}

st.title("Add New Book")

books = st.session_state["books"].values()

# --- Author ---
existing_authors = sorted({b["author"] for b in books if b.get("author")})
if existing_authors:
    author_select = st.selectbox("Author", existing_authors + ["New author..."])
    if author_select == "New author...":
        author = st.text_input("Enter author name")
    else:
        author = author_select
else:
    author = st.text_input("Author")

title = st.text_input("Title *")
year = st.number_input("Year published", min_value=1, max_value=2026, value=2024, step=1)
pages = st.number_input("Number of pages", min_value=1, max_value=10000, value=300, step=1)

# --- Genre ---
existing_genres = sorted({b["genre"] for b in books if b.get("genre")})
if existing_genres:
    genre_select = st.selectbox("Genre", existing_genres + ["New genre..."])
    if genre_select == "New genre...":
        genre = st.text_input("Enter genre")
    else:
        genre = genre_select
else:
    genre_select = None
    genre = st.text_input("Genre")

format_ = st.selectbox("Format", ["Physical", "E-book", "Audiobook"])

# --- Language ---
existing_languages = sorted({b["language"] for b in books if b.get("language")})
if not existing_languages:
    existing_languages = ["English"]
language_select = st.selectbox("Language", existing_languages + ["New language..."])
if language_select == "New language...":
    language = st.text_input("Enter language")
else:
    language = language_select

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
    elif genre_select == "New genre..." and not genre.strip():
        st.error("Please enter a genre.")
    elif language_select == "New language..." and not language.strip():
        st.error("Please enter a language.")
    elif existing_authors and author_select == "New author..." and not author.strip():
        st.error("Please enter an author name.")
    else:
        new_id = len(st.session_state["books"])
        st.session_state["books"][new_id] = {
            "title": title.strip(),
            "author": author.strip(),
            "year": int(year),
            "pages": int(pages),
            "genre": genre.strip(),
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
