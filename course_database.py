import psycopg2
from flask import Flask, render_template

# Database connection details
dbname = "postgres"
dbuser = "postgres"
dbpassword = "newpassword"
dbhost = "localhost"

app = Flask(__name__)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# SQL statement to create the table
sql_create_table = """
CREATE TABLE IF NOT EXISTS courses (
  course_id SERIAL PRIMARY KEY,
  course_name VARCHAR(255) NOT NULL,
  course_description TEXT NOT NULL
);
"""

# SQL statement to insert a course
sql_insert_course = """
INSERT INTO courses (course_name, course_description) VALUES (%s, %s);
"""

# Sample computer science courses
courses_data = [
    ("Introduction to Programming", "Learn the fundamentals of programming using Python."),
    ("Data Structures and Algorithms", "Explore efficient ways to organize and manipulate data."),
    ("Computer Architecture", "Understand the hardware components and their interaction within a computer system."),
    ("Software Engineering", "Master the principles of designing, developing, and maintaining software."),
    ("Database Management Systems", "Learn how to store, retrieve, and manage data in a structured way."),
]

def connect_to_db():
    """Connects to the PostgreSQL database and returns the connection object."""
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    """Creates the 'courses' table in the database if it doesn't already exist."""
    try:
        with conn.cursor() as cur:
            cur.execute(sql_create_table)
            conn.commit()
            print("Table 'courses' created successfully!")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

def insert_courses(conn, courses):
    """Inserts sample computer science courses into the 'courses' table."""
    try:
        with conn.cursor() as cur:
            for course in courses:
                cur.execute(sql_insert_course, course)
            conn.commit()
            print("Sample computer science courses inserted!")
    except psycopg2.Error as e:
        print(f"Error inserting courses: {e}")

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        create_table(conn)
        insert_courses(conn, courses_data)
        conn.close()

# Run the Flask application
app.run(debug=True)
