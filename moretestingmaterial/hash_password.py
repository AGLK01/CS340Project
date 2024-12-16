from werkzeug.security import generate_password_hash
import psycopg2

conn = psycopg2.connect(
    host="aws-0-eu-central-1.pooler.supabase.com",
    database="postgres",
    user="postgres.agwvpuvzmhsberiqxsim",
    password="kjkger2346wgae#$Q^"
)
cursor = conn.cursor()

username = "testuser"
plain_password = "testpassword"
hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256')

cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, hashed_password))
conn.commit()
cursor.close()
conn.close()

print("Test user created successfully.")
