
import streamlit as st
import pandas as pd
import requests
import random

@st.cache_data(ttl=3600)
def fetch_data(random_book):

    API_URL = f"https://openbookrank.com/api/v1/books/{random_book}.json"
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    return response.json()


