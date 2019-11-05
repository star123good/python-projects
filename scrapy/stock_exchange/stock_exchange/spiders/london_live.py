# -*- coding: utf-8 -*-
import scrapy
# from ..common_analyze import convert_to_string


class LondonLiveSpider(scrapy.Spider):
    name = 'london_live'
    start_urls = [
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=MCX',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=NMX',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=ASX',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=AIM5',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=AIM1',
        'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=AXX',
    ]

    def parse(self, response):
        # body tag
        body_tag = response.css('div#pi-colonna1-display')

        # all detail pages
        tbody_tag = body_tag.css('tbody')
        for tr_tag in tbody_tag.css('tr'):
            next_url = tr_tag.css('td')[1].css('a::attr(href)').get()
            if next_url is not None:
                yield response.follow(next_url, callback=self.detail_parse)

        # next page url
        next_url = body_tag.css('a[title="Next"]::attr(href)').get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)

    def detail_parse(self, response):
        table_tag = response.css('table[summary="Company Information"] tbody')
        title_tag = response.css('div#box-testata')
        if table_tag is not None and title_tag is not None:
            result = {}
            result['title'] = (''.join(title_tag.css('h1.tesummary::text').extract())).strip()
            for tr_tag in table_tag.css('tr'):
                # td_tags = tr_tag.css('td::text')
                # td_tags = tr_tag.xpath('.//td//text()')
                td_tags = tr_tag.css('td')
                if len(td_tags) > 1:
                    # key = convert_to_string(td_tags[0].xpath('.//text()'))
                    # value = convert_to_string(td_tags[1].xpath('.//text()'))
                    key = td_tags[0].css('::text').get()
                    if td_tags[1].css('a').get() is not None:
                        value = td_tags[1].css('a::attr(href)').get()
                    else:
                        value = td_tags[1].css('::text').get()
                    result[key] = value
            
            yield result