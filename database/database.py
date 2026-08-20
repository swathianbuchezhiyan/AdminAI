import sqlite3
import os


DATABASE_PATH = "database/adminai.db"


# ---------------------------------------
# Database Connection
# ---------------------------------------

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection



# ---------------------------------------
# Initialize Database
# ---------------------------------------

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    schema_path = "database/schema.sql"


    if os.path.exists(schema_path):

        with open(
            schema_path,
            "r"
        ) as file:

            schema = file.read()

            cursor.executescript(schema)


    connection.commit()

    connection.close()



# ---------------------------------------
# Initialize Default Officers
# ---------------------------------------

def initialize_default_officers():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM officers"
    )

    count = cursor.fetchone()[0]


    if count == 0:

        cursor.execute("""
            INSERT INTO officers
            (
                name,
                username,
                password,
                department,
                role
            )

            VALUES (?, ?, ?, ?, ?)

        """,(
            "Admin Officer",
            "admin",
            "admin123",
            "Administration",
            "Admin"
        ))


    connection.commit()

    connection.close()



# ---------------------------------------
# Save Complaint
# ---------------------------------------

def save_complaint(
    citizen_name,
    mobile_number,
    email,
    district,
    ai_category,
    department,
    ai_confidence,
    priority,
    complaint_title,
    complaint_description,
    image_path
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        INSERT INTO complaints
        (
            full_name,
            mobile_number,
            email,
            district,

            ai_category,
            department,
            ai_confidence,

            priority,

            complaint_title,
            complaint_description,

            image_path
        )


        VALUES
        (
            ?, ?, ?, ?,
            ?, ?, ?,
            ?,
            ?, ?,
            ?
        )

    """,
    (
        citizen_name,
        mobile_number,
        email,
        district,

        ai_category,
        department,
        ai_confidence,

        priority,

        complaint_title,
        complaint_description,

        image_path
    ))



    complaint_number = cursor.lastrowid


    complaint_id = (
        f"ADM2026{complaint_number:04d}"
    )


    cursor.execute("""

        UPDATE complaints

        SET complaint_id = ?

        WHERE id = ?

    """,
    (
        complaint_id,
        complaint_number
    ))


    connection.commit()

    connection.close()


    return complaint_id



# ---------------------------------------
# Get All Complaints
# ---------------------------------------

def get_all_complaints():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT *

        FROM complaints

        ORDER BY id DESC

    """)


    complaints = cursor.fetchall()


    connection.close()


    return complaints



# ---------------------------------------
# Update Complaint Status
# ---------------------------------------

def update_complaint_status(
    complaint_id,
    status,
    officer_remark
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        UPDATE complaints

        SET
            status = ?,
            officer_remark = ?

        WHERE complaint_id = ?

    """,
    (
        status,
        officer_remark,
        complaint_id
    ))


    connection.commit()

    connection.close()



# ---------------------------------------
# Add Officer
# ---------------------------------------

def add_officer(
    name,
    username,
    password,
    department,
    role="Officer"
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        INSERT INTO officers
        (
            name,
            username,
            password,
            department,
            role
        )

        VALUES (?, ?, ?, ?, ?)

    """,
    (
        name,
        username,
        password,
        department,
        role
    ))


    connection.commit()

    connection.close()



# ---------------------------------------
# Verify Officer Login
# ---------------------------------------

def verify_officer(
    username,
    password
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT *

        FROM officers

        WHERE username = ?

        AND password = ?

    """,
    (
        username,
        password
    ))


    officer = cursor.fetchone()


    connection.close()


    return officer



# ---------------------------------------
# Get Department Complaints
# ---------------------------------------

def get_department_complaints(
    department
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""

        SELECT *

        FROM complaints

        WHERE department = ?

        ORDER BY id DESC

    """,
    (
        department,
    ))


    complaints = cursor.fetchall()


    connection.close()


    return complaints