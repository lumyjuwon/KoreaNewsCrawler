# KoreaNewsCrawler

This crawler is a crawler that crawls news articles from media organizations posted on NAVER portal.  
Crawlable article categories include politics, economy, lifeculture, global, IT/science, society.
In the case of sports articles, that include korea baseball, korea soccer, world baseball, world soccer, basketball, volleyball, golf, general sports, e-sports.
  
## How to install
    pip install KoreaNewsCrawler
    
## Method

* **set_category(category_name)**
  
 This method is to set the category you want to collect.  
 The categories that can be included in the parameter are 'politics', 'economy', 'society', 'living_culture', 'IT_science', 'world', and 'opinion'.  
 You can have multiple parameters.  
 category_name: politics, economy, society, living_culture, IT_science, world, opinion
  
* **set_date_range(startyear, startmonth, endyear, endmonth)**
  
 This method refers to the time period of news you want to collect. By default, it collects data from the month of startmonth to the month of endmonth.
  
* **start()**
  
 This method is the crawl execution method.
  
## Article News Crawler Example
```
from korea_news_crawler.articlecrawler import ArticleCrawler

Crawler = ArticleCrawler()  
Crawler.set_category("politics", "IT_science", "economy")  
Crawler.set_date_range("2017-01", "2018-04-20") 
Crawler.start()
```
  Perform a parallel crawl of news in the categories Politics, IT Science, and Economy from January 2017 to April 20, 2018 using a multiprocessor.

## Sports News Crawler Example 
  Method is similar to ArticleCrawler().
```
from korea_news_crawler.sportcrawler import SportCrawler 

Spt_crawler = SportCrawler()
Spt_crawler.set_category('korea baseball','korea soccer')
Spt_crawler.set_date_range("2017-01", "2018-04-20") 
Spt_crawler.start()
```
  Execute a parallel crawl of Korean baseball and Korean soccer news from January 2017 to April 20, 2018 using a multiprocessor.
  
## Results
 ![ex_screenshot](./img/article_result.PNG)
 ![ex_screenshot](./img/sport_resultimg.PNG)
 
 Colum A: Article date & time  
 Colum B: Article Category  
 Colum C: Media Company  
 Colum D: Article title  
 Colum E: Article body  
 Colum F: Article address  
 All the data you collect is saved with a CSV extension.  
