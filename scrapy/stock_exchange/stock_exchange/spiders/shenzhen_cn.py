# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class ShenzhenCnSpider(CommonSpider):
    name = 'shenzhen_cn'
    start_urls = ['https://zh.wikipedia.org/wiki/Category:%E6%B7%B1%E5%9C%B3%E8%AF%81%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8']

    def __init__(self):
        self.info_titles = ['Name', '产业', '員工人數', '网站', '代表人物', '總資產', '成立', '總部']
        self.stock_name = ShenzhenCnSpider.name
        self.language_select = 'cn'
        super()
