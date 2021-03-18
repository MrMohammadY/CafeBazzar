import json
import requests
from abc import ABC
from crawler.parser import Parser
from crawler.config import payload_link, payload_data, HEADER, CATEGORIES
from threading import Thread
from ORM.models import LinkCafeBazzar, DataCafeBazzar
from queue import Queue


class BaseCrawler(ABC):
    def __init__(self, url):
        self.url = url
        self.parser = Parser()

    def post(self, data, payload, type_post):
        """
        :param data: data can category or app path
         which characterized with type post

        :param payload: set payload for request to api

        :param type_post:
        can link(requests send to get app path api)
        or data(requests send to get app information api)
        :return:
        """

        if type_post == 'link':
            payload["singleRequest"]["getPageV2Request"]["path"] = data
        else:
            payload["singleRequest"]["appDetailsRequest"]["packageName"] = data

        try:
            response = requests.post(
                self.url,
                data=json.dumps(payload),
                headers=HEADER
            )

        except requests.HTTPError:
            return None

        if response.status_code == 200:
            return response

        return None


class CafeBazzarLinkCrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url)

    def crawl_links(self, categories, thread_index):
        """
        here requests to api with categories payload and get all app path
        and parse that and save

        :param categories:
        :param thread_index:
        :return:
        """
        while categories.qsize():
            category = categories.get()

            try:
                response = self.post(category, payload_link, 'link')

                links = self.parser.link_parser(json.loads(response.content))
                LinkCafeBazzar.save_links(set(links))

                print(f'Thread: {thread_index}\t|\t'
                      f'category: {category}\t|\t\t\t\t\t\t'
                      f'capacity {len(links)}')

                categories.task_done()
            except :
                print(category)
                categories.task_done()

    def run_crawler(self):
        """
        here create a queue with all categories and send to run crawler for get
        all app path from api with categories
        :return:
        """
        threads_list = list()

        queue = Queue()
        [queue.put(c) for c in CATEGORIES]

        for i in range(6):
            thread = Thread(target=self.crawl_links, args=(queue, i))
            threads_list.append(thread)
            thread.start()

        for thread in threads_list:
            thread.join()

        print('All Task Done...')


class CafeBazzarDataCrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url)
        self.paths = None

    def crawl_data(self, queue):
        """
        here send app path in payload to api and get app information from api
        :param queue:
        :return:
        """
        while queue.qsize():
            try:
                path = queue.get()
                response = self.post(path, payload_data, 'data')
                data = self.parser.data_parser(json.loads(response.text))
                DataCafeBazzar.save_apps(data)
                queue.task_done()
            except:
                queue.task_done()

    def run_crawler(self):
        """
        here load all app path from database and create a queue with that
        and save run crawler for get app information from api
        :return:
        """
        links = LinkCafeBazzar.load_links()
        threads_list = list()

        queue = Queue()
        [queue.put(link.path) for link in links]

        for i in range(10):
            thread = Thread(target=self.crawl_data, args=(queue,))
            threads_list.append(thread)
            thread.start()

        for thread in threads_list:
            thread.join()

        print('All Task Done...')
