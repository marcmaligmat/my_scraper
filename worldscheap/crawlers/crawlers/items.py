import scrapy
from scrapy_djangoitem import DjangoItem
from product.models_game import Game




class CrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GameItem(DjangoItem):
    django_model = Game
    image_urls = scrapy.Field()
    genre_list = scrapy.Field()
    developer_list = scrapy.Field()
    images = scrapy.Field()
    tag_list = scrapy.Field()