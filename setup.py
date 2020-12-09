from setuptools import setup

# build package command: python setup.py bdist_wheel
# release package command: twine upload dist/KoreaNewsCrawler-version-py3-none-any.whl

setup(
    name             = 'KoreaNewsCrawler',
    version          = '1.50',
    description      = 'Crawl the korean news',
    author           = 'lumyjuwon',
    author_email     = 'lumyjuwon@gmail.com',
    url              = 'https://github.com/lumyjuwon/KoreaNewsCrawler',
    download_url     = 'https://github.com/lumyjuwon/KoreaNewsCrawler/archive/1.50.tar.gz',
    install_requires = ['requests', 'beautifulsoup4'],
    packages         = ['korea_news_crawler'],
    keywords         = ['crawl', 'KoreaNews', 'crawler'],
    python_requires  = '>=3.6',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3.6'
    ]
)