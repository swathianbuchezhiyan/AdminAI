import streamlit as st
from database.database import (
    initialize_database,
    initialize_default_officers
)

# Initialize database and default officers
initialize_database()
initialize_default_officers()

st.set_page_config(
    page_title="AdminAI",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ AdminAI")
st.subheader("AI Governance Assistant")

st.markdown("""
### Welcome to AdminAI

AdminAI is an AI-powered governance platform that helps government officers:

- 📋 Manage citizen complaints
- 🤖 Categorize complaints using Artificial Intelligence
- ⚡ Identify high-priority issues
- 📊 View analytics and reports
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info("📝 Submit Complaint")

with col2:
    st.info("📊 Officer Dashboard")

col3, col4 = st.columns(2)

with col3:
    st.info("🤖 AI Analytics")

with col4:
    st.info("🔐 Officer Login")

st.divider()

st.caption("© 2026 AdminAI | AI Governance Assistant")