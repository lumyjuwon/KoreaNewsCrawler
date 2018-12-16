# newscrawler
이 크롤러는 네이버 포털에 올라오는 언론사 뉴스 기사들을 크롤링 해주는 크롤러입니다.

크롤링 가능한 기사 카테고리는 정치, 경제, 생활문화, IT과학, 사회 입니다.

스포츠 기사같은 경우 야구, 축구, 농구, 배구, 골프, 일반 스포츠, e스포츠 입니다.

## 사용자 파이썬 패키지
  * BeautifulSoup
  
  SetUp: pip install beautifulsoup4

## 사용법

  * 수집 분류 설정
  
    url_list = [100, 101,102, 103, 104, 105]
    Category = ["정치", "경제" "사회", "생활문화", "세계", "IT과학"]
    newscrawler는 정치, 경제, 사회, 생활문화, 세계, IT과학 분류의 기사를 수집합니다.
    만약 원하지 않는 분류가 있을 경우 url_list와 Category 리스트에서 요소를 삭제하시기 바랍니다.
  
    100-정치, 101-경제, 102-사회, 103-생활문화, 104-세계, 105-IT과학
  
 * 수집 날짜 설정
 
    #Main 주석이 처리 된 아래 내용에서 final_urlday = Make_url(url, 2017, 2018, 1, 6)을 찾습니다.
    Maker_url(url, 2017, 2018, 1, 6)은 2017년 1월 ~ 2018년 6월 30일 까지 [기사 제목, 기사 본문, 언론사, 카테고리] 데이터를 크롤링 해줍니다.
    Mkaer_url 기간을 수정하여 원하는 기간에 맞는 데이터를 수집하세요.
 
 ## 결과물
 ![ex_screenshot](./img/article_resultimg.PNG)
 ![ex_screenshot](./img/sport_resultimg.PNG)
 
 수집한 모든 데이터는 csv 확장자로 저장됩니다.
 
