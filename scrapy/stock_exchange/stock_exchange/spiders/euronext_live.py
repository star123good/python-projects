# -*- coding: utf-8 -*-
import scrapy
from ..common_analyze import convert_to_string


class EuronextLiveSpider(scrapy.Spider):
    name = 'euronext_live'
    start_urls = [
        'https://live.euronext.com/en/ajax/getTopPerformersPopup/MostActive?belongs_to=ALXA,XAMS,TNLA&is_factory=true',
        'https://live.euronext.com/en/ajax/getTopPerformersPopup/MostActive?belongs_to=ALXB,XBRU,MLXB,ENXB,TNLB&is_factory=true',
        'https://live.euronext.com/en/ajax/getTopPerformersPopup/MostActive?belongs_to=XESM,XMSM,XATL,XDUB&is_factory=true',
        'https://live.euronext.com/en/ajax/getTopPerformersPopup/MostActive?belongs_to=ENXL,ALXL,XLIS&is_factory=true',
        'https://live.euronext.com/en/ajax/getTopPerformersPopup/MostActive?belongs_to=XPAR,ALXP,XMLI&is_factory=true',
    ]

    def parse(self, response):
        # body tag
        body_tag = response.css('tbody')

        # tr tag
        for tr_tag in body_tag.css('tr'):
            td_name = tr_tag.css('td.name')
            next_url = td_name.css('a::attr(href)').get()
            title = td_name.css('a::text').get()
            if next_url is not None and title is not None:
                next_url = 'https://live.euronext.com' + next_url
                # yield scrapy.Request(next_url, callback=self.detail_parse_quote, meta={ 'data' : { 'title' : title }, 'url' : next_url })
                yield scrapy.Request(next_url+'/market-information', callback=self.detail_parse_market, meta={ 'data' : { 'title' : title }, 'url' : next_url })

    def detail_parse_quote(self, response):
        data = response.meta.get('data', {})
        next_url = response.meta.get('url', '')
        # title = response.css('h1#header-instrument-name strong::text').get()
        # price = response.css('span#header-instrument-price::text').get()
        # currency = response.css('span#header-instrument-currency::text').get()
        # data['title'] = title
        # data['price'] = currency + price

        quote_tbody_tag = response.css('div#detailed-quote tbody')
        if quote_tbody_tag is not None:
            for tr_tag in quote_tbody_tag.css('tr'):
                td_tags = tr_tag.css('td::text').getall()
                if td_tags[0] == 'Volume' : data['volume'] = td_tags[1]
                elif td_tags[0] == 'Market Cap' : data['market_cap'] = td_tags[1]
        
        yield scrapy.Request(next_url+'/market-information', callback=self.detail_parse_market, meta={ 'data' : data, 'url' : next_url })
    
    def detail_parse_market(self, response):
        data = response.meta.get('data', {})
        next_url = response.meta.get('url', '')

        for card_tag in response.css('div.card'):
            card_header_tag = card_tag.css('div.card-header h3::text').get()
            if card_header_tag == 'ICB SECTORIAL CLASSIFICATION':
                td_tags = card_tag.css('div.card-body td')
                data['industry'] = convert_to_string(td_tags[1].xpath('.//text()'))
        
        yield scrapy.Request(next_url+'/company-information', callback=self.detail_parse_company, meta={ 'data' : data, 'url' : next_url })
    
    def detail_parse_company(self, response):
        data = response.meta.get('data', {})
        next_url = response.meta.get('url', '')
        
        address_tags = response.css('#home-office-address-column1-wrapper div.mb-1')
        if address_tags is not None:
            data['address'] = convert_to_string(address_tags[0].xpath('.//text()'))
            data['website'] = address_tags[2].css('::attr(href)').get()

        yield data