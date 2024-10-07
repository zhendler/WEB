from sqlalchemy import create_engine, func, desc, cast, Numeric
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade

# Налаштування підключення до бази даних
DATABASE_URL = 'postgresql+psycopg2://example:example@localhost:5432/mydatabase'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    try:
        result = session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
        ).join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
        return result
    except Exception as e:
        print(f"Error in select_1: {e}")
        return []
    finally:
        session.close()

def select_2(subject_name):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    try:
        subquery = session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
        ).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Student.id).order_by(desc('avg_grade')).limit(1).all()
        return subquery
    except Exception as e:
        print(f"Error in select_2: {e}")
        return []
    finally:
        session.close()

def select_3(subject_name):
    """
    Знайти середній бал у групах з певного предмета.
    """
    try:
        result = session.query(
            Group.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
        ).select_from(Group).join(Group.students).join(Grade).join(Subject).filter(Subject.name == subject_name).group_by(Group.id).all()
        return result
    except Exception as e:
        print(f"Error in select_3: {e}")
        return []
    finally:
        session.close()


def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    try:
        result = session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
        ).scalar()
        return result
    except Exception as e:
        print(f"Error in select_4: {e}")
        return None
    finally:
        session.close()

def select_5(teacher_fullname):
    """
    Знайти які курси читає певний викладач.
    """
    try:
        result = session.query(Subject.name).join(Teacher).filter(Teacher.fullname == teacher_fullname).all()
        return [subject[0] for subject in result]
    except Exception as e:
        print(f"Error in select_5: {e}")
        return []
    finally:
        session.close()

def select_6(group_name):
    """
    Знайти список студентів у певній групі.
    """
    try:
        result = session.query(Student.fullname).join(Group).filter(Group.name == group_name).all()
        return [student[0] for student in result]
    except Exception as e:
        print(f"Error in select_6: {e}")
        return []
    finally:
        session.close()

def select_7(group_name, subject_name):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    try:
        result = session.query(
            Student.fullname,
            Grade.grade,
            Grade.timestamp
        ).join(Group).join(Grade).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).all()
        return result
    except Exception as e:
        print(f"Error in select_7: {e}")
        return []
    finally:
        session.close()

def select_8(teacher_fullname):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    try:
        result = session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label('avg_grade')
        ).join(Subject).join(Teacher).filter(Teacher.fullname == teacher_fullname).scalar()
        return result
    except Exception as e:
        print(f"Error in select_8: {e}")
        return None
    finally:
        session.close()

def select_9(student_fullname):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    try:
        result = session.query(Subject.name).join(Grade).join(Student).filter(Student.fullname == student_fullname).distinct().all()
        return [subject[0] for subject in result]
    except Exception as e:
        print(f"Error in select_9: {e}")
        return []
    finally:
        session.close()

def select_10(student_fullname, teacher_fullname):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    try:
        result = session.query(Subject.name).join(Grade).join(Student).join(Teacher).filter(
            Student.fullname == student_fullname,
            Teacher.fullname == teacher_fullname
        ).distinct().all()
        return [subject[0] for subject in result]
    except Exception as e:
        print(f"Error in select_10: {e}")
        return []
    finally:
        session.close()

if __name__ == "__main__":
    # Приклад виклику функцій
    print("Top 5 students by average grade:")
    print(select_1())

    print("\nTop student in Mathematics:")
    print(select_2("Mathematics"))

    print("\nAverage grade per group in Physics:")
    print(select_3("Physics"))

    print("\nOverall average grade:")
    print(select_4())

    print("\nCourses taught by a specific teacher:")
    print(select_5("Tammy Singh"))

    print("\nStudents in Group A:")
    print(select_6("Group A"))

    print("\nGrades in Group B for Chemistry:")
    print(select_7("Group B", "Chemistry"))

    print("\nAverage grade given by a specific teacher:")
    print(select_8("Tammy Singh"))

    print("\nCourses attended by a specific student:")
    print(select_9("Rebecca Wright"))

    print("\nCourses that Alice Johnson is taught by Jane Smith:")
    print(select_10("Rebecca Wright", "Tammy Singh"))
