import logging

from psycopg2 import DatabaseError

from connection import create_connection


def create_table(conn, sql_expression):
    c = conn.cursor()
    try:
        c.execute(sql_expression)
        conn.commit()
    except DatabaseError as err:
        logging.error(err)
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_expression = """
     CREATE TABLE IF NOT EXISTS groups (
     id SERIAL PRIMARY KEY,
     group_name VARCHAR(120)
    );
    
     CREATE TABLE IF NOT EXISTS students (
     id SERIAL PRIMARY KEY,
     name VARCHAR(120),
     group_id INT,
     FOREIGN KEY (group_id) REFERENCES groups (id)
     
    );
    

    
    CREATE TABLE IF NOT EXISTS Teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30));
    
    CREATE TABLE IF NOT EXISTS Subjects (
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR(30),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
    );
    
    CREATE TABLE IF NOT EXISTS Grades (
    id SERIAL PRIMARY KEY,
    student_id INT,
    subject_id INT,
    grade INT,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (subject_id) REFERENCES subjects (id),
    date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        with create_connection() as conn:
            if conn is not None:
                create_table(conn, sql_expression)
            else:
                logging.error('Error: can\'t create the database connection')
    except RuntimeError as err:
        logging.error(err)