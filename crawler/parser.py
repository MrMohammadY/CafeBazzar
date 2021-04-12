from crawler.config import BASE_LINK


class Parser:
    """
        for understand parser you should print data and
         copy that and create json file and paste there
         after that you should read that and understand this parser
    """
    @staticmethod
    def link_parser(data):
        """
        :param data: a dictionary get from api and parse here to find app path
        :return:
        """
        link_list = list()

        data = data['singleReply']['getPageV2Reply']['page']['pageBodyInfo'][
            'pageBody']['rows']

        for d in data:
            apps = d.get('simpleAppList')
            if apps:

                for app in apps.get('apps'):
                    link_list.append(app['info']['packageName'].strip())

        return link_list

    @staticmethod
    def data_parser(data):
        """

        :param data: a dictionary get from api and parse here
         to find app information
        :return:
        """
        data = data['singleReply']['appDetailsReply']

        app_data = {
            'app_name': data['name'],
            'app_package_name': data['packageName'],
            'app_url': BASE_LINK + data['packageName'],
            'app_author_name': data['authorName'],
            'app_category_name': data['categoryName'],
            'app_price': data['price']['price'],
            'app_rate': data['stats']['rate'],
            'app_review_count': data['stats']['reviewCount'],
            'app_install_count': data['stats']['installCountRange'],
            'app_size': data['package']['verboseSize']
        }

        return app_data
