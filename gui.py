# Student_Auto_Messenger

import csv
import pandas as pd
import os
import student
import database
from datetime import datetime
import tkinter as tk


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Student Auto-Messenger")
        self.geometry("600x500")

        self.add_student_button = tk.Button(self, text="Add Student", command=self.add)
        self.add_student_button.pack(side='top')

        self.delete_student_button = tk.Button(self, text="Delete Student", command=self.delete)
        self.delete_student_button.pack()

        self.view_student_button = tk.Button(self, text="View Student Info", command=self.view)
        self.view_student_button.pack()

        tk.Label(self, text="Welcome to the Student Auto Messenger!").pack(expand=True)

        self.exit_button = tk.Button(self, text="Exit", command=self.destroy)
        self.exit_button.pack(side='bottom',anchor='center')

    def add(self):
        add_window = AddStudentWindow()
        add_window.mainloop()

    def delete(self):
        delete_window = DeleteStudentWindow()
        delete_window.mainloop()
    def view(self):
        view_window = ViewStudentWindow()
        view_window.mainloop()


class AddStudentWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Add Student Info")
        self.geometry("500x200")

        tk.Label(self, text="Student Name:").grid(row=0, column=0, sticky='e')
        self.student_name = tk.Text(self, height=2, width=20)
        self.student_name.grid(row=0, column=1)

        tk.Label(self, text="Student Phone # (Only numbers):").grid(row=1, column=0, sticky='e')
        self.student_phone = tk.Text(self, height=2, width=20)
        self.student_phone.grid(row=1, column=1)

        tk.Label(self, text="Student Class Time (08:00 or 20:00):").grid(row=2, column=0, sticky='e')
        self.student_class_time = tk.Text(self, height=2, width=20)
        self.student_class_time.grid(row=2, column=1)

        tk.Label(self, text="Student Class Day:").grid(row=3, column=0, sticky='e')
        self.student_class_day = tk.Text(self, height=2, width=20)
        self.student_class_day.grid(row=3, column=1)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, columnspan=2)

        self.exit_button = tk.Button(self, text="Exit", command=self.destroy)
        self.exit_button.grid(row=5, column=0, columnspan=2)

    def submit(self):
        student_name = self.student_name.get("1.0", "end-1c")
        student_phone = self.student_phone.get("1.0", "end-1c")
        student_class_time = self.student_class_time.get("1.0", "end-1c")
        student_class_day = self.student_class_day.get("1.0", "end-1c")

        student_class_time = datetime.strptime(student_class_time, '%H:%M').time()

        add_student = student.Student(student_name, student_phone, student_class_time, student_class_day)

        database_obj = database.Database(add_student)
        database_obj.add_student()

        self.destroy()
class DeleteStudentWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs )

        self.title("Delete Student Info")
        self.geometry("500x200")

        tk.Label(self, text=f"Student Name:").grid(row=0, column=0, sticky='e')
        self.student_name = tk.Text(self, height=2, width=20)
        self.student_name.grid(row=0, column=1)

        self.submit_button = tk.Button(self, text="Submit", command=self.delete)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def delete(self):
        student_name = self.student_name.get("1.0", "end-1c")
        delete_student = student.Student(student_name)

        database_obj = database.Database(delete_student)
        database_obj.delete_student()

        self.destroy()
class ViewStudentWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("View Student Info")
        self.geometry("400x400")

        tk.Label(self, text=f"Student Name:").grid(row=0, column=0, sticky='e')
        self.student_name = tk.Text(self, height=2, width=20)
        self.student_name.grid(row=0, column=1)

        self.search_button = tk.Button(self, text="Submit", command=self.search_student)
        self.search_button.grid(row=4, column=0, columnspan=2)

    def search_student(self):
        student_name = self.student_name.get("1.0", "end-1c")
        search_name = student.Student(student_name)

        database_obj = database.Database(search_name)
        student_info = database_obj.view_student_info()

        view_window_obj = ViewInfoWindow(student_info)



class ViewInfoWindow(tk.Tk):
    def __init__(self, student_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Result")
        self.geometry("200x200")
        self.name = student_data[0]
        self.phone = student_data[1]
        self.class_time = student_data[2]
        self.class_day = student_data[3]
        tk.Label(self, text=f"Student Name: {self.name}").grid(row=0, column=0, sticky='e')
        tk.Label(self, text=f"Student Phone #: {self.phone}").grid(row=1, column=0, sticky='e')
        tk.Label(self, text=f"Student Class Time: {self.class_time}").grid(row=2, column=0, sticky='e')
        tk.Label(self, text=f"Student Class Day: {self.class_day}").grid(row=3, column=0, sticky='e')

        self.submit_button = tk.Button(self, text="Submit", command=self.destroy)
        self.submit_button.grid(row=4, column=0, columnspan=2)

