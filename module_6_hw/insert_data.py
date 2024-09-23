import logging
import random
from faker import Faker
from random import randint
from connection import create_connection


fake = Faker()
NUM_STUDENTS = 50

group_names = ['Alpha', 'Betta', 'Gamma', 'Delta', 'Epsilon']

try:
    with create_connection() as conn:
        with conn.cursor() as cur:
            for name in group_names:
                cur.execute("INSERT INTO groups (group_name) VALUES (%s) RETURNING id;", (name,))
            groups = cur.fetchall()

            teachers = []
            for _ in range(5):
                name = fake.name()
                cur.execute("INSERT INTO teachers (name) VALUES (%s) RETURNING id;", (name,))
                teacher_id = cur.fetchone()[0]
                teachers.append(teacher_id)


            subjects = []
            for _ in range(8):
                sub_name = fake.job()
                teacher_id = random.choice(teachers)
                cur.execute("INSERT INTO subjects (subject_name, teacher_id) VALUES (%s, %s) RETURNING id;", (sub_name, teacher_id))
                sub_id = cur.fetchone()[0]
                subjects.append(sub_id)


            students = []
            for _ in range(NUM_STUDENTS):
                group_id = random.choice(groups)[0]
                name=fake.name()
                cur.execute('INSERT INTO students (name, group_id) VALUES (%s, %s) RETURNING id', (name, group_id))
                student_id = cur.fetchone()[0]
                students.append(student_id)

            for students_id in students:
                num_grades = randint(15, 21)
                for _ in range(num_grades):
                    subj_id = random.choice(subjects)
                    grade = randint(50, 100)
                    date_recived = fake.date_between(start_date='-1y', end_date='today')
                    cur.execute('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s)',
                                (students_id, subj_id, grade, date_recived))


            conn.commit()
            cur.close()
            conn.close()
except Exception as e:
    print(f"Сталася помилка: {e}")




