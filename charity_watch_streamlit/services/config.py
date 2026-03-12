import os
import streamlit as st
from dotenv import load_dotenv

#loading environment variables
load_dotenv()

def get_secret(key):
    #gets secret key using after loading secret environment variables
    val = os.getenv(key)
    #if there is a secret key then we return it
    if val:
        return val
    #else we use st.secrets to return the key (for streamlit cloud)
    try:
        return st.secrets[key]
    except Exception:
        return None