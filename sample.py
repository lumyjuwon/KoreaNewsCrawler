from korea_news_crawler.articlecrawler import ArticleCrawler

if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.start(isMultiProc=True)
