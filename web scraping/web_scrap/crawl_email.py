'''
A web crawler for extracting email addresses from web pages.

Takes a string of URLs and requests each page, checks to see if we've
found any emails and prints each email it finds.
'''

import argparse
import re
import sys
import urllib3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, urls):
        '''
        @urls: a string containing the (comma separated) URLs to crawl.
        '''
        self.urls = urls.split(',')

    def crawl(self):
        '''
        Iterate the list of URLs and request each page, then parse it and
        print the emails we find.
        '''
        for url in self.urls:
            data = self.get_content(url)
            if data is not None:
                for email in self.process(data):
                    print(email)

    @staticmethod
    def request(url):
        '''
        Request @url and return the page contents.
        '''
        response = urllib3.urlopen(url)
        return response.read()

    def is_good_response(self, resp):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)

    def get_content(self, url):
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            print(e)
            return None
  
    @staticmethod
    def process(data):
        '''
        Process @data and yield the emails we find in it.
        '''
        data = data.decode('utf-8')
        mail_list = re.findall('\w+@\w+\.{1}\w+', data)
        # for email in re.findall(r'\w+@\w+\.{1}\w+', data):
        for email in mail_list:
            yield email


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--urls', dest='urls', required=True,
        help='A comma separated string of emails.')
    parsed_args = argparser.parse_args()
    crawler = Crawler(parsed_args.urls)
    crawler.crawl()


if __name__ == '__main__':
  sys.exit(main())