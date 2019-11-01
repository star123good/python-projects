# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class HongkongCnSpider(CommonSpider):
    name = 'hongkong_cn'
    start_urls = ['https://zh.wikipedia.org/wiki/%E9%A6%99%E6%B8%AF%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%88%97%E8%A1%A8']

    def __init__(self):
        self.info_titles = ['Name', '产业', '員工人數', '网站', '創辦人', '總資產', '成立', '總部']
        self.stock_name = HongkongCnSpider.name
        self.language_select = 'cn'
        super()
