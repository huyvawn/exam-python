# create repository
import mysql.connector
from datetime import datetime

# 1. Connect to database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="medical_service"
    )

def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS medical_service")
    cursor.execute("USE medical_service")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        date_of_birth DATE NOT NULL,
        gender VARCHAR(10) NOT NULL,
        address VARCHAR(255),
        phone_number VARCHAR(15),
        email VARCHAR(100)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        specialization VARCHAR(100) NOT NULL,
        phone_number VARCHAR(15),
        email VARCHAR(100),
        years_of_experience INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT NOT NULL,
        doctor_id INT NOT NULL,
        appointment_date DATETIME NOT NULL,
        reason VARCHAR(255),
        status VARCHAR(50) DEFAULT 'pending',
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
    );
    """)
    conn.commit()
    conn.close()

# 2. Add 3 patients and 5 doctors
def insert_patients(cursor):
    patients = [
        ("Nguyen A", "2010-01-01", "Male", "Ha Noi", "0123456789", "nguyena@gmail.com"),
        ("Nguyen B", "1990-01-01", "Female", "Ha Noi", "0987654321", "nguyenb@gmail.com"),
        ("Nguyen C", "2000-01-01", "Male", "Ho Chi Minh", "0123456788", "nguyencc@gmail.com"),
    ]
    cursor.executemany("""
        INSERT INTO patients (full_name, date_of_birth, gender, address, phone_number, email)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, patients)

def insert_doctors(cursor):
    doctors = [
        ("Nguyen Si", "Orthopetrics", "0123456987", "singuyen@gmail.com", 3),
        ("Tran Binh", "Neurology", "0111222333", "binhtran@gmail.com", 10),
        ("Pham Hao", "Diagnostic", "0333444555", "haopham@gmail.com", 5),
        ("Bui Long", "Pediatrics", "0444555666", "longbui@gmail.com", 2),
        ("Nguyen Minh", "Surgery", "0777888999", "minhnguyen@gmail.com", 5),
    ]
    cursor.executemany("""
        INSERT INTO doctors (full_name, specialization, phone_number, email, years_of_experience)
        VALUES (%s, %s, %s, %s, %s)
    """, doctors)

# 3. Add appointments
def insert_appointments(cursor):
    appointments = [
        (1, 1, datetime(2025, 6, 5, 8, 0), "Shoulder ache", "pending"),
        (2, 2, datetime(2025, 6, 5, 9, 0), "Headache", "pending"),
        (3, 3, datetime(2025, 6, 5, 10, 0), "Patients exhausted, tired", "pending"),
    ]
    cursor.executemany("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason, status)
        VALUES (%s, %s, %s, %s, %s)
    """, appointments)

# 4. Show appointments
def show_appointments(cursor):
    cursor.execute("""
        SELECT p.full_name, p.date_of_birth, p.gender, p.address, d.full_name, a.reason, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    results = cursor.fetchall()
    print("\n----- Appointment Report -----")
    print("No | Patient's name | Birthday | Gender | Address | Doctor | Reason | Date")
    for idx, row in enumerate(results, start=1):
        print(f"{idx} | {' | '.join(str(i) for i in row)}")

# 5. Get appointments for today
def get_today_appointments(cursor):
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(f"""
        SELECT p.address, p.full_name, p.date_of_birth, p.gender, d.full_name, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE DATE(a.appointment_date) = '{today}'
    """)
    results = cursor.fetchall()
    print("\n----- Today's Appointments -----")
    print("Address | No | Patient's name | Birthday | Gender | Doctor | Status")
    for idx, row in enumerate(results, start=1):
        print(f"{row[0]} | {idx} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

def main():
    setup_database()
    conn = connect_db()
    cursor = conn.cursor()

    insert_patients(cursor)
    insert_doctors(cursor)
    insert_appointments(cursor)

    conn.commit()

    show_appointments(cursor)
    get_today_appointments(cursor)

    conn.close()