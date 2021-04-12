from peewee import Model, CharField, BooleanField, ForeignKeyField
from playhouse.db_url import connect
from crawler.config import BASE_LINK

db = connect('mysql://Mohammad:09101916484@127.0.0.1:3306/CafeBazzar')


class BaseModel(Model):
    class Meta:
        database = db


class LinkCafeBazzar(BaseModel):
    path = CharField(max_length=255)
    url = CharField(max_length=255)
    crawl = BooleanField(default=False)

    @classmethod
    def load_links(cls):
        return cls.select().where(cls.crawl == False)

    @classmethod
    def check_exists(cls, path):
        query = cls.select().where(cls.path == path)
        if query.exists():
            return False
        return True

    @classmethod
    def save_links(cls, paths):
        for path in paths:
            if cls.check_exists(path):
                cls.create(path=path, url=BASE_LINK + path)

    @classmethod
    def update_status(cls, path):
        link = cls.select().where(cls.path == path, cls.crawl == False).first()
        link.crawl = True
        link.save()

    @classmethod
    def show_info(cls, type_info):
        if type_info == 'all_crawl':
            return cls.select().count()
        elif type_info == 'true_crawl':
            return cls.select().where(cls.crawl == True).count()
        elif type_info == 'false_crawl':
            return cls.select().where(cls.crawl == False).count()


class Categories(BaseModel):
    name = CharField(max_length=255)

    CATEGORIES_APPS = [
        'آب و هوا',
        'آشپزی و رستوران',
        'آموزش',
        'ابزارها',
        'استراتژی',
        'امتیازی',
        'امور مالی',
        'اکشن',
        'تفننی',
        'تناسب اندام',
        'خرید',
        'رانندگی',
        'رفت و آمد',
        'سبک زندگی',
        'سرگرمی',
        'سفر',
        'شبکه‌های اجتماعی',
        'شبیه‌سازی',
        'شخصی‌سازی',
        'عکاسی و ویدیو',
        'مذهبی',
        'معمایی',
        'موسیقی',
        'ورزشی',
        'پزشکی',
        'کتاب‌ها و مطبوعات',
        'کلمات و دانستنی‌ها',
        'کودک',
    ]

    @classmethod
    def check_exists(cls, category):
        query = cls.select().where(cls.name == category)
        if query.exists():
            return False
        return True

    @classmethod
    def set_foreignkey_category(cls, category):
        if category in cls.CATEGORIES_APPS:
            q_category = cls.select().where(cls.name == category)
            return q_category
        return None

    @classmethod
    def save_category(cls, category):
        if cls.check_exists(category):
            cls.create(name=category)

    @classmethod
    def show_information(cls):
        count = 0
        for category in sorted(cls.CATEGORIES_APPS):
            cat = cls.select().where(cls.name == category).first()
            print(f'category: {cat.name.ljust(40)}\t|\t'
                  f' app count: {cat.apps.count()}')
            count += cat.apps.count()
        print(count)


class DataCafeBazzar(BaseModel):
    app_name = CharField(max_length=255)
    app_package_name = CharField(max_length=64)
    app_url = CharField(max_length=255),
    app_author_name = CharField(max_length=64)
    app_category_name = ForeignKeyField(Categories, backref='apps')
    app_price = CharField(max_length=32)
    app_rate = CharField(max_length=8)
    app_review_count = CharField(max_length=32)
    app_install_count = CharField(max_length=32)
    app_size = CharField(max_length=32)

    @classmethod
    def load_data(cls):
        return cls.select()

    @classmethod
    def check_exists(cls, data):
        query = cls.select().where(
            cls.app_package_name == data['app_package_name']
        )
        if query.exists():
            return False
        return True

    @classmethod
    def save_apps(cls, data):
        if cls.check_exists(data):
            if data['app_category_name'] in Categories.CATEGORIES_APPS:
                category = Categories.set_foreignkey_category(
                    data['app_category_name']
                )
                data['app_category_name'] = category
                cls.create(**data)
                LinkCafeBazzar.update_status(data['app_package_name'])
                print(f'saved {data["app_package_name"]}')
            else:
                print(f'category: {data["app_category_name"]} not found')
        else:
            LinkCafeBazzar.update_status(data['app_package_name'])
            print(f'this {data["app_package_name"]} is exists')

    @classmethod
    def show_info(cls):
        return cls.select().count()
