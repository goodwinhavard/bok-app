import streamlit as st
import pandas as pd

st.title("Book Stats")

if "books" not in st.session_state:
    st.session_state["books"] = {}

books = list(st.session_state["books"].values())
read_books = [b for b in books if b.get("status") == "Read"]

if not books:
    st.info("No books added yet. Use the **Add New Book** page to get started.")
    st.stop()

# --- Top-level metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total books", len(books))
col2.metric("Books read", len(read_books))
col3.metric("Want to read", len(books) - len(read_books))
total_pages = sum(b.get("pages") or 0 for b in read_books)
col4.metric("Pages read", f"{total_pages:,}")

st.divider()

# --- Books read per year ---
st.subheader("Books read per year")
years = [b["date_finished"][:4] for b in read_books if b.get("date_finished")]
if years:
    year_counts = pd.Series(years).value_counts().sort_index()
    year_df = year_counts.reset_index()
    year_df.columns = ["Year", "Books"]
    st.bar_chart(year_df.set_index("Year"))
else:
    st.info("No finished books with a date yet.")

st.divider()

# --- Pages read per year ---
st.subheader("Pages read per year")
pages_by_year = {}
for b in read_books:
    if b.get("date_finished") and b.get("pages"):
        y = b["date_finished"][:4]
        pages_by_year[y] = pages_by_year.get(y, 0) + b["pages"]
if pages_by_year:
    pages_df = pd.DataFrame(sorted(pages_by_year.items()), columns=["Year", "Pages"])
    st.bar_chart(pages_df.set_index("Year"))
else:
    st.info("No finished books with pages and a date yet.")

st.divider()

# --- Genre breakdown ---
st.subheader("Genre breakdown")
genres = [b["genre"] for b in books if b.get("genre")]
if genres:
    genre_df = pd.Series(genres).value_counts().reset_index()
    genre_df.columns = ["Genre", "Count"]
    st.bar_chart(genre_df.set_index("Genre"))

st.divider()

# --- Format breakdown ---
st.subheader("Format breakdown")
formats = [b["format"] for b in books if b.get("format")]
if formats:
    fmt_df = pd.Series(formats).value_counts().reset_index()
    fmt_df.columns = ["Format", "Count"]
    st.bar_chart(fmt_df.set_index("Format"))

st.divider()

# --- Average rating per year ---
st.subheader("Average personal rating per year")
ratings_by_year = {}
for b in read_books:
    if b.get("date_finished") and b.get("rating"):
        y = b["date_finished"][:4]
        ratings_by_year.setdefault(y, []).append(b["rating"])
if ratings_by_year:
    avg_df = pd.DataFrame(
        [(y, sum(r) / len(r)) for y, r in sorted(ratings_by_year.items())],
        columns=["Year", "Avg rating"],
    )
    st.line_chart(avg_df.set_index("Year"))
else:
    st.info("No rated books yet.")
