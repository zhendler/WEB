from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

# Ассоціативна таблиця для відношення багато до багато між Group та Subject
group_subject_association = Table(
    'group_subject',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True)
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship('Student', back_populates='group')
    subjects = relationship('Subject', secondary=group_subject_association, back_populates='groups')


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship('Group', back_populates='students')
    grades = relationship('Grade', back_populates='student')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)

    subjects = relationship('Subject', back_populates='teacher')


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship('Teacher', back_populates='subjects')
    grades = relationship('Grade', back_populates='subject')
    groups = relationship('Group', secondary=group_subject_association, back_populates='subjects')


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    grade = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))

    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')
