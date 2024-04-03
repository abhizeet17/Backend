import psycopg2
from psycopg2 import sql
import bcrypt

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="newpassword",
    host="localhost",
    port="5432"
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Define the SQL statement to create the signup table
create_signup_table_query = """
CREATE TABLE IF NOT EXISTS signup (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);
"""

# Execute the SQL command to create the signup table
cursor.execute(create_signup_table_query)

# Commit changes to the database
conn.commit()

# Function to check if user exists in signup table
def user_exists(username):
    cursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
    return cursor.fetchone() is not None

# Function to add user information to signup table
def add_user_to_signup(username, password, name, role):
    hashed_password = hash_password(password)
    insert_query = """
    INSERT INTO signup (username, password, name, role)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (username, hashed_password, name, role))
    conn.commit()

def login_or_signup(username, password, name, role):
    if user_exists(username):
        print("User already exists. Please choose a different username.")
    else:
        add_user_to_signup(username, password, name, role)
        print("User signed up successfully.")

# Example usage
login_or_signup("user1", "password123", "John Doe", "user")

# Close cursor and connection
cursor.close()
conn.close()
