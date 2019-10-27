# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class BombaySpider(CommonSpider):
    name = 'bombay'
    start_urls = ['https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Bombay_Stock_Exchange']

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = BombaySpider.name
        self.language_select = 'en'
        super()
