from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.route('/search_patient', methods=['GET'])
def search_patient():
    name = request.args.get('name')
    nid = request.args.get('nid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        if name:
            cursor.execute("SELECT * FROM Patient WHERE name ILIKE %s;", (f"%{name}%",))
        elif nid:
            cursor.execute("SELECT * FROM Patient WHERE NID = %s;", (nid,))
        else:
            return jsonify({"error": "No search criteria provided"}), 400
        patients = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search_employee', methods=['GET'])
def search_employee():
    name = request.args.get('name')
    eid = request.args.get('eid')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        if name and eid:
            cursor.execute("SELECT * FROM Employee WHERE name ILIKE %s AND EID = %s;", (f"%{name}%", eid))
        elif name:
            cursor.execute("SELECT * FROM Employee WHERE name ILIKE %s;", (f"%{name}%",))
        elif eid:
            cursor.execute("SELECT * FROM Employee WHERE EID = %s;", (eid,))
        else:
            return jsonify({"error": "No search criteria provided"}), 400
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
