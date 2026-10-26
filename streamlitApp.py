import streamlit as st
import pandas as pd
import plotly.express as px
from data_service import fetch_data
import random

#initialization of book list that will be used within the API_URL in data_service.py
books = {}
book_list = ["the-hunger-games","the-martian", "dune", "project-hail-mary", "enders-game", "cress", "the-stand"]


if "selected_books" not in st.session_state:

    st.session_state.selected_books = random.sample(book_list, 3)

selected_books = st.session_state.selected_books

for random_book in selected_books:
    book = fetch_data(random_book)
    books[book["title"]] = book

# the following code is streamlit code to allow for easy user understanding and segmentation of information.
st.title("Book Information Site")
st.header("Three Random Books")

st.divider()

st.header("Overview")
st.subheader("What this App is for:")
st.write("This application is going to display and compare data of random books selected from an API.")

st.header("Data Display")
st.write("This part of the application allows for different charts to be displayed based on ranking, awards won, and the year released for the particular random set of books that is received.")


#this code is setting up a clean data set for pandas to be able to utilize as a dataframe
data_dictionary = {}

for book, values in books.items():
    data_dictionary[book] = {"title": values["title"], "rating": values["score"]["value"], "awards": len(values["awards"]), "year": values["year"]}

#setting up dataframe
books_df = pd.DataFrame.from_dict(data_dictionary, orient="index")

#code for the charts section, which utilizes a radio widget.
st.subheader("Charts")
choice_widget = st.radio("Choose a chart to display different data:", ["Book Ratings", "Awards Won", "Publication Year"])

#depending on the user's choice, it will display that specific chart, where the chart is created at each aspect for figure.

#to improve efficieny, instantiate all three charts
figure1 = px.bar(books_df, x="title", y="rating", title="Book Ratings - out of 10", labels={"title": "Book Title", "rating": "Rating"})
figure2 = px.pie(books_df, names="title", values="awards", title="Awards Won By Book", labels={"title": "Book Title", "awards": "Awards Won"})
figure3 = px.scatter(books_df, x="title", y="year", title="Publication Year", labels={"title": "Book Title", "year": "Year"})

#depending on the choice, the radio widget will display the respective chart, where the charts were previously created as figure 1-3.
if choice_widget == "Book Ratings":
    st.plotly_chart(figure1)
elif choice_widget == "Awards Won":
    st.plotly_chart(figure2)
elif choice_widget == "Publication Year":
    st.plotly_chart(figure3)

