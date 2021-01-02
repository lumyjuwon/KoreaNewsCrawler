import calendar
import csv
import requests
import re
import json
from bs4 import BeautifulSoup
from time import sleep
from multiprocessing import Process
from korea_news_crawler.exceptions import *
from korea_news_crawler.writer import Writer
#from korea_news_crawler.writer import Writer


class SportCrawler:
    def __init__(self):
        self.category = {'한국야구': "kbaseball", '해외야구': "wbaseball", '해외축구': "wfootball",
                         '한국축구': "kfootball", '농구': "basketball", '배구': "volleyball", '일반 스포츠': "general",
                         'e스포츠': "esports",
                         'korea baseball': "kbaseball", 'world baseball': "wbaseball", 'world football': "wfootball",
                         'korea football': "kfootball", 'basketball': "basketball", 'volleyball': "volleyball",
                         'general sports': "general",
                         'e-sports': "esports"
                         }
        self.selected_category = []
        self.selected_url_category = []
        self.date = {'start_year': 0, 'start_month': 0, 'end_year': 0, 'end_month': 0}

    def get_total_page(self, url):
        totalpage_url = f'{url}&page=10000'
        request_content = requests.get(totalpage_url,headers={'User-Agent': 'Mozilla/5.0'})
        page_number = re.findall('\"totalPages\":(.*)}', request_content.text)
        return int(page_number[0])

    def content(self, html_document, url_label):
        content_match = []
        Tag = html_document.find_all('script', {'type': 'text/javascript'})
        Tag_ = re.sub(',"officeName', '\nofficeName', str(Tag))
        regex = re.compile('oid":"(?P<oid>\d+)","aid":"(?P<aid>\d+)"')
        content = regex.findall(Tag_)
        for oid_aid in content:
            maked_url = "https://sports.news.naver.com/" + url_label + "/news/read.nhn?oid=" + oid_aid[0] + "&aid=" + \
                        oid_aid[1]
            content_match.append(maked_url)
        return content_match

    def clear_content(self, text):
        remove_special = re.sub('[∙©\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        remove_author = re.sub('\w\w\w 기자', '', remove_special)
        remove_flash_error = re.sub('본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가fuctio flashremoveCallback|tt|t|앵커 멘트|xa0', '', remove_author)
        # 공백 에러 삭제
        remove_strip = remove_flash_error.strip().replace('   ', '')
        # 기사 내용을 reverse 한다.
        reverse_content = ''.join(reversed(remove_strip))
        cleared_content = ''
        for i in range(0, len(remove_strip)):
            # 기사가 reverse 되었기에  ".다"로 기사가 마무리 되므로, 이를 탐색하여 불필요한 정보를 모두 지운다.
            # 이 매커니즘에 의해 영문 기사가 완전히 나오지 않는 이슈가 있습니다... edge case가 적다면  '.다'를 '.'으로바꾸는 편이 나아보입니다.
           if reverse_content[i:i + 2] == '.다':
                cleared_content = ''.join(reversed(reverse_content[i:]))
                break
        cleared_content = re.sub('if deployPhase(.*)displayRMCPlayer', '', cleared_content)
        return cleared_content

    def clear_headline(self, text):
        first = re.sub('[∙©\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        return first

    def make_sport_page_url(self, input_url, start_year, last_year, start_month, last_month):
        urls = []
        for year in range(start_year, last_year + 1):
            target_start_month = start_month
            target_last_month = last_month

            if year != last_year:
                target_start_month = 1
                target_last_month = 12
            else:
                target_start_month = start_month
                target_last_month = last_month

            for month in range(target_start_month, target_last_month + 1):
                for day in range(1, calendar.monthrange(year, month)[1] + 1):
                    if len(str(month)) == 1:
                        month = "0" + str(month)
                    if len(str(day)) == 1:
                        day = "0" + str(day)
                    url = f'{input_url}{year}{month}{day}'
                    # page 날짜 정보만 있고 page 정보가 없는 url 임시 저장
                    final_url = f'${input_url}{year}{month}{day}'

                    # TotalPage 확인
                    total_page = self.get_total_page(final_url)
                    for page in range(1, total_page + 1):
                        # url page 초기화
                        url = f'{final_url}&page={page}'
                        # [[page1,page2,page3 ....]
                        urls.append(url)
        return urls

    def crawling(self, category_name):
        writer = Writer(category='Sport', article_category=category_name, date=self.date)
        url_category = [self.category[category_name]]
        category = [category_name]



        # URL 카테고리. Multiprocessing시 어차피 1번 도는거라 refactoring할 필요 있어보임
        for url_label in url_category:
            # URL 인덱스와 category 인덱스가 일치할 경우 그 값도 일치
            category = category[url_category.index(url_label)]
            url = f'https://sports.news.naver.com/{url_label}/news/list.nhn?isphoto=N&view=photo&date='
            final_url_day = self.make_sport_page_url(url, self.date['start_year'],
                                                    self.date['end_year'], self.date['start_month'], self.date['end_month'])
            print("succeed making url")
            print("crawler starts")
            if len(str(self.date['start_month'])) == 2:
                start_month = str(self.date['start_month'])
            else:
                start_month = '0' + str(self.date['start_month'])

            if len(str(self.date['end_month'])) == 2:
                end_month = str(self.date['end_month'])
            else:
                end_month = '0' + str(self.date['end_month'])

            # category Year Month Data Page 처리 된 URL
            for list_page in final_url_day:
                title_script = ''
                office_name_script = ''
                time_script = ''
                matched_content = ''

                # 제목 / URL
                request_content = requests.get(list_page, headers={'User-Agent': 'Mozilla/5.0'})
                content_dict = json.loads(request_content.text)
                # 이는 크롤링에 사용

                hef_script = ''

                for contents in content_dict["list"]:
                    oid = contents['oid']
                    aid = contents['aid']
                    title_script = contents['title']
                    time_script = contents['datetime']
                    hef_script = "https://sports.news.naver.com/news.nhn?oid=" + oid + "&aid=" + aid
                    office_name_script = contents['officeName']
                    sleep(0.01)
                    content_request_content = requests.get(hef_script, headers={'User-Agent': 'Mozilla/5.0'})
                    content_document_content = BeautifulSoup(content_request_content.content, 'html.parser')
                    content_tag_content = content_document_content.find_all('div', {'class': 'news_end'},
                                                                            {'id': 'newsEndContents'})
                    # 뉴스 기사 본문 내용 초기화
                    text_sentence = ''

                    try:
                        text_sentence = text_sentence + str(content_tag_content[0].find_all(text=True))
                        matched_content = self.clear_content(text_sentence)
                        writer.write_row([time_script, category, office_name_script, self.clear_headline(title_script),
                                          matched_content,
                                          hef_script])
                    except:
                        pass
            writer.close()

    def set_category(self, *args):
        for key in args:
            if self.category.get(key) is None:
                raise InvalidCategory(key)
        self.selected_category = args
        for selected in self.selected_category:
            self.selected_url_category.append(self.category[selected])

    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_category:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()

    def set_date_range(self, start_year, start_month, end_year, end_month):
        self.date['start_year'] = start_year
        self.date['start_month'] = start_month
        self.date['end_year'] = end_year
        self.date['end_month'] = end_month


# Main
if __name__ == "__main__":
    Spt_crawler = SportCrawler()
    Spt_crawler.set_category('한국야구','한국축구')
    Spt_crawler.set_date_range(2020, 12, 2020, 12)
    Spt_crawler.start()
