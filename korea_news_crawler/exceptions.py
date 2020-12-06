#처리 가능한 값보다 큰 값이 나왔을 때
class OverFlow(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is overflow."

    def __str__(self):
        return str(str(self.args) + self.message)
    

#처리 가능한 값보다 작은 값이 나왔을 때
class UnderFlow(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is underflow."

    def __str__(self):
        return str(str(self.args) + self.message)

#변수가 올바르지 않을 때
class InvalidArgs(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is Invalid Arguments"

    def __str__(self):
        return str(self.args + self.message)

#카테고리가 올바르지 않을 때
class InvalidCategory(Exception):
    def __init__(self, category):
        self.category = category
        self.message = " is Invalid Category."

    def __str__(self):
        return str(self.category + self.message)

#년도가 올바르지 않을 때
class InvalidYear(Exception):
    def __init__(self, startyear, endyear):
        self.startyear = startyear
        self.endyear = endyear
        self.message = str(startyear) + "(startyear) is bigger than " + str(self.endyear) +"(endyear)"

    def __str__(self):
        return str(self.message)

#달이 올바르지 않을 때
class InvalidMonth(Exception):
    def __init__(self, month):
        self.month = month
        self.message = str(month) + " is an invalid month"

    def __str__(self):
        return str(self.message)

#시작 달과 끝나는 달이 올바르지 않을 때
class OverbalanceMonth(Exception):
    def __init__(self, start_month, end_month):
        self.start_month = start_month
        self.end_month = end_month
        self.message = "start_month(" + str(self.start_month) + ") is an overbalance with end_month" + "(" + str(self.end_month) + ")"

    def __str__(self):
        return str(self.message)

#실행시간이 너무 길어서 데이터를 얻을 수 없을 때
class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return str(self.message)
