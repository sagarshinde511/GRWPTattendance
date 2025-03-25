import streamlit as st
import mysql.connector

# Database connection details
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1",
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Function to fetch existing studId records
def get_stud_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, studId FROM attendance_enroll")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to update studId
def update_stud_id(record_id, new_stud_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE attendance_enroll SET studId = %s WHERE id = %s", (new_stud_id, record_id))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("Update Student ID in Attendance Enroll")

# Fetch and display existing studIds
stud_id_records = get_stud_ids()
if stud_id_records:
    record_dict = {f"ID: {rec[0]}, Student ID: {rec[1]}": rec[0] for rec in stud_id_records}
    selected_record = st.selectbox("Select Record to Update:", list(record_dict.keys()))
    
    new_stud_id = st.text_input("Enter New Student ID:")
    
    if st.button("Update"):
        if new_stud_id:
            update_stud_id(record_dict[selected_record], new_stud_id)
            st.success(f"Updated Student ID to {new_stud_id} for {selected_record}")
        else:
            st.warning("Please enter a new Student ID.")
else:
    st.error("No records found in the database.")
