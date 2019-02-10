class OverFlow(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is overflow."

    def __str__(self):
        return str(str(self.args) + self.message)


class UnderFlow(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is underflow."

    def __str__(self):
        return str(str(self.args) + self.message)


class InvalidArgs(Exception):
    def __init__(self, args):
        self.args = args
        self.message = " is not Invalid Arguments"

    def __str__(self):
        return str(self.args + self.message)


class InvalidCategory(Exception):
    def __init__(self, category):
        self.category = category
        self.message = " is not valid."

    def __str__(self):
        return str(self.category + self.message)


class InvalidYear(Exception):
    def __init__(self, startyear, endyear):
        self.startyear = startyear
        self.endyear = endyear
        self.message = str(startyear) + "(startyear) is bigger than " + str(self.endyear) +"(endyear)"

    def __str__(self):
        return str(self.message)


class InvalidMonth(Exception):
    def __init__(self, month):
        self.month = month
        self.message = str(month) + " is an invalid month"

    def __str__(self):
        return str(self.message)
