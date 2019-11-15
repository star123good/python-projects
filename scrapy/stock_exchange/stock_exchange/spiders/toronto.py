# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class TorontoSpider(CommonSpider):
    name = 'toronto'
    start_urls = ['https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Toronto_Stock_Exchange']

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = TorontoSpider.name
        self.language_select = 'en'
        super()
