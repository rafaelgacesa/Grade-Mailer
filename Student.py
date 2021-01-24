# method to retrieve all emails stored for a student
def get_email(e):
    emails = e.iloc[:, 2:]  # removing metadata
    email_list = []

    # iterates through columns
    for i in range(0, emails.shape[1]):
        if emails.iat[0, i] == emails.iat[0, i]:  # filtering out blank cells (NaN)
            email_list.append(emails.iat[0, i])

    return email_list


# method that retrieves a students test scores from the tests sheet
def get_test_scores(t):
    marks = []
    scores = t.iloc[:, 5:]  # removing the first 5 columns which store metadata

    # for loop that iterates through the tests sheet by 3 columns, as a test mark is stored every 3 columns
    for i in range(0, scores.shape[1], 3):
        if scores.iat[0, i] == scores.iat[0, i] and scores.iat[0, i] != 0:
            marks.append(scores.iat[0, i])
        else:
            marks.append(-1)  # if the mark is invalid, a -1 is added

    return marks


# method that retrieves assignments/obs activities a student has not completed
def get_missing(q, o):
    # removing the first 17 columns which contain metadata
    q = q.iloc[:, 17:]
    o = o.iloc[:, 17:]
    missing = []

    # loop that cycles through each cell in the row and checks for characters or 0
    for i in range(0, q.shape[1]):
        if (str(q.iat[0, i]).isalpha() and q.iat[0, i] == q.iat[0, i]) or q.iat[0, i] == 0:
            missing.append(q.columns[i])

    # same thing, but for obs/cons
    for i in range(0, o.shape[1]):
        if (str(o.iat[0, i]).isalpha() and o.iat[0, i] == o.iat[0, i]) or o.iat[0, i] == 0:
            missing.append(o.columns[i])

    return missing


# object that stores all of the information about a student, including name, marks, email, etc.
class Student:
    def __init__(self, info, t, q, o, e):
        # extracting values from the pd data series
        self.last = info.iat[0, 0]  # eg. last name is stored in top left cell
        self.first = info.iat[0, 1]
        self.mark = info.iat[0, 2]
        self.tests = get_test_scores(t)  # getting the array of test scores
        self.tests = [self.tests, get_missing(q, o)]
        self.email = get_email(e)

    # debug method, prints a statement
    def __str__(self):
        return "{} {} has a mark of {}".format(self.first, self.last, round(self.mark))
