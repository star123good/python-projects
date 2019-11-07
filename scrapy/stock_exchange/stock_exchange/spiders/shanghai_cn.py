# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class ShanghaiCnSpider(CommonSpider):
    name = 'shanghai_cn'
    start_urls = ['https://zh.wikipedia.org/wiki/Category:%E4%B8%8A%E6%B5%B7%E8%AF%81%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8']

    def __init__(self):
        self.info_titles = ['Name', '产业', '員工人數', '网站', '代表人物', '總資產', '成立', '總部']
        self.stock_name = ShanghaiCnSpider.name
        self.language_select = 'cn'
        super()

