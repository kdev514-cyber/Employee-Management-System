import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

st.title("Supabase Connection Test")

response = (
    supabase
    .table("employees")
    .select("*")
    .execute()
)

st.success("Supabase connection successful!")

st.write(response.data)
