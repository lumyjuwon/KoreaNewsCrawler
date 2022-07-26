import csv
import platform
from korea_news_crawler.exceptions import *


class Writer(object):
    def __init__(self, category, article_category, date):
        self.start_year = date['start_year']
        self.start_month = f'0{date["start_month"]}' if len(str(date['start_month'])) == 1 else str(date['start_month'])
        self.start_day = f'0{date["start_day"]}' if len(str(date['start_day'])) == 1 else str(date['start_day'])
        self.end_year = date['end_year']
        self.end_month = f'0{date["end_month"]}' if len(str(date['end_month'])) == 1 else str(date['end_month'])
        self.end_day = f'0{date["end_day"]}' if len(str(date['end_day'])) == 1 else str(date['end_day'])
        self.file = None
        self.initialize_file(category, article_category)

        self.csv_writer = csv.writer(self.file)

    def initialize_file(self, category, article_category):
        output_path = f'../output'
        if os.path.exists(output_path) is not True:
            os.mkdir(output_path)

        file_name = f'{output_path}/{category}_{article_category}_{self.start_year}{self.start_month}{self.start_day}_{self.end_year}{self.end_month}{self.end_day}.csv'
        if os.path.isfile(file_name) and os.path.getsize(file_name) != 0:
            raise ExistFile(file_name)

        user_os = str(platform.system())
        if user_os == "Windows":
            self.file = open(file_name, 'w', encoding='euc-kr', newline='')
        # Other OS uses utf-8
        else:
            self.file = open(file_name, 'w', encoding='utf-8', newline='')

    def write_row(self, arg):
        self.csv_writer.writerow(arg)

    def close(self):
        self.file.close()
