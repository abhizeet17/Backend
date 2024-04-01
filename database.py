import psycopg2

# Database connection details (replace if your host is different)
dbname = "postgres"
dbuser = "postgres"
dbpassword = "newpassword"
dbhost = "localhost"  # Update if your database is on a different host

# SQL statement to create the table
sql_create_table = """
CREATE TABLE IF NOT EXISTS courses (
  course_id SERIAL PRIMARY KEY,
  course_name VARCHAR(255) NOT NULL,
  course_description TEXT NOT NULL
);
"""

# Comments explaining each sample course insertion
sql_insert_courses = [
    """INSERT INTO courses (course_name, course_description) VALUES (%s, %s);""",
    ("Introduction to Programming", "Learn the fundamentals of programming using Python."),
    ("Data Structures and Algorithms", "Explore efficient ways to organize and manipulate data."),
    ("Computer Architecture", "Understand the hardware components and their interaction within a computer system."),
    ("Software Engineering", "Master the principles of designing, developing, and maintaining software."),
    ("Database Management Systems", "Learn how to store, retrieve, and manage data in a structured way."),
]


def connect_to_db():
    """Connects to the PostgreSQL database and returns the connection object.

    This function attempts to connect to the PostgreSQL database using the provided credentials.
    If successful, it returns a connection object. Otherwise, it prints an error message and returns None.
    """
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def create_table(conn):
    """Creates the 'courses' table in the database if it doesn't already exist.

    This function takes a database connection object as input. It executes an SQL statement to create
    the 'courses' table with the specified schema (columns and data types) if the table doesn't exist.
    Upon successful creation, it prints a confirmation message. In case of errors, it prints an error message.
    """
    try:
        cur = conn.cursor()
        cur.execute(sql_create_table)
        conn.commit()
        print("Table 'courses' created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_courses(conn, sql_statements):
    """Inserts sample computer science courses into the 'courses' table.

    This function takes a database connection object and a list of SQL statements as input.
    The SQL statements are expected to be INSERT statements for populating the 'courses' table.
    It iterates through the list, executing each statement and committing the changes to the database.
    Upon successful insertion, it prints a confirmation message. In case of errors, it prints an error message.
    """
    try:
        cur = conn.cursor()
        for statement in sql_statements:
            cur.execute(statement)
        conn.commit()
        print("Sample computer science courses inserted!")
    except Exception as e:
        print(f"Error inserting courses: {e}")


if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        create_table(conn)
        insert_courses(conn, sql_insert_courses)
        conn.close()
