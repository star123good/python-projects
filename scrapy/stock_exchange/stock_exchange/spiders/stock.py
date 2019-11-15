# -*- coding: utf-8 -*-
import scrapy
from ..common_analyze import anlayze_exchange


class StockSpider(scrapy.Spider):
    name = 'stock'
    # allowed_domains = ['en.wikipedia.org/wiki']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_stock_exchanges']
    link_text_pattern = 'exchange'
    th_text_pattern = 'stock exchange'
    link_href_pattern = '/wiki/'
    link_href_replace_pattern = 'https://en.wikipedia.org/wiki/'


    # parse
    def parse(self, response):
        # show info
        show_result = anlayze_exchange(response)
        if show_result is not None:
            yield show_result
        
        # body tag
        body_tag = response.css('div#bodyContent')
        
        # wikitable
        for table_tags in body_tag.css('table.wikitable'):
            position = 0
            flag_find_exchange = False
            for th_tag in table_tags.css('th::text').getall():
                position += 1
                if self.th_text_pattern in str(th_tag).lower():
                    flag_find_exchange = True
                    break
            if flag_find_exchange:
                for td_tags in table_tags.css('td:nth-child(n+0):nth-child(-n+'+str(position)+')'):
                    # for a_tags in table_tags.css('a'):
                    for a_tags in td_tags.css('a'):
                        next_url = self.get_next_url(a_tags, False)
                        if next_url is not None:
                            yield response.follow(next_url, callback=self.parse)
        
        # other a tags with pattern
        for a_tags in body_tag.css('a'):
            next_url = self.get_next_url(a_tags)
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)
    
    
    # get next page url
    def get_next_url(self, link_tag, flag_pattern=True):
        result = None
        link_text = str(link_tag.css('::text').get())
        link_href = str(link_tag.css('::attr(href)').get())
        if self.link_href_pattern in link_href and (not flag_pattern or self.link_text_pattern in link_text.lower()):
            result = self.link_href_replace_pattern + link_href.split(self.link_href_pattern, 1)[1]
        return result

    