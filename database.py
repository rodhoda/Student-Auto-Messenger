from sqlalchemy import create_engine, Column, Integer, String, Time, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

Base = declarative_base()


# Define the SQLAlchemy ORM class for the Students table
class Student(Base):
    __tablename__ = 'Students'

    StudentID = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    Phone = Column(String(10), nullable=True)
    Class_time = Column(Time, nullable=True)
    Class_day = Column(String(10), nullable=True)


# Create the database engine
engine = create_engine('sqlite:///students.db')

# This line will create the tables if they do not exist, based on the SqlDatabase class
Base.metadata.create_all(engine)

# Create a sessionmaker, bound to the engine
Session = sessionmaker(bind=engine)


class Database():
    def __init__(self, student_object=None):
        self.student_name = student_object.name
        self.student_phone = student_object.number
        self.student_class_time = student_object.class_time
        self.student_class_day = student_object.class_day

        self.session = Session()

    def add_student(self):
        new_student = Student(Name=self.student_name,
                              Phone=self.student_phone,
                              Class_time=self.student_class_time,
                              Class_day=self.student_class_day)
        self.session.add(new_student)
        self.session.commit()

    def delete_student(self):
        student = self.session.query(Student).filter_by(Name=self.student_name)
        for s in student:
            self.session.delete(s)
            self.session.commit()

    def view_student_info(self):
        student = self.session.query(Student).filter_by(Name=self.student_name)
        return [attribute for s in student for attribute in (s.Name, s.Phone, s.Class_day, s.Class_time)]
