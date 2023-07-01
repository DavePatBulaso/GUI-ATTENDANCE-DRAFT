import tkinter

def encode():
    firstname = first_name_entry.get()
    lastname = last_name_entry.get()
    sdtnum = sdt_num_entry.get()

    print(f"First name: {firstname}")
    print(f"Last name: {lastname}")
    print(f"Student No.: {sdtnum}")
    print(f"---------------------------------------------------")


window = tkinter.Tk()
window.title("DATS (Digital Attendance Tracking System)")

frame = tkinter.Frame(window)
frame.pack()

# Encloses all label fields
user_attendance_frame = tkinter.LabelFrame(frame, text="Attendance Form", font=15)
user_attendance_frame.grid(row=0, column=0, padx=20, pady=20)

# First Name
first_name_label = tkinter.Label(user_attendance_frame, text="First Name")
first_name_label.grid(row=0, column=0)
first_name_entry = tkinter.Entry(user_attendance_frame)
first_name_entry.grid(row=0, column=1)

# Last Name
last_name_label = tkinter.Label(user_attendance_frame, text="Last Name")
last_name_label.grid(row=1, column=0)
last_name_entry = tkinter.Entry(user_attendance_frame)
last_name_entry.grid(row=1, column=1)

# Student Number
sdt_num_label = tkinter.Label(user_attendance_frame, text="Student No.")
sdt_num_label.grid(row=2, column=0)
sdt_num_entry = tkinter.Entry(user_attendance_frame)
sdt_num_entry.grid(row=2, column=1)

for widget in user_attendance_frame.winfo_children():
    widget.grid_configure(padx=10, pady=3)

button = tkinter.Button(frame, text="Encode data", command= encode)
button.grid(row=1, column=0, padx=10, pady=10)


window.mainloop()
