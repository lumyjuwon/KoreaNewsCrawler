#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Process
from korea_news_crawler.exceptions import *
from korea_news_crawler.articleparser import ArticleParser
from korea_news_crawler.writer import Writer
import os
import platform
import calendar
import requests
import re
from newspaper import Article

        
        
class ArticleCrawler(object):
    def __init__(self):
        choosen_categories = self.get_catergory()
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104, 'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.date = {'start_year': 0, 'start_month': 0, 'end_year': 0, 'end_month': 0}
        self.get_date()
        self.set_date_range(self.date['start_year'],self.date['start_month'],self.date['end_year'],self.date['end_month'])
        self.user_operating_system = str(platform.system())
        self.set_category(choosen_categories)
        self.keyword = self.get_keyword()

    def get_catergory(self):
        print("카테고리 : 정치 , 경제 , 사회 , 생활문화 , 세계 , IT과학 , 오피니언, 연합뉴스속보")
        print("원하는 카테고리를 입력 하세요(공백으로 구분) : ",end ='')
        choosen_categories = input()
        choosen_list = choosen_categories.split(' ')
        print(choosen_list)
        return choosen_list
    
    def get_date(self):
        print("크롤링을 원하는 날짜 기간을 입력하세요 ")
        for keys in self.date.keys() :
            print(keys + " : ",end= '')
            get_date = int(input())
            self.date[keys] = get_date
            
##########################################################
    def get_keyword(self):
        keyword = 'initvalue'
        ynkeyword = input("기사 제목 키워드 찾기 기능을 사용하시겠습니까? (y/n) :")
        if ynkeyword == "n" or ynkeyword == "N":
            return keyword
        elif ynkeyword == "y" or ynkeyword == "Y":
            keyword = input("원하는 키워드를 입력해주세요 :")
            return keyword
        else:
            print("invalid input")
            return keyword
##########################################################                  

    def set_category(self, args):
        for key in args:
            if self.categories.get(key) is None and key != '연합뉴스속보':
                raise InvalidCategory(key)
        self.selected_categories = args

    def set_date_range(self, start_year, start_month, end_year, end_month):
        args = [start_year, start_month, end_year, end_month]
        if start_year > end_year:
            raise InvalidYear(start_year, end_year)
        if start_month < 1 or start_month > 12:
            raise InvalidMonth(start_month)
        if end_month < 1 or end_month > 12:
            raise InvalidMonth(end_month)
        if start_year == end_year and start_month > end_month:
            raise OverbalanceMonth(start_month, end_month)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    @staticmethod
    def make_news_page_url(category_url, start_year, end_year, start_month, end_month):
        made_urls = []
        for year in range(start_year, end_year + 1):
            print(year)
            if start_year == end_year:
                year_startmonth = start_month
                year_endmonth = end_month
            else:
                if year == start_year:
                    year_startmonth = start_month
                    year_endmonth = 12
                elif year == end_year:
                    year_startmonth = 1
                    year_endmonth = end_month
                else:
                    year_startmonth = 1
                    year_endmonth = 12
            
            for month in range(year_startmonth, year_endmonth + 1):
                for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)
                        
                    # 날짜별로 Page Url 생성
                    url = category_url + str(year) + str(month) + str(month_day)
                    # totalpage는 네이버 페이지 구조를 이용해서 page=10000으로 지정해 totalpage를 알아냄
                    # page=10000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨 (Redirect)
                    totalpage = ArticleParser.find_news_totalpage(url + "&page=10000")
                    for page in range(1, totalpage + 1):
                        made_urls.append(url + "&page=" + str(page))
        return made_urls

    @staticmethod
    def get_url_data(url, max_tries=10):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
                return requests.get(url, headers=headers1)
            except requests.exceptions:
                sleep(60)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))    

        writer = Writer(category_name=category_name, date=self.date)
        # 기사 URL 형식
        if (category_name == "연합뉴스속보"):
            url = "http://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y" \
                  + "&date="

        else:
            url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
                self.categories.get(category_name)) + "&date="

        # start_year년 start_month월 ~ end_year의 end_month 날짜까지 기사를 수집합니다.
        day_urls = self.make_news_page_url(url, self.date['start_year'], self.date['end_year'], self.date['start_month'], self.date['end_month'])
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in day_urls:
            print(URL)
            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = self.get_url_data(URL)
            document = BeautifulSoup(request.content, 'html.parser')
            
            # html - newsflash_body - type06_headline, type06
            # 각 페이지에 있는 기사들 가져오기
            if (category_name == "연합뉴스속보"):
                post_temp = document.select('.newsflash_body .type02 li ')

            else:
                post_temp = document.select('.newsflash_body .type06_headline li dl')
                post_temp.extend(document.select('.newsflash_body .type06 li dl'))
           
            # 각 페이지에 있는 기사들의 url 저장
            post = []
            headlines = []
            companys = []

            
            for line in post_temp:
                post.append(line.a.get('href')) # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음
                try:
                    companys.append(line.find('span', class_="writing").text)
                except:
                    companys.append("err")
                try:
                    h = line.find_all('a')
                    if len(h) > 1:
                        headlines.append(h[1].text)
                    elif len(h) == 1:
                        headlines.append(h[0].text)
                    else:
                        headlines.append("err")
                except:
                    headlines.append("err")
            del post_temp
        
            
            print(len(post))

            for i in range(len(post)):  # 기사 URL
                # 크롤링 대기 시간
                print(i)
                sleep(0.01)
                content_url = post[i]
                
                # 기사 HTML 가져옴
                try:
                    article = Article(content_url, language='ko')
                    article.download()
                    article.parse()
                    text_sentence = article.text.strip()
                    text_company = companys[i]
                    text_headline = headlines[i].strip()
        ######################################################################
                    if self.keyword == 'initvalue':
                        wcsv = writer.get_writer_csv()
                        wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])
                    else:
                        headline_to_words = text_headline.split()
                        if headline_to_words.index(self.keyword) >= 0:
                            wcsv = writer.get_writer_csv()
                            wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])
        ######################################################################

                            
                except Exception as err:
                    print(err)
        
        writer.close()
        return        

    def start(self, isMultiProc):
        # MultiProcess 크롤링 시작
        
        for category_name in self.selected_categories:
            if isMultiProc:
                proc = Process(target=self.crawling, args=(category_name,))
                proc.start()
            else:
                self.crawling(category_name)


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    #Crawler.set_category("생활문화", "IT과학")
    #Crawler.set_date_range(2017, 1, 2018, 4)
    Crawler.start()

