from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import re
import os
import subprocess

# download log file
log_file = "downloads.csv"

# default counter of files to download
counter = 10

# host url
host_url = "https://www.kanald.com.tr"

# default path
# default_path = "/carkifelek/bolumler"
default_path = "/oylebirgecerzamanki/bolum"

# default url
default_url = host_url + default_path

# pattern path
# pattern_path = "/carkifelek/bolumler"
pattern_path = "/oylebirgecerzamanki/"

# page number
# page_num = 3
page_num = 5

# set of crawled urls
processed_urls = []

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

def get_link_urls(url):
    """
    get a href urls
    """
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    # print(html)
    for a in html.select('a'):
        # print(a['href'])
        if(pattern_path in a['href'] and a['href'].count("/") == 3):
            processed_urls.append(a['href'])
    # print(processed_urls)

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
    for page in range(page_num):
        url = default_url + "?page=" + (str)(page+1)
        get_link_urls(url)

    # download log file handler & logs
    file_handler = open(log_file, "a+")
    file_handler.seek(0)
    logs_str = file_handler.read()

    process_urls(file_handler, logs_str)

    file_handler.close()

if __name__ == '__main__':
    counter = (int)(sys.argv[1])
    main()
    