from korea_news_crawler.articlecrawler import ArticleCrawler
if __name__ == "__main__":
    Crawler = ArticleCrawler()
    # 정치, 경제, 생활문화, IT과학, 사회, 세계 카테고리 사용 가능
    Crawler.set_category("IT과학", "세계")
    # 2017년 12월 (1일) 부터 2018년 1월 13일까지 크롤링 시작 YYYY-MM-DD의 형식으로 입력
    Crawler.set_date_range('2017-12', '2018-01-13')
    Crawler.start()
