import requests
from requests.exceptions import RequestException
import sys
import re
import os
import subprocess
# from urlparse import urlparse
from threading import Thread
# import httplib, sys
# from Queue import Queue

# input list file & output ok, bad files
in_file = "sample.txt"
out_ok_file = "out_ok.txt"
out_bad_file = "out_bad.txt"

# result string
result_ok_str = ""
result_bad_str = ""

# checking urls
checking_urls = []

def doWork(url):
    status, url = getStatus(url)
    doSomethingWithResult(status, url)

def getStatus(ourl):
    try:
        # url = urlparse(ourl)
        url = ourl
        r = requests.get(url, stream=True, timeout=10)
        # conn = httplib.HTTPConnection(url.netloc)   
        # conn.request("HEAD", url.path)
        # res = conn.getresponse()
        return r.status_code, url
    except:
        return "error", url

def doSomethingWithResult(status, url):
    global result_ok_str, result_bad_str
	# print(status, url)
    if status != 404:
        result_ok_str += url + "\n"
    else :
        result_bad_str += url + "\n"

def main():
    try:
        # download log file handler & logs
        file_handler = open(in_file, "a+")
        file_ok_handler = open(out_ok_file, "w")
        file_bad_handler = open(out_bad_file, "w")
        file_handler.seek(0)
        in_str = file_handler.read()

        for url in in_str.split():
            checking_urls.append(url.strip())
            t = Thread(target=doWork(url))
            t.daemon = True
            t.start()
			# doWork(url)

        file_ok_handler.write(result_ok_str)
        file_bad_handler.write(result_bad_str)
        file_handler.close()

    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()