# -*- coding: utf-8 -*-
import scrapy
import os
import errno



# make folder and file
# and write content in it
def make_write_file(filename, content, replace_flag, replace_source, replace_target):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            # if exc.errno != errno.EEXIST:
            #     raise
            pass
    
    if replace_flag == True:
        content = content.decode()
        content = content.replace("'", '"')
        content = content.replace('<a href="'+replace_source, '<a href="'+replace_target)
        content = content.encode('utf-8')
        # my_regex = r'(?<=<a href=")' + re.escape(replace_source) + r'[^"]*'
        # content = re.sub(my_regex, '<a href="'+replace_target+'">', content)

    with open(filename, "wb") as f:
        f.write(content)


# if not login, return true
def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    return False


# indir spider
# running command : "scrapy crawl indir"
class IndirSpider(scrapy.Spider):
    name = 'indir'
    base_url = 'https://'
    target_root = 'indir'
    target_url = 'http://' + target_root + '/'
    start_urls = [base_url+'wp-login.php']
    default_url = base_url+''

    # spider from login page
    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'log': '', 'pwd': ''},
            callback=self.after_login
        )

    # after login, scrape the frist page
    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed.")
            return

        # continue scraping with authenticated session...
        return response.follow(self.default_url, self.parse_after_login)

    # after login, crawler
    def parse_after_login(self, response):
        # get filename from response.url
        filename = self.target_root + '/' + response.url.split('#')[0].replace(self.base_url, '') + 'index.html'
        make_write_file(filename, response.body, True, self.base_url, self.target_url)

        # get next page urls
        next_page = response.css('a.nextpostslink::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_after_login)

        # get every films urls
        film_urls = response.css('div.yazi a.more-link::attr(href)').getall()
        for next_url in film_urls:
            yield response.follow(next_url, callback=self.parse_after_login)
