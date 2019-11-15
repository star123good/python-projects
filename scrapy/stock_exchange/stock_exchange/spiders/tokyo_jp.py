# -*- coding: utf-8 -*-
# import scrapy
from ..common_analyze import CommonSpider


class TokyoJpSpider(CommonSpider):
    name = 'tokyo_jp'
    start_urls = ['https://ja.wikipedia.org/wiki/Category:%E6%9D%B1%E8%A8%BC%E4%B8%80%E9%83%A8%E4%B8%8A%E5%A0%B4%E4%BC%81%E6%A5%AD']

    def __init__(self):
        self.info_titles = ['Name', '業種', '従業員数', '外部リンク', '関係する人物', '資本金', '設立', '本店所在地']
        self.stock_name = TokyoJpSpider.name
        self.language_select = 'jp'
        super()
