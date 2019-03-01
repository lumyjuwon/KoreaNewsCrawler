#!/usr/bin/env python
# -*- coding: euc-kr -*-

from time import sleep
from bs4 import BeautifulSoup
from exceptions import *
from multiprocessing import Process
import os
import calendar
import requests
import csv
import re


class ArticleCrawler:
    def __init__(self):
        self.category = {'politics': 100, 'economy': 101, 'society': 102, 'culture': 103, 'global': 104, 'IT/science': 105}
        self.selected_category = []
        self.date = {'startyear': 0, 'endyear': 0, 'endmonth': 0}

    def set_category(self, *args):
        for key in args:
            if self.category.get(key) is None:
                raise InvalidCategory(key)
            else:
                self.selected_category = args

    def set_date_range(self, startyear, endyear, endmonth):
        args = [startyear, endyear, endmonth]
        if startyear > endyear:
            raise InvalidYear(startyear, endyear)
        if endmonth < 1 or endmonth > 12:
            raise InvalidMonth(endmonth)
        for key, date in zip(self.date, args):
            self.date[key] = date
        print(self.date)

    def clearcontent(self, text):
        special_symbol_removed_content = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        end_phrase_removed_content = re.sub(
            '본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가fuctio flashremoveCallback|tt|t|앵커 멘트|xa0', '',
            special_symbol_removed_content)
        blank_removed_content = end_phrase_removed_content.strip().replace('   ', '')  # 공백 에러 삭제
        reversed_content = ''.join(reversed(blank_removed_content))  # 기사 내용을 reverse 한다.
        content = ''
        for i in range(0, len(blank_removed_content)):
            if reversed_content[
               i:i + 2] == '.다':  # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지운다.
                content = ''.join(reversed(reversed_content[i:]))
                break
        return content

    def clearheadline(self, text):
        special_symbol_removed_headline = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        return special_symbol_removed_headline

    def find_news_totalpage(self, url):
        try:
            totlapage_url = url
            request_content = requests.get(totlapage_url)
            document_content = BeautifulSoup(request_content.content, 'html.parser')
            headline_tag = document_content.find('div', {'class': 'paging'}).find('strong')
            regex = re.compile(r'<strong>(?P<num>\d+)')
            match = regex.findall(str(headline_tag))
            return int(match[0])
        except Exception:
            return 0

    def make_news_page_url(self, category_url, startyear, lastyear, startmonth, lastmonth):
        maked_url = []
        final_startmonth = startmonth
        final_lastmonth = lastmonth
        for year in range(startyear, lastyear + 1):
            if year != lastyear:
                startmonth = 1
                lastmonth = 12
            else:
                startmonth = final_startmonth
                lastmonth = final_lastmonth
            for month in range(startmonth, lastmonth + 1):
                for month_day in range(1, calendar.monthrange(year, month)[1] + 1):
                    url = category_url
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(month_day)) == 1:
                        month_day = "0" + str(month_day)
                    url = url + str(year) + str(month) + str(month_day)
                    final_url = url  # page 날짜 정보만 있고 page 정보가 없는 url 임시 저장
                    totalpage = self.find_news_totalpage(
                        final_url + "&page=1000")  # totalpage는 네이버 페이지 구조를 이용해서 page=1000으로 지정해 totalpage를 알아냄 ( page=1000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨)
                    for page in range(1, totalpage + 1):
                        url = final_url  # url page 초기화
                        url = url + "&page=" + str(page)
                        maked_url.append(url)
        return maked_url

    def parse(self, category_name):
        print(category_name + " pid: " + str(os.getpid()))

        file = open('Article_' + category_name + '.csv', 'w', encoding='euc_kr', newline='')
        wcsv = csv.writer(file)

        url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + str(
            self.category.get(category_name)) + "&date="
        final_urlday = self.make_news_page_url(url, self.date['startyear'], self.date['endyear'], 1, self.date[
            'endmonth'])  # startyear년 1월 ~ endyear의 endmonth 날짜까지 기사를 수집합니다.
        print(category_name + " Urls are generated")
        print("The crawler starts")

        for URL in final_urlday:

            regex = re.compile("date=(\d+)")
            news_date = regex.findall(URL)[0]

            request = requests.get(URL)
            document = BeautifulSoup(request.content, 'html.parser')
            tag_document = document.find_all('dt', {'class': 'photo'})

            post = []
            for tag in tag_document:
                post.append(tag.a.get('href'))  # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음

            for content_url in post:  # 기사 URL
                sleep(0.01)
                request_content = requests.get(content_url)
                document_content = BeautifulSoup(request_content.content, 'html.parser')

                try:
                    tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                    text_headline = ''  # 뉴스 기사 제목 초기화
                    text_headline = text_headline + self.clearheadline(str(tag_headline[0].find_all(text=True)))
                    if not text_headline:  # 공백일 경우 기사 제외 처리
                        continue

                    tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                    text_sentence = ''  # 뉴스 기사 본문 초기화
                    text_sentence = text_sentence + self.clearcontent(str(tag_content[0].find_all(text=True)))
                    if not text_sentence:  # 공백일 경우 기사 제외 처리
                        continue

                    tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                    text_company = ''  # 언론사 초기화
                    text_company = text_company + str(tag_company[0].get('content'))
                    if not text_company:  # 공백일 경우 기사 제외 처리
                        continue

                    wcsv.writerow([news_date, category_name, text_company, text_headline, text_sentence, content_url])

                except Exception as ex:  # UnicodeEncodeError ..
                    print(ex)
                    pass
        file.close()

    def start(self):
        for category_name in self.selected_category:
            proc = Process(target=self.parse, args=(category_name,))
            proc.start()


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category("politics", "economy")  # 정치, 경제, 생활문화, IT과학, 사회 카테고리 사용 가능
    Crawler.set_date_range(2017, 2018, 4)  # 2017년 1월부터 2018년 4월까지 크롤링 시작
    Crawler.start()
