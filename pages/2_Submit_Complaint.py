import streamlit as st
import os

from database.database import save_complaint

from models.predict import (
    predict_complaint,
    predict_priority,
    generate_summary
)


st.title("📝 Submit Complaint")

st.subheader("Citizen Complaint Form")


# ---------------------------------------
# Citizen Details
# ---------------------------------------

citizen_name = st.text_input(
    "👤 Full Name"
)

mobile_number = st.text_input(
    "📱 Mobile Number"
)

email = st.text_input(
    "📧 Email (Optional)"
)


# ---------------------------------------
# Location
# ---------------------------------------

district = st.selectbox(
    "📍 Select District",
    [
        "Chennai",
        "Coimbatore",
        "Madurai",
        "Trichy",
        "Thanjavur",
        "Mayiladuthurai",
        "Sirkali",
        "Salem",
        "Tirunelveli",
        "Other"
    ]
)


# ---------------------------------------
# Complaint Details
# ---------------------------------------

complaint_title = st.text_input(
    "📝 Complaint Title"
)

complaint_description = st.text_area(
    "📄 Complaint Description (Tamil / English)",
    height=150
)


# ---------------------------------------
# Image Upload
# ---------------------------------------

uploaded_file = st.file_uploader(
    "📷 Upload Complaint Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


image_path = None


if uploaded_file is not None:

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    image_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    st.success(
        "📷 Image uploaded successfully"
    )


# ---------------------------------------
# Tamil → English
# ---------------------------------------

def translate_tamil(text):

    tamil_complaints = {

        "எங்கள் பகுதியில் சாலை மிகவும் மோசமாக உள்ளது":
            "The road in our area is very badly damaged",

        "சாலை மிகவும் மோசமாக உள்ளது":
            "The road is very badly damaged",

        "சாலையில் பள்ளங்கள் உள்ளன":
            "There are potholes on the road",

        "சாலை சேதமடைந்துள்ளது":
            "The road is damaged",

        "சாலை பழுதடைந்துள்ளது":
            "The road is damaged",

        "குப்பைகள் அகற்றப்படவில்லை":
            "Garbage has not been removed",

        "எங்கள் பகுதியில் குப்பைகள் உள்ளன":
            "There is garbage in our area",

        "தண்ணீர் வரவில்லை":
            "There is no water supply",

        "குடிநீர் பிரச்சனை உள்ளது":
            "There is a drinking water problem",

        "மின்சாரம் இல்லை":
            "There is no electricity",

        "மின்சார பிரச்சனை உள்ளது":
            "There is an electricity problem",

        "மருத்துவமனை அருகில் சுகாதார பிரச்சனை":
            "There is a sanitation problem near the hospital"
    }

    cleaned_text = text.strip()

    if cleaned_text in tamil_complaints:

        return tamil_complaints[cleaned_text]

    return text


# ---------------------------------------
# Initialize Session State
# ---------------------------------------

if "complaint_submitted" not in st.session_state:

    st.session_state.complaint_submitted = False


# ---------------------------------------
# Submit Complaint
# ---------------------------------------

if st.button("🚀 Submit Complaint"):

    if (
        citizen_name.strip() == ""
        or mobile_number.strip() == ""
        or complaint_title.strip() == ""
        or complaint_description.strip() == ""
    ):

        st.warning(
            "⚠️ Please fill all required fields"
        )

    else:

        # --------------------------------
        # Translate Tamil Complaint
        # --------------------------------

        english_complaint = translate_tamil(
            complaint_description
        )

        if english_complaint != complaint_description:

            st.info(
                f"🌐 Translated Complaint: {english_complaint}"
            )


        # --------------------------------
        # AI Prediction
        # --------------------------------

        ai_category, confidence = predict_complaint(
            english_complaint
        )

        department = ai_category

        priority = predict_priority(
            english_complaint
        )


        # --------------------------------
        # AI Complaint Summary
        # --------------------------------

        complaint_summary = generate_summary(
            english_complaint
        )


        # --------------------------------
        # Save Complaint
        # --------------------------------

        complaint_id = save_complaint(
            citizen_name,
            mobile_number,
            email,
            district,
            ai_category,
            department,
            confidence,
            priority,
            complaint_title,
            complaint_description,
            image_path
        )


        # --------------------------------
        # Store Result
        # --------------------------------

        st.session_state.complaint_submitted = True

        st.session_state.ai_category = ai_category
        st.session_state.department = department
        st.session_state.confidence = confidence
        st.session_state.priority = priority
        st.session_state.complaint_summary = complaint_summary
        st.session_state.complaint_id = complaint_id


# ---------------------------------------
# AI Result Display
# ---------------------------------------

if st.session_state.complaint_submitted:

    st.subheader(
        "🤖 AI Analysis Result"
    )

    st.success(
        f"🏢 Department: {st.session_state.department}"
    )

    st.info(
        f"📂 AI Category: {st.session_state.ai_category}"
    )

    st.info(
        f"📊 Confidence Score: {st.session_state.confidence}%"
    )

    st.info(
        f"📝 AI Complaint Summary: {st.session_state.complaint_summary}"
    )


    priority = st.session_state.priority


    if priority == "High":

        st.error(
            f"🚨 Priority: {priority}"
        )

    elif priority == "Medium":

        st.warning(
            f"⚠️ Priority: {priority}"
        )

    else:

        st.success(
            f"✅ Priority: {priority}"
        )


    st.divider()

    st.success(
        "✅ Complaint Submitted Successfully!"
    )

    st.info(
        f"🆔 Complaint ID: {st.session_state.complaint_id}"
    )