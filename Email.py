import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# method that returns a boolean which decides whether the email goes to parents or not
def to_parents(s, include):
    for i in include:  # for each test chosen to be in the email
        if s.tests[0][i] <= 70 and s.tests[0][i] != -1:  # if the student got less than 70, email parents
            return True

    if len(s.tests[1]) >= 3:  # if student has 3 or more missing assignments, email parents
        return True

    return False


# method that takes student, tests, and assessment selection and builds the email message
def build_message(s, t, include):
    # overall average is included in every email
    message = "Hi {},\n\nYour overall mark in the course is {}%.\n".format(s.first, round(s.mark))

    # for each assessment that was selected, add the mark
    for i in include:
        if s.tests[0][i] == -1:  # if there is no grade or an invalid grade in the gradebook
            message += "It appears you have not written {}.\n".format(t[0][i])
        else:
            message += "On {}, you scored {} out of {}, which is {}%.\n".format(
                t[0][i], s.tests[0][i], int(t[1][i]), round((s.tests[0][i] / t[1][i]) * 100, 1))

    # missing assignments
    if len(s.tests[1]) >= 1:  # if the missing sheet contains anything
        message += "\nThe following assignments/mastery checks are missing or have not been passed:\n"
        for a in s.tests[1]:
            message += "{}\n".format(a)
    else:
        message += "\nYou have no missing assignments or mastery checks.\n"

    # signature
    message += "\nMr. Hodal"
    return message


# method that connects with the smtp server and sends the email
def send_email(to, subject, body):
    # authentication with the email server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("HSCLunchAPI", "REDACTED")

    # building the email object
    email = MIMEMultipart()
    email['From'] = "HSCLunchAPI@gmail.com"

    if isinstance(to, str):
        email['To'] = to  # if the email is just a single string
    else:
        email['To'] = ", ".join(to)  # joining the list of emails

    email['Subject'] = subject

    # adding the body message and sending the email
    email.attach(MIMEText(body, 'plain'))
    s.send_message(email)


# simple object that takes a student object, the tests array, and the assessments to include and creates an email
class Email:
    def __init__(self, s, t, include):
        subject = "Calculus Grade Update"  # subject of the message, can change
        message = build_message(s, t, include)

        if to_parents(s, include):
            send_email(s.email, subject, message)
        else:
            send_email(s.email[0], subject, message)
