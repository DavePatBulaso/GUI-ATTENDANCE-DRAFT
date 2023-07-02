import os
import tkinter
import re
from tkinter import messagebox
from datetime import datetime, timedelta


# Class for the Digital Attendance Tracking System
class AttendanceTracker:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("DATS (Digital Attendance Tracking System)")

        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        # Encloses all label fields
        self.user_attendance_frame = tkinter.LabelFrame(self.frame, text="Attendance Form", font=15)
        self.user_attendance_frame.grid(row=0, column=0, padx=20, pady=20)

        # First Name
        self.first_name_label = tkinter.Label(self.user_attendance_frame, text="First Name")
        self.first_name_label.grid(row=0, column=0)
        self.first_name_entry = tkinter.Entry(self.user_attendance_frame)
        self.first_name_entry.grid(row=0, column=1)

        # Last Name
        self.last_name_label = tkinter.Label(self.user_attendance_frame, text="Last Name")
        self.last_name_label.grid(row=1, column=0)
        self.last_name_entry = tkinter.Entry(self.user_attendance_frame)
        self.last_name_entry.grid(row=1, column=1)

        # Student Number
        self.sdt_num_label = tkinter.Label(self.user_attendance_frame, text="Student No.")
        self.sdt_num_label.grid(row=2, column=0)
        self.sdt_num_entry = tkinter.Entry(self.user_attendance_frame)
        self.sdt_num_entry.grid(row=2, column=1)

        for widget in self.user_attendance_frame.winfo_children():
            widget.grid_configure(padx=10, pady=3)

        # Button for Encoding the Data
        self.button = tkinter.Button(self.frame, text="Encode data", command=self.encode)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        self.check_absent_students()
        self.window.destroy()

    def encode(self):
        firstname = self.first_name_entry.get()
        lastname = self.last_name_entry.get()
        student_no = self.sdt_num_entry.get()
        checker1 = ValidateData(firstname, lastname, student_no)
        checker1.calldata()
        checker1.checker()

    def check_absent_students(self):
        attendance_log_file = f"attendance_log_{datetime.now().strftime('%Y-%m-%d')}.txt"
        masterlist_file = "masterlist.txt"
        absent_students = []

        with open(masterlist_file, "r") as masterlist:
            masterlist_students = set()
            for line in masterlist:
                match = re.search(r"(\d+)$", line)
                if match:
                    student_no = match.group(1)
                    masterlist_students.add(student_no)

            with open(attendance_log_file, "r") as attendance_log:
                attendance_students = set()
                for line in attendance_log:
                    match = re.search(r"Student No: (\d+)", line)
                    if match:
                        student_no = match.group(1)
                        attendance_students.add(student_no)

            absent_students = masterlist_students - attendance_students

        if absent_students:
            with open(attendance_log_file, "a") as attendance_log:
                attendance_log.write("\n--- Absent Students ---\n")
                for student_no in absent_students:
                    attendance_log.write(f"{student_no}\n")
            tkinter.messagebox.showinfo(
                title="Absent Students",
                message="Absent students have been appended to the attendance log.",
            )


# Class for checking the data inputted by the user.
class ValidateData:
    def __init__(self, firstname, lastname, student_no):
        self.stud_no_line = None
        self.lastname_line = None
        self.firstname_line = None
        self.firstname = firstname
        self.lastname = lastname
        self.student_no = student_no

    # Function that checks first name, last name, and student number.
    def calldata(self):
        with open("masterlist.txt", "r") as f:
            for line, row in enumerate(f.read().splitlines()):
                if re.findall('\\b' + re.escape(self.firstname) + '\\b', row):
                    self.firstname_line = line

        with open("masterlist.txt", "r") as f:
            for line, row in enumerate(f.read().splitlines()):
                if re.findall('\\b' + re.escape(self.lastname) + '\\b', row):
                    self.lastname_line = line

        with open("masterlist.txt", "r") as f:
            for line, row in enumerate(f.read().splitlines()):
                if re.findall('\\b' + re.escape(self.student_no) + '\\b', row):
                    self.stud_no_line = line

    # Function that checks all three possible outcomes.
    def checker(self):
        try:
            assert len(self.firstname) > 2
            if (self.firstname_line == self.lastname_line and self.firstname_line == self.lastname_line):
                tkinter.messagebox.showwarning(
                    title="VALIDATED!", message="You are now validated."
                )

                # Check for duplicate entry in attendance log
                attendance_log_file = f"attendance_log_{datetime.now().strftime('%Y-%m-%d')}.txt"

                if not os.path.isfile(attendance_log_file):
                    with open(attendance_log_file, "w") as file:
                        # Create an empty file if it doesn't exist yet
                        pass

                duplicate_entry = False
                with open(attendance_log_file, "r") as file:
                    for line in file:
                        if (
                                f"First Name: {self.firstname}," in line
                                and f"Last Name: {self.lastname}," in line
                                and f"Student No: {self.student_no}" in line
                        ):
                            duplicate_entry = True
                            break

                if duplicate_entry:
                    tkinter.messagebox.showwarning(
                        title="DUPLICATE ENTRY!",
                        message="You have already checked-in for today.",
                    )
                else:
                    # Append entry to attendance log
                    with open(attendance_log_file, "a") as file:
                        file.write(
                            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Check-In, First Name: {self.firstname}, "
                            f"Last Name: {self.lastname}, Student No: {self.student_no}\n"
                        )
                    tkinter.messagebox.showinfo(
                        title="SUCCESS!",
                        message="Your check-in has been recorded in the attendance log.",
                    )

            else:
                tkinter.messagebox.showwarning(
                    title="NOT VALIDATED!", message="You are not yet validated."
                )

        except AssertionError:
            tkinter.messagebox.showwarning(
                title="NOT VALIDATED!",
                message="Your value input cannot be found "
                        "inside the text file. (Check for spelling errors)",
            )
        except AttributeError:
            tkinter.messagebox.showwarning(
                title="NOT VALIDATED!",
                message="Your value input cannot be found "
                        "inside the text file. (Check for spelling errors)",
            )


attendance_tracker = AttendanceTracker()
