import pandas as pd
from Student import Student


# this method takes the filepath and reads each sheet from the excel gradebook
def read_file(path):
    gb = pd.read_excel(path)
    tests = pd.read_excel(path, sheet_name=1)
    quizzes = pd.read_excel(path, sheet_name=2)
    obs = pd.read_excel(path, sheet_name=3)
    emails = pd.read_excel(path, sheet_name=4)

    return [gb, tests, quizzes, obs, emails]  # returns an array of pd datatables for each sheet


# gradebook object that gets the assessments and their values, as well as creating a student list
class Gradebook:
    def __init__(self, path):
        self.path = path
        self.gradebook = read_file(path)  # array that contains the datatables from the spreadsheet

    # method to retrieve the names and mark values of each assessment
    def get_tests(self):
        t = self.gradebook[1]  # tests sheet from excel file
        t = t.iloc[:, 5:]  # removing the first 5 columns, which contain metadata
        names = []
        marks = []

        # for loop that iterates through the tests sheet by 3 columns, as there is a new assessment every 3 columns
        for i in range(0, t.shape[1], 3):
            names.append(t.columns[i])  # column header is the name of the assessment
            marks.append(t.iat[0, i])  # first row contains mark values

        return [names, marks]  # returns a 2d array containing assessment names and mark values

    # method that retrieves information about each student and returns an array of the class
    def get_students(self):
        gb = self.gradebook[0]  # summary sheet
        test = self.gradebook[1]  # tests sheet
        quiz = self.gradebook[2]  # quiz sheet
        obs = self.gradebook[3]  # obs/cons sheet
        emails = self.gradebook[4]  # emails sheet
        students = []

        for i in range(0, gb.shape[0]):  # for each row in the spreadsheet
            s = gb.iloc[[i]]  # student info in the corresponding row

            # locating and storing the row which contains the students information in the 4 other sheets
            t = test.loc[test['Unnamed: 0'] == s.iat[0, 0]]
            q = quiz.loc[quiz['Unnamed: 0'] == s.iat[0, 0]]
            o = obs.loc[obs['Unnamed: 0'] == s.iat[0, 0]]
            e = emails.loc[emails['Unnamed: 0'] == s.iat[0, 0]]

            # creating a new student object with the info and storing it in the array
            students.append(Student(s, t, q, o, e))

        return students
