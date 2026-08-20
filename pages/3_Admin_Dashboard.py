import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from database.database import get_all_complaints
from models.predict import generate_summary


# =======================================
# PAGE TITLE
# =======================================

st.title("📊 Admin Dashboard")
st.subheader("Complaint Management System")


# =======================================
# GET COMPLAINTS
# =======================================

complaints = get_all_complaints()


if len(complaints) == 0:

    st.info("No complaints available")

else:

    # ===================================
    # DATABASE COLUMNS
    # ===================================

    columns = [
        "ID",
        "Complaint ID",
        "Name",
        "Mobile",
        "Email",
        "District",
        "AI Category",
        "Department",
        "AI Confidence",
        "Priority",
        "Title",
        "Description",
        "Image",
        "Status",
        "Officer Remark",
        "Updated At",
        "Submitted Date"
    ]


    # ===================================
    # CREATE DATAFRAME
    # ===================================

    df = pd.DataFrame(
        complaints,
        columns=columns
    )


    # ===================================
    # SEARCH & FILTERS
    # ===================================

    st.subheader("🔍 Search & Filters")

    col1, col2 = st.columns(2)


    with col1:

        search = st.text_input(
            "Search Complaint ID / Citizen Name"
        )


        department_filter = st.selectbox(
            "Department",
            [
                "All"
            ]
            +
            sorted(
                df["Department"]
                .dropna()
                .unique()
                .tolist()
            )
        )


    with col2:

        status_filter = st.selectbox(
            "Status",
            [
                "All"
            ]
            +
            sorted(
                df["Status"]
                .dropna()
                .unique()
                .tolist()
            )
        )


        priority_filter = st.selectbox(
            "Priority",
            [
                "All"
            ]
            +
            sorted(
                df["Priority"]
                .dropna()
                .unique()
                .tolist()
            )
        )


    # ===================================
    # APPLY FILTERS
    # ===================================

    filtered_df = df.copy()


    if search:

        filtered_df = filtered_df[
            filtered_df["Complaint ID"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
            |
            filtered_df["Name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]


    if department_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Department"]
            == department_filter
        ]


    if status_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Status"]
            == status_filter
        ]


    if priority_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Priority"]
            == priority_filter
        ]


    # ===================================
    # NO RESULTS
    # ===================================

    if filtered_df.empty:

        st.warning(
            "No complaints found for selected filters."
        )

        st.stop()


    # ===================================
    # COMPLAINT OVERVIEW
    # ===================================

    st.subheader("📈 Complaint Overview")


    total = len(filtered_df)


    pending = len(
        filtered_df[
            filtered_df["Status"]
            == "Pending"
        ]
    )


    in_progress = len(
        filtered_df[
            filtered_df["Status"]
            == "In Progress"
        ]
    )


    resolved = len(
        filtered_df[
            filtered_df["Status"]
            == "Resolved"
        ]
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Complaints",
        total
    )


    col2.metric(
        "Pending",
        pending
    )


    col3.metric(
        "In Progress",
        in_progress
    )


    col4.metric(
        "Resolved",
        resolved
    )


    st.divider()


    # ===================================
    # AI SUMMARY
    # ===================================

    st.subheader("🤖 AI Complaint Summary")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "AI Categories",
        filtered_df["AI Category"].nunique()
    )


    col2.metric(
        "High Priority",
        len(
            filtered_df[
                filtered_df["Priority"]
                == "High"
            ]
        )
    )


    # Make confidence numeric
    confidence_values = pd.to_numeric(
        filtered_df["AI Confidence"],
        errors="coerce"
    )


    average_confidence = confidence_values.mean()


    if pd.isna(average_confidence):

        average_confidence = 0


    col3.metric(
        "Average Confidence",
        f"{round(average_confidence, 2)}%"
    )


    st.divider()


    # ===================================
    # DEPARTMENT ANALYTICS
    # ===================================

    st.subheader(
        "🏢 Department-wise Complaints"
    )


    department_count = (
        filtered_df["Department"]
        .value_counts()
        .reset_index()
    )


    department_count.columns = [
        "Department",
        "Complaints"
    ]


    bar_fig = px.bar(
        department_count,
        x="Department",
        y="Complaints",
        text="Complaints",
        title="Complaints by Department"
    )


    bar_fig.update_layout(
        height=400,
        showlegend=False
    )


    st.plotly_chart(
        bar_fig,
        use_container_width=True
    )


    st.divider()


    # ===================================
    # PRIORITY DISTRIBUTION
    # ===================================

    st.subheader(
        "🚨 AI Priority Distribution"
    )


    priority_count = (
        filtered_df["Priority"]
        .value_counts()
        .reset_index()
    )


    priority_count.columns = [
        "Priority",
        "Count"
    ]


    priority_chart = px.pie(
        priority_count,
        names="Priority",
        values="Count",
        hole=0.4,
        title="AI Priority Overview"
    )


    st.plotly_chart(
        priority_chart,
        use_container_width=True
    )


    st.divider()


    # ===================================
    # STATUS DISTRIBUTION
    # ===================================

    st.subheader(
        "📌 Complaint Status Distribution"
    )


    status_count = (
        filtered_df["Status"]
        .value_counts()
        .reset_index()
    )


    status_count.columns = [
        "Status",
        "Count"
    ]


    pie_fig = px.pie(
        status_count,
        names="Status",
        values="Count",
        hole=0.4,
        title="Complaint Status Overview"
    )


    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )


    st.divider()


    # ===================================
    # COMPLAINT DETAILS
    # ===================================

    st.subheader(
        "📋 Complaint Details"
    )


    for index, row in filtered_df.iterrows():

        with st.expander(
            f"🆔 {row['Complaint ID']} | {row['Title']}"
        ):

            # ---------------------------
            # Citizen Details
            # ---------------------------

            st.write(
                f"👤 Citizen: {row['Name']}"
            )


            st.write(
                f"📱 Mobile: {row['Mobile']}"
            )


            st.write(
                f"📧 Email: {row['Email']}"
            )


            st.write(
                f"📍 District: {row['District']}"
            )


            # ---------------------------
            # AI Details
            # ---------------------------

            st.write(
                f"🤖 AI Category: {row['AI Category']}"
            )


            st.write(
                f"🏢 Department: {row['Department']}"
            )


            st.write(
                f"📊 AI Confidence: "
                f"{row['AI Confidence']}%"
            )


            st.write(
                f"🚨 Priority: {row['Priority']}"
            )


            st.write(
                f"📌 Status: {row['Status']}"
            )


            # ---------------------------
            # Complaint
            # ---------------------------

            st.write(
                f"📝 Title: {row['Title']}"
            )


            st.write(
                f"📄 Description: "
                f"{row['Description']}"
            )


            # ===================================
            # AI GENERATED SUMMARY
            # ===================================

            st.markdown("---")

            st.subheader(
                "🤖 AI Generated Summary"
            )


            description = str(
                row["Description"]
            )


            summary = generate_summary(
                description
            )


            st.info(
                f"📝 {summary}"
            )


            # ===================================
            # OFFICER REMARK
            # ===================================

            st.markdown("---")


            remark = row["Officer Remark"]


            # FIX FOR NaN / NULL
            if (
                pd.notna(remark)
                and str(remark).strip() != ""
                and str(remark).lower() != "nan"
            ):

                st.success(
                    f"👮 Officer Remark: {remark}"
                )

            else:

                st.warning(
                    "👮 Officer Remark: Not updated"
                )


            # ===================================
            # COMPLAINT IMAGE
            # ===================================

            if (
                pd.notna(row["Image"])
                and str(row["Image"]).strip() != ""
                and str(row["Image"]).lower() != "nan"
            ):

                image_path = str(
                    row["Image"]
                )


                if Path(image_path).exists():

                    st.image(
                        image_path,
                        use_container_width=True
                    )


            # ===================================
            # DATES
            # ===================================

            st.caption(
                f"🕒 Submitted: "
                f"{row['Submitted Date']}"
            )


            if (
                pd.notna(row["Updated At"])
                and str(row["Updated At"]).strip() != ""
                and str(row["Updated At"]).lower() != "nan"
            ):

                st.caption(
                    f"🔄 Updated: "
                    f"{row['Updated At']}"
                )