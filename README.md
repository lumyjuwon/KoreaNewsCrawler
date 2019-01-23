# newscrawler
이 크롤러는 네이버 포털에 올라오는 언론사 뉴스 기사들을 크롤링 해주는 크롤러입니다.

크롤링 가능한 기사 카테고리는 정치, 경제, 생활문화, IT과학, 사회 입니다.

스포츠 기사같은 경우 야구, 축구, 농구, 배구, 골프, 일반 스포츠, e스포츠 입니다.

## 사용자 파이썬 패키지
  * BeautifulSoup
  
  SetUp: pip install beautifulsoup4

## 사용법

* set_category(category_name)
  
  이 메서드는 수집하려고자 하는 카테고리는 설정하는 메서드입니다.
  파라미터에 들어갈 수 있는 카테고리는 '정치', '경제', '사회', '생활문화', '세계', 'IT과학'입니다.
  파라미터는 여러 개 들어갈 수 있습니다.
  
* set_date_range(startyear, endyear, endmonth)
  
  이 메서드는 수집하려고자 하는 뉴스의 기간을 의미합니다. 기본적으로 1월달부터 endmonth월까지 데이터를 수집합니다.
  
* start()
  
  이 메서드는 크롤링 실행 메서드입니다.
  
e.g)

Crawler = ArticleCrawler()

Crawler.set_category("정치", "IT과학", "세계", "경제")

Crawler.set_date_range(2017, 2018, 4)

Crawler.start()
  
  2017년 1월 ~ 2018년 4월까지 정치, IT과학, 세계, 경제 카테고리 뉴스를 멀티프로세서를 이용하여 병렬 크롤링을 진행 함.
    
 
 ## 결과물
 ![ex_screenshot](./img/article_resultimg.PNG)
 ![ex_screenshot](./img/sport_resultimg.PNG)
 
 수집한 모든 데이터는 csv 확장자로 저장됩니다.
 
