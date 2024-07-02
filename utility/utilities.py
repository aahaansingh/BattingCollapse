import streamlit as st
from supabase import create_client, Client
import pandas as pd

@st.cache_resource
def init_connection():
    url = st.secrets["connections"]["supabase"]["SUPABASE_URL"]
    key = st.secrets["connections"]["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

@st.cache_data(ttl=600)
def run_query(_connection: Client, function: str, start_date: str, end_date: str):
    return _connection.rpc(function, {"start_date":start_date, "end_date":end_date}).execute()