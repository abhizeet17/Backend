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

# Define the SQL statement to create the login table
create_login_table_query = """
CREATE TABLE IF NOT EXISTS login (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);
"""

# Execute the SQL command to create the login table
cursor.execute(create_login_table_query)

# Commit changes to the database
conn.commit()

# Function to add user information to signup table
def add_user_to_signup(username, password, name, role):
    hashed_password = hash_password(password)
    insert_query = """
    INSERT INTO signup (username, password, name, role)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (username, hashed_password, name, role))
    conn.commit()

# Function to add user information to login table
def add_user_to_login(username, password, role):
    hashed_password = hash_password(password)
    insert_query = """
    INSERT INTO login (username, password, role)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_query, (username, hashed_password, role))
    conn.commit()

# Clear existing data from the tables
truncate_signup_table_query = """
TRUNCATE TABLE signup;
"""
cursor.execute(truncate_signup_table_query)

truncate_login_table_query = """
TRUNCATE TABLE login;
"""
cursor.execute(truncate_login_table_query)

# Example usage
add_user_to_signup("user1", "password123", "John Doe", "user")
add_user_to_login("user1", "password123", "user")

# Close cursor and connection
cursor.close()
conn.close()
