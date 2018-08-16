#!/usr/bin/env python
# -*- coding: euc-kr -*-

import calendar
import requests
from time import sleep
from bs4 import BeautifulSoup
import csv
import re

def Clearcontent(text):
    first = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]','', text)
    second = re.sub('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가fuctio flashremoveCallback|tt|t|앵커 멘트|xa0', '', first)
    Third = second.strip().replace('   ', '')  # 공백 에러 삭제
    Four = ''.join(reversed(Third))  # 기사 내용을 reverse 한다.
    content = ''
    for i in range(0, len(Third)):
        if Four[i:i+2] == '.다':  # reverse 된 기사 내용중, ".다"로 끝나는 경우 기사 내용이 끝난 것이기 때문에 기사 내용이 끝난 후의 광고, 기자 등의 정보는 다 지운다.
            content = ''.join(reversed(Four[i:]))
            break
    return content

def Clearheadline(text):
    first = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
    return first

def html_totalpage(url):
    totlapage_url = url
    request_content = requests.get(totlapage_url)
    document_content = BeautifulSoup(request_content.content, 'html.parser')
    Tag_headline = document_content.find('div', {'class': 'paging'}).find('strong')
    regex = re.compile(r'<strong>(?P<num>\d+)')
    match = regex.findall(str(Tag_headline))
    return int(match[0])

def Make_url(URL, startyear, lastyear, startmonth, lastmonth):
    Maked_url = []
    final_startmonth = startmonth
    final_lastmonth = lastmonth
    for year in range(startyear, lastyear + 1):
        if year != lastyear:
            startmonth = 1
            lastmonth = 12
        else:
            startmonth = final_startmonth
            lastmonth = final_lastmonth
        for Month in range(startmonth, lastmonth + 1):
            for Month_Day in range(1, calendar.monthrange(year, Month)[1] + 1):
                url = URL
                if len(str(Month)) == 1:
                    Month = "0" + str(Month)
                if len(str(Month_Day)) == 1:
                    Month_Day = "0" + str(Month_Day)
                url = url + str(year) + str(Month) + str(Month_Day)
                final_url = url  # page 날짜 정보만 있고 page 정보가 없는 url 임시 저장
                totalpage = html_totalpage(final_url+"&page=1000") # totalpage는 네이버 페이지 구조를 이용해서 page=1000으로 지정해 totalpage를 알아냄 ( page=1000을 입력할 경우 페이지가 존재하지 않기 때문에 page=totalpage로 이동 됨)
                for page in range(1, totalpage + 1):
                    url = final_url # url page 초기화
                    url = url + "&page=" + str(page)
                    Maked_url.append(url)
    return Maked_url


# Main
url_list = [100, 101,102, 103, 104, 105]
Category = ["정치", "경제" "사회", "생활문화", "세계", "IT과학"]

for url_num in url_list:  # URL 카테고리
    category = Category[url_list.index(url_num)]  # URL 인덱스와 Category 인덱스가 일치할 경우 그 값도 일치
    file = open('Article_' + category + '.csv', 'w', encoding='euc-kr', newline='')
    wcsv = csv.writer(file)

    url = "http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" +str(url_num)+"&date="
    final_urlday = Make_url(url, 2017, 2018, 1, 6) # 2017년 1월 ~ 2018년 6월 마지막 날까지 기사를 수집합니다.
    print("url success")

    for URL in final_urlday:
        request = requests.get(URL)
        document = BeautifulSoup(request.content, 'html.parser')
        Tag = document.find_all('dt', {'class': 'photo'})

        post = []
        for tag in Tag:
            post.append(tag.a.get('href'))  # 해당되는 page에서 모든 기사들의 URL을 post 리스트에 넣음

        for content_url in post:  # 기사 URL
            sleep(0.01)
            request_content = requests.get(content_url)
            document_content = BeautifulSoup(request_content.content, 'html.parser')

            try:
                Tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                text_headline = ''  # 뉴스 기사 제목 초기화
                text_headline = text_headline + Clearheadline(str(Tag_headline[0].find_all(text=True)))
                if not text_headline:  # 공백일 경우 기사 제외 처리
                    continue

                Tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                text_sentence = ''  # 뉴스 기사 본문 초기화
                text_sentence = text_sentence + Clearcontent(str(Tag_content[0].find_all(text=True)))
                if not text_headline: # 공백일 경우 기사 제외 처리
                    continue

                Tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                text_company = ''  # 언론사 초기화
                text_company = text_company + str(Tag_company[0].get('content'))
                if not text_headline: # 공백일 경우 기사 제외 처리
                    continue

                wcsv.writerow([text_headline, text_sentence, text_company, category])

            except:  # UnicodeEncodeError ..
                pass
    file.close()
