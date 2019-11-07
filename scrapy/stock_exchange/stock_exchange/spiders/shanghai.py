# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class ShanghaiSpider(CommonSpider):
    name = 'shanghai'
    start_urls = ['https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Shanghai_Stock_Exchange']

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = ShanghaiSpider.name
        self.language_select = 'en'
        super()
