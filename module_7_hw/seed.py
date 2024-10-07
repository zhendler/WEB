from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade, group_subject_association
from faker import Faker
import random
import datetime

# Налаштування підключення до бази даних
DATABASE_URL = 'postgresql+psycopg2://example:example@localhost:5432/mydatabase'
# Для SQLite використовуйте:
# DATABASE_URL = 'sqlite:///mydatabase.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


def seed():
    # Створення груп
    group_names = ['Group A', 'Group B', 'Group C']
    groups = [Group(name=name) for name in group_names]
    session.add_all(groups)
    session.commit()

    # Створення викладачів
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()

    # Створення предметів
    subject_names = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Literature', 'English',
                     'Computer Science']
    subjects = []
    for name in subject_names[:random.randint(5, 8)]:
        teacher = random.choice(teachers)
        subjects.append(Subject(name=name, teacher=teacher))
    session.add_all(subjects)
    session.commit()

    # Асигнуємо предмети до груп
    for group in groups:
        # Випадково призначаємо кілька предметів кожній групі
        assigned_subjects = random.sample(subjects, k=random.randint(3, len(subjects)))
        group.subjects.extend(assigned_subjects)
    session.commit()

    # Створення студентів
    students = [Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(30)]
    session.add_all(students)
    session.commit()

    # Створення оцінок
    for student in students:
        # Отримуємо предмети, які відвідує група студента
        student_subjects = student.group.subjects
        for subject in student_subjects:
            num_grades = random.randint(5, 20)
            for _ in range(num_grades):
                grade = random.randint(1, 100)
                timestamp = fake.date_time_between(start_date='-1y', end_date='now')
                session.add(Grade(grade=round(grade, 2), timestamp=timestamp, student=student, subject=subject))
    session.commit()
    print("Database seeded successfully.")


if __name__ == "__main__":
    seed()
