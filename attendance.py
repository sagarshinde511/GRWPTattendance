import streamlit as st
import mysql.connector

# Database connection details
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1",
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Function to fetch existing student IDs
def get_stud_ids():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, studId FROM attendance_enroll")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to update student ID
def update_stud_id(record_id, new_stud_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE attendance_enroll SET studId = %s WHERE id = %s", (new_stud_id, record_id))
    conn.commit()
    conn.close()

# Function to insert student data into StudentAttendance
def insert_student(roll_no, name, branch):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO StudentAttendance (RollNo, Name, Branch) VALUES (%s, %s, %s)", (roll_no, name, branch))
    conn.commit()
    conn.close()

# Function to fetch attendance records
def get_attendance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM StoreAttendance")
    data = cursor.fetchall()
    conn.close()
    return data

# Streamlit UI
st.title("Student Attendance Management")

tabs = st.tabs(["Update Student ID", "Register Student", "Check Attendance"])

# Tab 1: Update Student ID
with tabs[0]:
    st.header("Update Student ID in Attendance Enroll")
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

# Tab 2: Register Student
with tabs[1]:
    st.header("Register New Student")
    roll_no = st.text_input("Roll Number:")
    name = st.text_input("Name:")
    branch = st.text_input("Branch:")
    if st.button("Register"):
        if roll_no and name and branch:
            insert_student(roll_no, name, branch)
            st.success(f"Student {name} (Roll No: {roll_no}) registered successfully.")
        else:
            st.warning("Please fill all fields.")

# Tab 3: Check Attendance
with tabs[2]:
    st.header("Attendance Records")
    attendance_data = get_attendance()
    if attendance_data:
        st.table(attendance_data)
    else:
        st.warning("No attendance records found.")
