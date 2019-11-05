# -*- coding: utf-8 -*-
import scrapy
import io
import re
import PyPDF2
from ..common_analyze import get_domain_from_url, ignored_extensions, pdf_extension, get_pattern_texts


class CompanySpider(scrapy.Spider):
    name = 'company'
    start_urls = ['']
    # allowed_domains = [get_domain_from_url(url) for url in start_urls]
    total_counter = 0

    def parse(self, response):
        try:
            if response.url[-4:].lower() == pdf_extension:
                self.read_pdf(response)
            elif response.css('body') is not None:
                # counter
                counter = get_pattern_texts(response=response)
                if counter > 0:
                    CompanySpider.total_counter += counter
                    # yield {'counter' : CompanySpider.total_counter, 'url' : response.url}
                
                # next url
                if response.css('a') is not None:
                    for a_tag in response.css('a'):
                        next_url = a_tag.css('::attr(href)').get()
                        if next_url is not None:
                            if next_url[-4:].lower() == pdf_extension:
                                # pdf read
                                yield response.follow(next_url, callback=self.read_pdf)
                            elif next_url[-4:].lower() not in ignored_extensions:
                                # html type response
                                yield response.follow(next_url, callback=self.parse)
        except:
            pass
    
    def __init__(self, *args, **kwargs): 
        super(CompanySpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')]
        self.allowed_domains = [get_domain_from_url(url) for url in self.start_urls]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CompanySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s, total counter: %d', spider.allowed_domains, CompanySpider.total_counter)
        print('Spider closed: {}, total counter: {}'.format(spider.allowed_domains, CompanySpider.total_counter))

    def read_pdf(self, response):
        reader = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        count = reader.numPages
        for i in range(count):
            page = reader.getPage(i)
            # counter
            counter = get_pattern_texts(text=page.extractText())
            if counter > 0:
                CompanySpider.total_counter += counter