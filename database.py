from sqlalchemy import create_engine, Column, Integer, String, Time


class Database():
    def __init__(self, student_object):
        self.student_name = student_object.name
        self.student_phone = student_object.phone
        self.student_class_time = student_object.class_time
        self.student_class_day = student_object.class_day






