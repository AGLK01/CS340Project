from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection details
DB_HOST = "aws-0-eu-central-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.agwvpuvzmhsberiqxsim"
DB_PASS = "kjkger2346wgae#$Q^"
DB_PORT = "6543"

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Employee;")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_employee', methods=['POST'])
def add_employee():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Employee (EID, name, access_level, IsManager, IsMP)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (data['EID'], data['name'], data['access_level'], data['IsManager'], data['IsMP'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee():
    eid = request.args.get('eid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employee WHERE EID = %s;", (eid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Patient (NID, name, dob, medical_records)
            VALUES (%s, %s, %s, %s);
            """,
            (data['NID'], data['name'], data['dob'], data['medical_records'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Patient registered successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_patient', methods=['DELETE'])
def delete_patient():
    nid = request.args.get('nid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Patient WHERE NID = %s;", (nid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Patient deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patients', methods=['GET'])
def get_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Patient;")
        patients = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Books;")
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Books (Patient_NID, Department_Specialty, AppointmentDate, Reason)
            VALUES (%s, %s, %s, %s);
            """,
            (data['Patient_NID'], data['Department_Specialty'], data['AppointmentDate'], data['Reason'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment booked successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_appointment', methods=['DELETE'])
def delete_appointment():
    patient_id = request.args.get('patient_id')
    appointment_date = request.args.get('appointment_date')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE Patient_NID = %s AND AppointmentDate = %s;", (patient_id, appointment_date))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_appointments', methods=['GET'])
def search_appointments():
    date = request.args.get('date')
    patient_id = request.args.get('patient_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM Books WHERE TRUE"
        params = []
        if date:
            query += " AND AppointmentDate::date = %s"
            params.append(date)
        if patient_id:
            query += " AND Patient_NID = %s"
            params.append(patient_id)
        cursor.execute(query, params)
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pharmacy', methods=['GET'])
def get_pharmacy():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Pharmacy;")
        drugs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(drugs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add_drug', methods=['POST'])
def add_drug():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Pharmacy (prescription_id, drug_name, cost, quantity)
            VALUES (%s, %s, %s, %s);
            """,
            (data['prescription_id'], data['drug_name'], data['cost'], data['quantity'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Drug added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete_drug', methods=['DELETE'])
def delete_drug():
    prescription_id = request.args.get('prescription_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Pharmacy WHERE prescription_id = %s;", (prescription_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Drug deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/issue_drug', methods=['POST'])
def issue_drug():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Issues_Drugs (MPID, Patient_NID, Prescription_ID)
            VALUES (%s, %s, %s);
            """,
            (data['MPID'], data['Patient_NID'], data['Prescription_ID'])
        )
        conn.commit()
        cursor.execute(
            "UPDATE Pharmacy SET quantity = quantity - 1 WHERE prescription_id = %s;",
            (data['Prescription_ID'],)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Drug issued successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/issued_drugs', methods=['GET'])
def get_issued_drugs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            """
            SELECT id.MPID, p.name AS patient_name, id.Prescription_ID
            FROM Issues_Drugs id
            JOIN Patient p ON id.Patient_NID = p.NID;
            """
        )
        issued_drugs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(issued_drugs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
