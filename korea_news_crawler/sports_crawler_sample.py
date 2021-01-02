from korea_news_crawler.sportcrawler import SportCrawler

if __name__ == "__main__":
    Spt_crawler = SportCrawler()
    Spt_crawler.set_category('한국야구', '한국축구')
    Spt_crawler.set_date_range(2020, 11, 2020, 11)
    Spt_crawler.start()
