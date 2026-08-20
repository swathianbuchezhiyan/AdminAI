import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import get_all_complaints


st.title("🤖 AI Analytics Dashboard")

st.subheader("📊 Complaint Intelligence & Insights")



# ---------------------------------------
# AI Priority Analysis Function
# ---------------------------------------

def analyze_priority(description):

    description = str(description).lower()


    high_keywords = [
        "fire",
        "accident",
        "emergency",
        "urgent",
        "no electricity",
        "power cut",
        "water shortage",
        "danger",
        "crime",
        "hospital"
    ]


    medium_keywords = [
        "repair",
        "damage",
        "issue",
        "problem",
        "delay",
        "complaint"
    ]


    for word in high_keywords:

        if word in description:

            return (
                "High",
                "🔴 High",
                90,
                "Emergency issue detected"
            )


    for word in medium_keywords:

        if word in description:

            return (
                "Medium",
                "🟡 Medium",
                70,
                "Department attention required"
            )


    return (
        "Low",
        "🟢 Low",
        50,
        "General complaint"
    )



# ---------------------------------------
# Load Complaints
# ---------------------------------------

complaints = get_all_complaints()



if len(complaints) == 0:

    st.info(
        "No complaints available for analysis"
    )


else:


    # ---------------------------------------
    # Database Columns (17)
    # ---------------------------------------

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


    df = pd.DataFrame(
        complaints,
        columns=columns
    )



    # ---------------------------------------
    # Summary Cards
    # ---------------------------------------

    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "📋 Total Complaints",
        len(df)
    )


    col2.metric(
        "⏳ Pending",
        len(
            df[df["Status"]=="Pending"]
        )
    )


    col3.metric(
        "⚙️ In Progress",
        len(
            df[df["Status"]=="In Progress"]
        )
    )


    col4.metric(
        "✅ Resolved",
        len(
            df[df["Status"]=="Resolved"]
        )
    )


    st.divider()



    # ---------------------------------------
    # Department Chart
    # ---------------------------------------

    st.subheader(
        "🏢 Department-wise Complaints"
    )


    dept_count = (
        df["Department"]
        .value_counts()
        .reset_index()
    )


    dept_count.columns = [
        "Department",
        "Count"
    ]


    dept_chart = px.bar(
        dept_count,
        x="Department",
        y="Count",
        text="Count",
        title="Department Analysis"
    )


    st.plotly_chart(
        dept_chart,
        use_container_width=True
    )



    st.divider()



    # ---------------------------------------
    # AI Category Chart
    # ---------------------------------------

    st.subheader(
        "🤖 AI Category Distribution"
    )


    category_count = (
        df["AI Category"]
        .value_counts()
        .reset_index()
    )


    category_count.columns = [
        "Category",
        "Count"
    ]


    category_chart = px.pie(
        category_count,
        names="Category",
        values="Count",
        hole=0.4
    )


    st.plotly_chart(
        category_chart,
        use_container_width=True
    )



    st.divider()



    # ---------------------------------------
    # Status Chart
    # ---------------------------------------

    st.subheader(
        "📌 Complaint Status"
    )


    status_count = (
        df["Status"]
        .value_counts()
        .reset_index()
    )


    status_count.columns = [
        "Status",
        "Count"
    ]


    status_chart = px.pie(
        status_count,
        names="Status",
        values="Count",
        hole=0.4
    )


    st.plotly_chart(
        status_chart,
        use_container_width=True
    )



    st.divider()



    # ---------------------------------------
    # AI Priority Analysis
    # ---------------------------------------

    st.subheader(
        "🚨 AI Priority Analysis"
    )


    priority_list = []

    high_priority = []



    for index,row in df.iterrows():


        level,display,confidence,reason = analyze_priority(
            row["Description"]
        )


        priority_list.append(level)



        st.info(
f"""
🆔 Complaint ID:
{row["Complaint ID"]}

🤖 AI Category:
{row["AI Category"]}

🏢 Department:
{row["Department"]}

📊 AI Confidence:
{row["AI Confidence"]}%

📝 Description:
{row["Description"]}

🚨 Priority:
{display}

💡 Reason:
{reason}
"""
        )


        if level == "High":

            high_priority.append({

                "Complaint ID":
                row["Complaint ID"],

                "Department":
                row["Department"],

                "Category":
                row["AI Category"],

                "Priority":
                display,

                "Confidence":
                f"{confidence}%"

            })


        if row["Officer Remark"]:

            st.write(
                f"👮 Officer Remark: {row['Officer Remark']}"
            )


        st.divider()



    # ---------------------------------------
    # Priority Chart
    # ---------------------------------------

    st.subheader(
        "📊 Priority Distribution"
    )


    priority_count = (
        pd.Series(priority_list)
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
        hole=0.4
    )


    st.plotly_chart(
        priority_chart,
        use_container_width=True
    )



    st.divider()



    # ---------------------------------------
    # High Priority Complaints
    # ---------------------------------------

    st.subheader(
        "🚨 High Priority Complaints"
    )


    if high_priority:

        high_df = pd.DataFrame(
            high_priority
        )


        st.dataframe(
            high_df,
            use_container_width=True
        )


    else:

        st.success(
            "No High Priority Complaints"
        )



    st.divider()



    # ---------------------------------------
    # AI Insight
    # ---------------------------------------

    st.subheader(
        "🤖 AI Insight"
    )


    top_department = (
        df["Department"]
        .value_counts()
        .idxmax()
    )


    st.success(
f"""
🚨 Highest complaint volume:
{top_department}

AI Recommendation:
Monitor this department and prioritize faster resolution.
"""
    )