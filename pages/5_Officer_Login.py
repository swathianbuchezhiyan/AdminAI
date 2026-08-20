import streamlit as st
import sys
from pathlib import Path

# ---------------------------------------
# Base Directory
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR)
)


# ---------------------------------------
# Database Functions
# ---------------------------------------

from database.database import (
    verify_officer,
    get_department_complaints,
    update_complaint_status
)

from models.predict import generate_summary


# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Officer Portal",
    page_icon="👮",
    layout="wide"
)


# ---------------------------------------
# Session Setup
# ---------------------------------------

if "officer" not in st.session_state:

    st.session_state.officer = None


# ---------------------------------------
# Update Success Message
# ---------------------------------------

if "update_success" in st.session_state:

    st.success(
        st.session_state["update_success"]
    )

    del st.session_state["update_success"]


# ---------------------------------------
# LOGIN
# ---------------------------------------

if st.session_state.officer is None:

    st.title(
        "👮 Officer Login"
    )

    st.subheader(
        "Department Officer Portal"
    )


    username = st.text_input(
        "👤 Username"
    )


    password = st.text_input(
        "🔒 Password",
        type="password"
    )


    if st.button("Login"):

        officer = verify_officer(
            username,
            password
        )


        if officer:

            st.session_state.officer = officer

            st.success(
                "Login Successful!"
            )

            st.rerun()


        else:

            st.error(
                "Invalid Username or Password"
            )


# ---------------------------------------
# OFFICER DASHBOARD
# ---------------------------------------

else:

    officer = st.session_state.officer


    st.title(
        "👮 Officer Dashboard"
    )


    st.subheader(
        f"Welcome, {officer['name']}!"
    )


    st.write(
        f"👤 **Officer:** {officer['name']}"
    )


    st.write(
        f"🏢 **Department:** {officer['department']}"
    )


    st.divider()


    # ---------------------------------------
    # Department Complaints
    # ---------------------------------------

    st.subheader(
        "📋 Department Complaints"
    )


    complaints = get_department_complaints(
        officer["department"]
    )


    if complaints:

        st.write(
            f"📊 **Total Complaints:** {len(complaints)}"
        )

        st.divider()


        # ---------------------------------------
        # Complaint List
        # ---------------------------------------

        for complaint in complaints:

            st.markdown(
                f"## 🆔 {complaint['complaint_id']} | "
                f"{complaint['complaint_title']}"
            )


            # -----------------------------------
            # Complaint Details
            # -----------------------------------

            with st.expander(
                "View Complaint Details"
            ):


                # -----------------------------------
                # Citizen Information
                # -----------------------------------

                st.subheader(
                    "👤 Citizen Information"
                )


                st.write(
                    f"**Name:** "
                    f"{complaint['full_name']}"
                )


                # -----------------------------------
                # Complaint Information
                # -----------------------------------

                st.subheader(
                    "📝 Complaint Information"
                )


                st.write(
                    f"**Title:** "
                    f"{complaint['complaint_title']}"
                )


                st.write(
                    f"**Description:** "
                    f"{complaint['complaint_description']}"
                )


                # -----------------------------------
                # AI Generated Summary
                # -----------------------------------

                st.subheader(
                    "🤖 AI Generated Summary"
                )


                summary = generate_summary(
                    complaint["complaint_description"]
                )


                st.info(
                    f"📝 {summary}"
                )


                # -----------------------------------
                # AI Analysis
                # -----------------------------------

                st.subheader(
                    "🤖 AI Analysis"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "AI Category",
                        complaint["ai_category"]
                    )


                with col2:

                    st.metric(
                        "Confidence",
                        f"{complaint['ai_confidence']}%"
                    )


                with col3:

                    st.metric(
                        "Priority",
                        complaint["priority"]
                    )


                st.divider()


                # -----------------------------------
                # Current Status
                # -----------------------------------

                st.write(
                    f"📌 **Current Status:** "
                    f"{complaint['status']}"
                )


                # -----------------------------------
                # Previous Officer Remark
                # -----------------------------------

                if complaint["officer_remark"]:

                    st.write(
                        f"💬 **Previous Remark:** "
                        f"{complaint['officer_remark']}"
                    )


                st.divider()


                # -----------------------------------
                # Update Complaint
                # -----------------------------------

                st.subheader(
                    "🔄 Update Complaint"
                )


                status_options = [
                    "Pending",
                    "In Progress",
                    "Resolved"
                ]


                current_status = complaint["status"]


                if current_status not in status_options:

                    current_status = "Pending"


                new_status = st.selectbox(

                    "📌 Status",

                    status_options,

                    index=status_options.index(
                        current_status
                    ),

                    key=f"status_{complaint['id']}"
                )


                officer_remark = st.text_area(

                    "👮 Officer Remark",

                    placeholder="Enter action taken...",

                    key=f"remark_{complaint['id']}"
                )


                # -----------------------------------
                # Update Button
                # -----------------------------------

                if st.button(

                    "Update Complaint",

                    key=f"update_{complaint['id']}"
                ):


                    update_complaint_status(

                        complaint["complaint_id"],

                        new_status,

                        officer_remark
                    )


                    st.session_state[
                        "update_success"
                    ] = (
                        "✅ Complaint Updated Successfully!"
                    )


                    st.rerun()


            st.divider()


    else:

        st.warning(
            "📭 No complaints found for your department."
        )


# ---------------------------------------
# LOGOUT
# ---------------------------------------

if st.session_state.officer is not None:

    st.divider()


    if st.button("Logout"):

        st.session_state.officer = None

        st.rerun()