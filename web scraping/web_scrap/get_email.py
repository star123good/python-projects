from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

def get_content(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print(e)
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_emails(url):
    html_text = get_content(url)
    html_text = html_text.decode('utf-8')
    mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)
    mail_list = list(dict.fromkeys(mail_list))
    return mail_list

def main():
    emails = get_emails('https://fr.mappy.com/activite/accessoires-de-mode/06000-nice#/0/M2/Taccessoires-de-mode/N151.12061,6.11309,7.26627,43.70343/Z11/')
    print(emails)

if __name__ == '__main__':
    main()