from database import (
    initialize_database,
    initialize_default_officers
)

import sqlite3


# ---------------------------------------
# Initialize Database
# ---------------------------------------

initialize_database()


# ---------------------------------------
# Create Default Officers
# ---------------------------------------

initialize_default_officers()


# ---------------------------------------
# Test Complaints
# ---------------------------------------

connection = sqlite3.connect(
    "database/adminai.db"
)

cursor = connection.cursor()


cursor.execute(
    "SELECT * FROM complaints"
)

complaints = cursor.fetchall()


print(
    "Total Complaints:",
    len(complaints)
)


for complaint in complaints:
    print(complaint)



# ---------------------------------------
# Test Officers
# ---------------------------------------

cursor.execute(
    "SELECT * FROM officers"
)

officers = cursor.fetchall()


print(
    "\nTotal Officers:",
    len(officers)
)


for officer in officers:
    print(officer)



connection.close()