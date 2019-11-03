# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class NasdaqSpider(CommonSpider):
    name = 'nasdaq'
    start_urls = ['https://en.wikipedia.org/wiki/Category:Companies_listed_on_NASDAQ']

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = NasdaqSpider.name
        self.language_select = 'en'
        super()
