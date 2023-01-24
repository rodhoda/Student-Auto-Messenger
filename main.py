# Student_Auto_Messenger

import csv
import pandas as pd
from twilio.rest import Client
import os


def user_interface():
    global choice
    exit_option = True

    print("Welcome!\n")

    while exit_option:
        choice = int(input(("\n1 - To create a file to manage your students\n"
                            "2 - To look at your file containing student info\n"
                            "3 - To add to an existing file\n"
                            "4 - Get the numbers from the file\n"
                            "5 - To send the sms message\n"
                            "6 - To delete a student from the file\n"
                            "7 - To find the information of a student\n"
                            "8 - Exit the program\n"
                            "Input: ")))
        if choice == 8:
            print("\nGoodbye!")
            exit_option = False

        elif 0 >= choice or choice > 8:
            print("This is not a valid value. Please choose a number from the menu listed.")

        elif choice != 8:
            day = input("Which day of the week would you like to create a file for? ")
            day = day.lower()
            file_name = '{}_tasks.csv'.format(day)

            if choice == 1 or choice == 3:
                create_and_add_file(choice, day, file_name)

            elif choice == 2:
                print(read_file(file_name), )

            elif choice == 4:
                print(get_by_column(file_name))

            elif choice == 5:
                send_sms(file_name)

            elif choice == 6:
                delete_from_file(file_name)

            elif choice == 7:
                print(find_row_using_name(day, file_name))
        else:
            print("Sorry! Please inputhe corresponding integer to the tasks from the menu.")


def create_and_add_file(choice, day, file_name):
    no_of_students = input("Please write the number of students you will be adding: ")

    if int(no_of_students) < 0 or int(no_of_students) > 50:
        print("This value is out of the bounds. Please choose a value between 1-49.")

    else:
        students = []
        for i in range(int(no_of_students)):
            student = input("Student name: ")
            while student.isdigit():
                student = input("Integers are not allowed. \nPlease try again: ")
            phone_num = input("Phone No.: ")
            class_time = input("Class time: ")
            class_duration = input("Class duration: ")
            students.append([])
            students[i] = [student, phone_num, class_time, class_duration]

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        if day in days:
            if choice == 1:
                if os.path.isfile(file_name):
                    add_or_not = input("This file already exists. "
                                       "Would you like to add this student in the existing file? Y/N ")
                    if add_or_not == 'Y':
                        with open(file_name, "a") as day_csv:
                            df = read_file(file_name)
                            for name in df["Name"]:
                                if name == student:
                                    print("This student already exists in the current file.")
                                    return
                            writer = csv.writer(day_csv)
                            writer.writerows(students)

                    elif add_or_not == 'N':
                        return
                else:
                    with open(file_name, "w") as day_csv:
                        writer = csv.writer(day_csv)
                        writer.writerows(students)
            elif choice == 3:
                with open(file_name, "a") as day_csv:
                    writer = csv.writer(day_csv)
                    writer.writerows(students)


def read_file(file_name):

    df = pd.read_csv(file_name, names=['Name', 'Phone number', 'Class time', 'Class duration'])

    if df.empty:
        print("file is empty")

    return df


def get_by_column(file_name):
    category_choice = input("Which category would you like to search with? Here are the choice: \n"
                            "'Name', 'Phone number','Class time','Class duration'\n")

    while category_choice not in ["Name", "Phone number", "Class time", "Class duration"]:
        category_choice = input("Please specifically write one of the choices of the list.\nInput: ")

    df = read_file(file_name)
    category = df[category_choice].tolist()
    if category_choice == "Phone number":
        category = ['+' + str(category) for category in category]

    return category


def send_sms(file_name):
    df = read_file(file_name)
    name = df['Name'].tolist()
    phone_num = df['Phone number'].tolist()
    class_time = df['Class time'].tolist()
    class_dur = df['Class duration'].tolist()

    account_sid = "ACd419297027367ec087249777f3ca2dac"
    auth_token = "6e96b1dd1b41d6b099ec5227fac0e390"

    client = Client(account_sid, auth_token)

    for i in range(len(phone_num)):

        client.messages.create(
            to=phone_num[i],
            from_="+12058581417",
            body="Hello,\nthis is a reminder that {} has a class at {} for {}".format(name[i], class_time[i],
                                                                                      class_dur[i])
        )


def delete_from_file(file_name):
    lines = []

    with open(file_name, 'r') as students:
        reader = csv.reader(students)
        student_name = input("What is the name of the student? ")
        while student_name.isdigit():
            student_name = input("Integers are not allowed. \nPlease try again: ")

        for row in reader:
            lines.append(row)
            for field in row:
                if field == student_name:
                    lines.remove(row)

    with open(file_name, 'w') as stud:
        confirm = input("Found the student! Are you sure you would like to remove them from the list? Y/N ")

        if confirm == 'Y':
            writer = csv.writer(stud)
            writer.writerows(lines)

        elif confirm == 'N':
            print("Action Cancelled.")

    df = pd.read_csv(file_name, names=['name', 'phone number', 'class time', 'duration']).set_index('name')

    if df.empty:
        print("checking")
        os.remove(file_name)


def find_row_using_name(day, file_name):
    lines = []
    student_name = input("What is the name of the student? ")

    with open(file_name, 'r') as students:
        reader = csv.reader(students)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == student_name:
                    return row
                else:
                    add_or_not = input("This student does not exist in the current file. "
                                       "Would you like to add them? Y/N ")
                    if add_or_not == 'Y':
                        create_and_add_file(3, day, file_name)
                        return
                    else:
                        return


if __name__ == "__main__":
    user_interface()
