import os

# 처리 가능한 값보다 큰 값이 나왔을 때
class OverFlow(Exception):
    def __init__(self, args):
        self.message = f'{args} is overflow'

    def __str__(self):
        return self.message
    

# 처리 가능한 값보다 작은 값이 나왔을 때
class UnderFlow(Exception):
    def __init__(self, args):
        self.message = f'{args} is underflow'

    def __str__(self):
        return self.message


# 변수가 올바르지 않을 때
class InvalidArgs(Exception):
    def __init__(self, args):
        self.message = f'{args} is Invalid Arguments'

    def __str__(self):
        return self.message


# 카테고리가 올바르지 않을 때
class InvalidCategory(Exception):
    def __init__(self, category):
        self.message = f'{category} is Invalid Category.'

    def __str__(self):
        return self.message


# 년도가 올바르지 않을 때
class InvalidYear(Exception):
    def __init__(self, start_year, end_year):
        self.message = f'{start_year}(start year) is bigger than {end_year}(end year)'

    def __str__(self):
        return str(self.message)


# 달이 올바르지 않을 때
class InvalidMonth(Exception):
    def __init__(self, month):
        self.message = f'{month} is an invalid month'

    def __str__(self):
        return self.message


# 시작 달과 끝나는 달이 올바르지 않을 때
class OverbalanceMonth(Exception):
    def __init__(self, start_month, end_month):
        self.message = f'{start_month}(start month) is an overbalance with {end_month}(end month)'

    def __str__(self):
        return self.message


# 실행시간이 너무 길어서 데이터를 얻을 수 없을 때
class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return self.message


# 존재하는 파일
class ExistFile(Exception):
    def __init__(self, path):
        absolute_path = os.path.abspath(path)
        self.message = f'{absolute_path} already exist'

    def __str__(self):
        return self.message
