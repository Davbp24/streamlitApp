import streamlit as st
import pandas as pd
import plotly.express as px
from data_service import fetch_data
import random

books = {}
book_list = ["the-hunger-games","the-martian", "dune", "project-hail-mary", "enders-game", "cress", "the-stand"]


if "selected_books" not in st.session_state:

    st.session_state.selected_books = random.sample(book_list, 3)

selected_books = st.session_state.selected_books

for random_book in selected_books:
    book = fetch_data(random_book)
    books[book["title"]] = book


st.title("Book Information Site")
st.header("Three Random Books")

st.divider()

st.header("Overview")
st.subheader("What this project is:")
st.write("This application is going to display and compare data of random books selected from an API.")
st.divider()
st.header("Data Display")
st.write("This part of the application allows for different charts to be displayed based on ranking, awards won, and the year released for the particular random set of books that you received.")

data_dictionary = {}

for book, values in books.items():
    data_dictionary[book] = {"title": values["title"], "rating": values["score"]["value"], "awards": len(values["awards"]), "year": values["year"]}


books_df = pd.DataFrame.from_dict(data_dictionary, orient="index")

st.subheader("Charts")
choice_widget = st.radio("Choose a chart to display different data:", ["Book Ratings", "Awards Won", "Publication Year"])

if choice_widget == "Book Ratings":
    figure = px.bar(books_df, x="title", y="rating", title="Book Ratings - out of 10", labels={"title": "Book Title", "rating": "Rating"})

    st.plotly_chart(figure)
elif choice_widget == "Awards Won":
    figure = px.pie(books_df, names="title", values="awards", title="Awards Won By Book", labels={"title": "Book Title", "awards": "Awards Won"})
    st.plotly_chart(figure)
elif choice_widget == "Publication Year":
    figure = px.scatter(books_df, x="title", y="year", title="Publication Year", labels={"title": "Book Title", "year": "Year"})
    st.plotly_chart(figure)

