import tkinter as tk
from tkinter import filedialog, IntVar, Checkbutton, CENTER
from Gradebook import Gradebook
from Email import Email


# this method takes the file path from user input and formats it into a gradebook
def import_gradebook():
    # hiding the import button
    dialog_button.place_forget()
    # retrieving the file path and creating a gradebook object
    gradebook = Gradebook(filedialog.askopenfilename())
    tests = gradebook.get_tests()  # holds the assessment names and mark values
    selection = []  # array of 0s and 1s for whether to include assessment in email
    root.geometry('')  # resetting the size of the window
    root.minsize(width='225', height='200')

    for t in tests[0]:  # this loop creates checkboxes for each assessment name and adds their values to the array
        var = IntVar()
        chk = Checkbutton(text=t, variable=var)
        chk.pack()
        selection.append(var)

    # send button that runs the method to collect the checkbox selections
    send_button = tk.Button(text='Send', command=lambda: get_selection(gradebook, selection))
    send_button.pack()


# method that reads the checkbox selections and sends the emails
def get_selection(gradebook, selection):
    include = []  # array that has assessment indexes added to it if checkboxes are ticked

    for i in range(0, len(selection)):  # loop that runs for as many assessments there are
        if selection[i].get() == 1:  # if the checkbox is ticked, add the index
            include.append(i)

    send_emails(gradebook, include)


# method that takes grades and list of assessments to include and sends the email
def send_emails(gradebook, include):
    students = gradebook.get_students()
    tests = gradebook.get_tests()

    for s in students:  # for each student, create an email object
        Email(s, tests, include)

    root.destroy()  # closes the window


# GUI and import button setup
root = tk.Tk()
root.geometry('200x200')
dialog_button = tk.Button(text='Select a file to import', command=import_gradebook)
dialog_button.place(relx=0.5, rely=0.5, anchor=CENTER)
root.mainloop()
