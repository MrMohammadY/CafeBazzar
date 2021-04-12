from crawler.cafebazaarcrawler import CafeBazzarDataCrawler, \
    CafeBazzarLinkCrawler
from crawler.config import BASE_URL_DATA, BASE_URL_LINK
from models.models import db, LinkCafeBazzar, DataCafeBazzar, Categories
import sys


def create_table():
    db.create_tables([LinkCafeBazzar, DataCafeBazzar, Categories])


def create_categories():
    for category in sorted(Categories.CATEGORIES_APPS):
        Categories.save_category(category)


def show_information():
    print(
        f'all link count: {LinkCafeBazzar.show_info("all_crawl")}\n'
        f'all crawled count: {LinkCafeBazzar.show_info("true_crawl")}\n'
        f'all not crawled count: {LinkCafeBazzar.show_info("false_crawl")}\n'
        f'all apps count in database: {DataCafeBazzar.show_info()}'
    )


def show_information_from_category():
    Categories.show_information()


if __name__ == '__main__':
    create_table()
    create_categories()

    if sys.argv[1] == '-cl':
        crawler = CafeBazzarLinkCrawler(BASE_URL_LINK)
        crawler.run_crawler()

    if sys.argv[1] == '-cd':
        crawler = CafeBazzarDataCrawler(BASE_URL_DATA)
        crawler.run_crawler()

    if sys.argv[1] == '-sai':
        show_information()

    if sys.argv[1] == '-sci':
        show_information_from_category()
