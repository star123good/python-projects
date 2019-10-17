from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import re
import os
import subprocess
from urllib.parse import urlparse

# download log file
log_file = "downloads.csv"

# default counter of files to download
counter = 10

# host url
host_url = ""

# default path
default_path = ""

# default url
default_url = host_url + default_path

# pattern path
pattern_path = ""

# page number
# page_num = 3
page_num = 5

# default max page number
default_max_page_num = 5

# page sort from first to last?
flag_sort_page = True

# set of crawled urls
processed_urls = []


get_page_number = lambda page : (str)(page+1) if flag_sort_page else (str)(default_max_page_num-page)


def get_paths_from_url(url):
    global host_url, default_path, pattern_path, default_url
    url_parse_result = urlparse(url)
    host_url = url_parse_result.scheme + '://' + url_parse_result.netloc
    default_path = url_parse_result.path
    pattern_path = url_parse_result.path.replace('/bolum', '/')
    default_url = host_url + default_path
    # print(host_url, default_path, pattern_path, default_url)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_link_urls(url, start_index=0):
    """
    get a href urls
    """
    global processed_urls, pattern_path
    try:
        raw_html = simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')
        print('downloading... ', url)
        # for a in html.select('a'):
        for a in html.select('div.kd-docs-section a.title'):
            # print(a['href'], pattern_path)
            # if(pattern_path in a['href'] and a['href'].count("/") == 3):
            if flag_sort_page :
                processed_urls.append(a['href'])
            else :
                processed_urls.insert(start_index, a['href'])
        # print(processed_urls)
    except:
        pass
    return len(processed_urls)


def get_content_url(url):
    raw_html = str(simple_get(url), 'utf-8')
    result_urls = re.findall(r'\"contentUrl\":\s*"([^"]*)"',raw_html)
    if(len(result_urls) > 0):
        return result_urls[0]
    else:
        return ''


def process_urls(file_handler, logs_str):
    result_urls = []
    command_urls = []
    result_str = ""
    file_list = os.listdir()
    # processed_urls.reverse()
    
    for url in processed_urls:
        if(not(url in result_urls) and not(url in logs_str)):
            result_urls.append(url)
    # print(result_urls)

    index = 0
    file_index = 1
    for url in result_urls:
        if(index >= counter):
            break
        
        content_url = get_content_url(host_url + url)
        
        if("/media.dogannet.tvS1/" in content_url):
            content_url = content_url.replace("/media.dogannet.tvS1/", "/media.dogannet.tv/S1/")
        
        if(content_url != ''):
            result_str += "\n" + url
            content_url = content_url.replace("index.m3u8", "1000/prog_index.m3u8")
            command_urls.append(content_url)
            filename = str(file_index) + '.mp4'
            while(filename in file_list):
                file_index = file_index + 1
                filename = str(file_index) + '.mp4'
            command = 'ffmpeg -i '+content_url+' -c copy '+filename
            print(command)
            # subprocess.call(command)
            os.system(command)
        index = index + 1
        file_index = file_index + 1
    
    file_handler.write(result_str)


def main():
    last_index = 0
    for page in range(page_num):
        url = default_url + "?page=" + get_page_number(page)
        # print(url)
        last_index = get_link_urls(url, start_index=last_index)

    # download log file handler & logs
    file_handler = open(log_file, "a+")
    file_handler.seek(0)
    logs_str = file_handler.read()

    process_urls(file_handler, logs_str)

    file_handler.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        get_paths_from_url(sys.argv[1])
    if len(sys.argv) > 2:
        if sys.argv[2].upper() == "FALSE" : flag_sort_page = False
    if len(sys.argv) > 3:
        counter = (int)(sys.argv[3])
        main()
    else:
        print('You must type command like this.\nFor example)\npython web_scrape1.py https://www.kanald.com.tr/yarimelma/bolum false 10')
    