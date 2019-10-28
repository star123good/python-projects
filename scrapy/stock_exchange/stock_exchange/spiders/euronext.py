# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class EuronextSpider(CommonSpider):
    name = 'euronext'
    start_urls = [
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_Euronext_Amsterdam',
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_Euronext_Brussels',
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_Euronext_Dublin',
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_Euronext_Lisbon',
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_the_Oslo_Stock_Exchange',
        'https://en.wikipedia.org/wiki/Category:Companies_listed_on_Euronext_Paris',
    ]

    def __init__(self):
        self.info_titles = ['Name', 'Industry', 'Number of employees', 'Website', 'Key people', 'Revenue', 'Founded', 'Headquarters']
        self.stock_name = EuronextSpider.name
        self.language_select = 'en'
        super()
