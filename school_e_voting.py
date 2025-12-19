import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="election_db"
)
cursor = db.cursor()

def calculate_age(dob):
    today = datetime.now().date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# ---------------- ADD STUDENT ----------------
def add_student():
    sid = int(input("Enter Student ID: "))
    name = input("Enter Student Name: ")
    cls = input("Enter Class: ")
    div = input("Enter Division: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    cursor.execute(
        "INSERT INTO students VALUES (%s,%s,%s,%s,%s)",
        (sid, name, cls, div, dob)
    )
    db.commit()

# ---------------- ADD TEACHER ----------------
def add_teacher():
    tid = int(input("Enter Teacher ID: "))
    name = input("Enter Teacher Name: ")
    dept = input("Enter Department: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    cursor.execute(
        "INSERT INTO teachers VALUES (%s,%s,%s,%s)",
        (tid, name, dept, dob)
    )
    db.commit()

# ---------------- CHECK STUDENT ----------------
def check_student():
    name = input("Enter Student Name or ID: ")
    cursor.execute(
        "SELECT name, dob FROM students WHERE name=%s OR student_id=%s",
        (name, name)
    )
    record = cursor.fetchone()
    if record:
        dob = datetime.strptime(str(record[1]), "%Y-%m-%d").date()
        age = calculate_age(dob)
        if age >= 18:
            print(f"{record[0]} is {age} years old and eligible for election.")
        else:
            print(f"{record[0]} is {age} years old and not eligible for election.")

# ---------------- CHECK TEACHER (CORRECTED) ----------------
def check_teacher():
    name = input("Enter Teacher Name or ID: ")
    cursor.execute(
        "SELECT name, dob FROM teachers WHERE name=%s OR teacher_id=%s",
        (name, name)
    )
    record = cursor.fetchone()
    if record:
        dob = datetime.strptime(str(record[1]), "%Y-%m-%d").date()
        age = calculate_age(dob)

        if age < 18:
            print(f"{record[0]} is {age} years old and not eligible for election.")
        elif age >= 60:
            print(f"{record[0]} is {age} years old, eligible for election and is a Senior Citizen.")
        else:
            print(f"{record[0]} is {age} years old and eligible for election.")

# ---------------- LIST ELIGIBLE STUDENTS ----------------
def list_eligible_students():
    cursor.execute("SELECT name, dob FROM students")
    for r in cursor.fetchall():
        dob = datetime.strptime(str(r[1]), "%Y-%m-%d").date()
        if calculate_age(dob) >= 18:
            print(r[0])

# ---------------- LIST ELIGIBLE TEACHERS ----------------
def list_eligible_teachers():
    cursor.execute("SELECT name, dob FROM teachers")
    for r in cursor.fetchall():
        dob = datetime.strptime(str(r[1]), "%Y-%m-%d").date()
        age = calculate_age(dob)
        if age >= 18:
            if age >= 60:
                print(f"{r[0]} (Senior Citizen)")
            else:
                print(r[0])

# ---------------- MAIN MENU ----------------
def main():
    while True:
        print("\n===== E-VOTING ELIGIBILITY SYSTEM =====")
        print("1. Add Student Details")
        print("2. Add Teacher Details")
        print("3. Check Student Eligibility")
        print("4. Check Teacher Eligibility")
        print("5. List Eligible Students")
        print("6. List Eligible Teachers")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            check_student()
        elif choice == '4':
            check_teacher()
        elif choice == '5':
            list_eligible_students()
        elif choice == '6':
            list_eligible_teachers()
        elif choice == '7':
            break

main()

