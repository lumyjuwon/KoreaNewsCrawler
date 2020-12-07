from bs4 import BeautifulSoup
from time import sleep
import calendar
import csv
import requests
import re
import json
from exceptions import *
from multiprocessing import Process

class SportCrawler:
    def __init__(self):
        self.category = {'한국야구': "kbaseball",'해외야구': "wbaseball",'해외축구' : "wfootball",
                         '한국축구': "kfootball", '농구': "basketball", '배구': "volleyball", '일반 스포츠': "general", 'e스포츠': "esports"}
        self.selected_category = []
        self.selected_urlcategory=[]
        self.date = {'startyear': 0,'startmonth':0, 'endyear': 0, 'endmonth': 0}

    def javascript_totalpage(self, url):

        totalpage_url = url +"&page=10000"
        request_content = requests.get(totalpage_url,headers={'User-Agent':'Mozilla/5.0'})
        pagenumber = re.findall('\"totalPages\":(.*)}',request_content.text)
        return int(pagenumber[0])


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

    def Clearcontent(self, text):
        remove_special = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        remove_author = re.sub('\w\w\w 기자', '', remove_special)
        remove_flasherror = re.sub(
            '본문 내용|TV플레이어| 동영상 뉴스|flash 오류를 우회하기 위한 함수 추가fuctio flashremoveCallback|tt|t|앵커 멘트|xa0', '', remove_author)
        remove_strip = remove_flasherror.strip().replace('   ', '')  # 공백 에러 삭제
        reverse_content = ''.join(reversed(remove_strip))  # 기사 내용을 reverse 한다.
        cleared_content = ''
        for i in range(0, len(remove_strip)):
            if reverse_content[
               i:i + 2] == '.다':  # 기사가 reverse 되었기에  ".다"로 기사가 마무리 되므로, 이를 탐색하여 불필요한 정보를 모두 지운다.

                cleared_content = ''.join(reversed(reverse_content[i:]))
                break
        cleared_content = re.sub('if deployPhase(.*)displayRMCPlayer ','',cleared_content)
        return cleared_content

    def Clearheadline(self, text):
        first = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&n▲▶◆◀■\\\=\(\'\"]', '', text)
        return first

    def Make_url(self, URL, startyear, lastyear, startmonth, lastmonth):
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
                    url = f'{url}{year}{Month}{Month_Day}'
                    final_url = url  # page 날짜 정보만 있고 page 정보가 없는 url 임시 저장

                    totalpage = self.javascript_totalpage(url)  # TotalPage 확인
                    for page in range(1, totalpage + 1):
                        url = final_url  # url page 초기화
                        url = f'{url}&page={page}'
                        Maked_url.append(url)  # [[page1,page2,page3 ....]
        return Maked_url
    def crawling(self, category_name):
        Url_category = []
        Category = []
        Category.append(category_name)
        Url_category.append(self.category[category_name])
        titlescript = []

        officename_script = []
        completed_content_match = []
        timescript = []
        for url_label in Url_category:  # URL 카테고리. Multiprocessing시 어차피 1번 도는거라 refactoring할 필요 있어보임
            category = Category[Url_category.index(url_label)]  # URL 인덱스와 Category 인덱스가 일치할 경우 그 값도 일치
            url = f'https://sports.news.naver.com/{url_label}/news/list.nhn?isphoto=N&view=photo&date='
            final_urlday = self.Make_url(url,self.date['startyear'],
                                                self.date['endyear'], self.date['startmonth'], self.date['endmonth'])
            print("succeed making url")
            if len(str(self.date['startmonth'])) == 2:
                startmonth = str(self.date['startmonth'])
            else:
                startmonth = '0'+str(self.date['startmonth'])
            if len(str(self.date['endmonth']))==2:
                endmonth=str(self.date['endmonth'])
            else:
                endmonth = '0'+str(self.date['endmonth'])
            file = open("Sport_" + category + "_"+str(self.date['startyear'])+str(startmonth)
                        +"_"+str(self.date['endyear'])+str(endmonth)+".csv", 'w', encoding='euc-kr', newline='')
            #위의 경우 self.date['endyear']가 f string으로 사용이 안됩니다.
            wcsv = csv.writer(file)
            hefscript2 = [] #이는 크롤링이 아닌 csv에 사용
            for list_page in final_urlday:  # Category Year Month Data Page 처리 된 URL
                # 제목 / URL
                request_content = requests.get(list_page, headers={'User-Agent': 'Mozilla/5.0'})
                content_dict = json.loads(request_content.text)
                hefscript = [] #이는 크롤링에 사용
                for contents in content_dict["list"]:
                    oid = contents['oid']
                    aid = contents['aid']
                    titlescript.append(contents['title'])
                    timescript.append(contents['datetime'])
                    hefscript.append("https://sports.news.naver.com/news.nhn?oid=" + oid + "&aid=" + aid)
                    hefscript2.append("https://sports.news.naver.com/news.nhn?oid=" + oid + "&aid=" + aid)
                    officename_script.append(contents['officeName'])
                # 본문
                # content page 기반하여 본문을 하면 된다. text_sentence에 본문을 넣고 Clearcontent진행 후 completed_conten_match에 append해주면 된다.
                # 추가적으로 pass_match에 언론사를 집어넣으면 된다.

                for content_page in hefscript:

                    sleep(0.01)
                    content_request_content = requests.get(content_page, headers={'User-Agent': 'Mozilla/5.0'})
                    content_document_content = BeautifulSoup(content_request_content.content, 'html.parser')
                    content_Tag_content = content_document_content.find_all('div', {'class': 'news_end'},
                                                                            {'id': 'newsEndContents'})
                    text_sentence = ''  # 뉴스 기사 본문 내용 초기화

                    try:
                        text_sentence = text_sentence + str(content_Tag_content[0].find_all(text=True))
                        completed_content_match.append(self.Clearcontent(text_sentence))
                    except:
                        pass

            # Csv 작성
            for csv_timeline, csv_headline, csv_content, csv_press, csv_url in zip(timescript,titlescript, completed_content_match, officename_script,hefscript2):
                try:
                    if not csv_timeline:
                        continue
                    if not csv_headline:
                        continue
                    if not csv_content:
                        continue
                    if not csv_press:
                        continue
                    if not csv_url:
                        continue
                    wcsv.writerow([csv_timeline, self.Clearheadline(csv_headline), csv_content, csv_press, category,csv_url])
                except:
                    pass

            file.close()

    def set_category(self, *args):
        for key in args:
            if self.category.get(key) is None:
                raise InvalidCategory(key)
        self.selected_category = args
        for selected in self.selected_category:
            self.selected_urlcategory.append(self.category[selected])
    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_category:
            proc = Process(target=self.crawling, args=(category_name,))
            proc.start()
    def set_date_range(self,startyear,startmonth,endyear,endmonth):
        self.date['startyear'] = startyear
        self.date['startmonth'] = startmonth
        self.date['endyear'] = endyear
        self.date['endmonth'] = endmonth


# Main
if __name__ == "__main__":
    Spt_crawler = SportCrawler()
    Spt_crawler.set_category('한국야구','한국축구')
    Spt_crawler.set_date_range(2020,12,2020,12)
    Spt_crawler.start()
