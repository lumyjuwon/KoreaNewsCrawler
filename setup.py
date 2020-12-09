from setuptools import setup

setup(
    name             = 'KoreaNewsCrawler',
    version          = '1.42',
    description      = 'Crawl the korean news',
    author           = 'lumyjuwon',
    author_email     = 'lumyjuwon@gmail.com',
    url              = 'https://github.com/lumyjuwon/KoreaNewsCrawler',
    download_url     = 'https://github.com/lumyjuwon/KoreaNewsCrawler/archive/1.42.tar.gz',
    install_requires = ['requests', 'beautifulsoup4'],
    packages         = ['korea_news_crawler'],
    keywords         = ['crawl', 'KoreaNews', 'crawler'],
    python_requires  = '>=3.6',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)