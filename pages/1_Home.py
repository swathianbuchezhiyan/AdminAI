import streamlit as st

from database.database import get_all_complaints


st.title("🏛️ AdminAI")

st.subheader("AI Governance Assistant")


st.markdown("---")


st.write("""
Welcome to **AdminAI**, an AI-powered governance platform designed to help government officers efficiently manage citizen complaints.

### Our Objectives

- 📋 Digital Complaint Management
- 🤖 AI Complaint Classification
- ⚡ Priority Detection
- 📊 Analytics Dashboard
- 🏛️ Better Public Service
""")


st.markdown("---")



# ---------------------------------------
# Load Complaint Data
# ---------------------------------------

complaints = get_all_complaints()



total_complaints = len(complaints)


resolved = 0

pending = 0

high_priority = 0



# ---------------------------------------
# Calculate Statistics
# ---------------------------------------

for complaint in complaints:


    status = complaint[10]


    if status == "Resolved":

        resolved += 1


    elif status == "Pending":

        pending += 1



    # AI Priority Check

    description = str(
        complaint[8]
    ).lower()



    high_keywords = [

        "fire",
        "accident",
        "emergency",
        "crime",
        "danger",
        "water shortage",
        "no electricity"

    ]



    for word in high_keywords:

        if word in description:

            high_priority += 1

            break




# ---------------------------------------
# Dashboard Cards
# ---------------------------------------

col1, col2, col3, col4 = st.columns(4)



with col1:

    st.metric(
        "📋 Complaints",
        total_complaints
    )



with col2:

    st.metric(
        "✅ Resolved",
        resolved
    )



with col3:

    st.metric(
        "⏳ Pending",
        pending
    )



with col4:

    st.metric(
        "🚨 High Priority",
        high_priority
    )



st.markdown("---")



st.success(
    "🚀 Welcome to AdminAI Version 1.0"
)