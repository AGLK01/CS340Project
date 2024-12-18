from flask import Flask, request, jsonify, render_template
import pg8000
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection details
DB_HOST = "aws-0-eu-central-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_USER = "postgres.agwvpuvzmhsberiqxsim"
DB_PASS = "kjkger2346wgae#$Q^"
DB_PORT = "6543"
def fetch_as_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Connect to PostgreSQL
def get_db_connection():
    conn = pg8000.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    cursor = conn.cursor()
    cursor.execute("SET TIME ZONE 'UTC+3';")  # Set PostgreSQL time zone explicitly
    cursor.close()
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employee;")
        employees = fetch_as_dict(cursor)
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

@app.route('/employees/search', methods=['GET'])
def search_employees():
    name = request.args.get('name')
    eid = request.args.get('eid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Employee WHERE TRUE"
        params = []
        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")
        if eid:
            query += " AND EID = %s"
            params.append(eid)
        cursor.execute(query, params)
        employees = fetch_as_dict(cursor)
        cursor.close()
        conn.close()
        return jsonify(employees)
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
        cursor = conn.cursor()
        cursor.execute("SELECT NID, name, dob, medical_records FROM Patient;")
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        patients = [
            {"nid": row[0], "name": row[1], "dob": row[2], "medical_records": row[3]}
            for row in rows
        ]

        cursor.close()
        conn.close()
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_patients', methods=['GET'])
def search_patients():
    name = request.args.get('name')
    nid = request.args.get('nid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT NID, name, dob, medical_records FROM Patient WHERE TRUE"
        params = []
        if name:
            query += " AND name ILIKE %s"
            params.append(f"%{name}%")
        if nid:
            query += " AND NID = %s"
            params.append(nid)
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        patients = [
            {"nid": row[0], "name": row[1], "dob": row[2], "medical_records": row[3]}
            for row in rows
        ]

        cursor.close()
        conn.close()
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT appointment_id, Patient_NID, Department_Specialty, AppointmentDate, Reason FROM Books;")
        rows = cursor.fetchall()

        # Convert rows to dictionaries without time manipulation
        appointments = [
            {
                "appointment_id": row[0],
                "patient_nid": row[1],
                "department_specialty": row[2],
                "appointmentdate": row[3].strftime('%Y-%m-%d %H:%M:%S'),  # Plain timestamp as string
                "reason": row[4]
            }
            for row in rows
        ]

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
    appointment_id = request.args.get('appointment_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE appointment_id = %s;", (appointment_id,))
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
    department_specialty = request.args.get('department_specialty')
    appointment_id = request.args.get('appointment_id')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT appointment_id, Patient_NID, Department_Specialty, AppointmentDate, Reason
            FROM Books WHERE TRUE
        """
        params = []
        if date:
            query += " AND AppointmentDate::date = %s"
            params.append(date)
        if patient_id:
            query += " AND Patient_NID = %s"
            params.append(patient_id)
        if department_specialty:
            query += " AND Department_Specialty ILIKE %s"
            params.append(f"%{department_specialty}%")
        if appointment_id:
            query += " AND appointment_id = %s"
            params.append(appointment_id)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        appointments = [
            {
                "appointment_id": row[0],
                "patient_nid": row[1],
                "department_specialty": row[2],
                "appointmentdate": row[3],
                "reason": row[4]
            }
            for row in rows
        ]

        cursor.close()
        conn.close()
        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pharmacy', methods=['GET'])
def get_pharmacy():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT prescription_id, drug_name, cost, quantity FROM Pharmacy;")
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        drugs = [
            {"prescription_id": row[0], "drug_name": row[1], "cost": row[2], "quantity": row[3]}
            for row in rows
        ]

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
        return jsonify({"message": "Drugs issued successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/issued_drugs', methods=['GET'])
def get_issued_drugs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id.MPID, p.name AS patient_name, id.Prescription_ID
            FROM Issues_Drugs id
            JOIN Patient p ON id.Patient_NID = p.NID;
            """
        )
        rows = cursor.fetchall()

        # Convert rows to dictionaries
        issued_drugs = [
            {"mpid": row[0], "patient_name": row[1], "prescription_id": row[2]}
            for row in rows
        ]

        cursor.close()
        conn.close()
        return jsonify(issued_drugs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


from werkzeug.security import generate_password_hash

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Save username and hashed password to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201


    except Exception as e:

        if "duplicate key value" in str(e).lower() or "unique constraint" in str(e).lower():
            return jsonify({"error": "Username already exists"}), 409

        return jsonify({"error": str(e)}), 500


from werkzeug.security import check_password_hash

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    try:
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Case-insensitive query for username
        cursor.execute("SELECT username, password FROM users WHERE LOWER(username) = LOWER(%s);", (username,))
        user = cursor.fetchone()

        # Log fetched user for debugging
        print(f"Fetched user: {user}")

        cursor.close()
        conn.close()

        if user and check_password_hash(user[1], password):  # Access password by index 1
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == '__main__':
    app.run(debug=True)
