# SmartDine Streamlit Frontend Placeholder
import sys

try:
    import streamlit as st
except ModuleNotFoundError:
    print(
        "\n========================================================================\n"
        "ERROR: Streamlit is not installed in the current Python environment.\n"
        "Please run this file using the virtual environment's Streamlit:\n"
        "  .\\.venv\\Scripts\\streamlit run frontend/app.py\n"
        "Or activate the virtual environment first:\n"
        "  .\\.venv\\Scripts\\activate\n"
        "========================================================================",
        file=sys.stderr
    )
    sys.exit(1)

import requests

st.set_page_config(
    page_title="SmartDine 🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

FASTAPI_URL = "http://localhost:8000/api/v1"

st.title("SmartDine 🍽️")
st.subheader("AI-Powered Restaurant Recommendations")
st.write("UI initialization is in progress. API connection is set to:", FASTAPI_URL)
