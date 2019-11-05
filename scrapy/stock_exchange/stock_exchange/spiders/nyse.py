# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class NyseSpider(CommonSpider):
    name = 'nyse'
    start_urls = ['https://en.wikipedia.org/w/index.php?title=Category:Companies_listed_on_the_New_York_Stock_Exchange']

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = NyseSpider.name
        self.language_select = 'en'
        super()
