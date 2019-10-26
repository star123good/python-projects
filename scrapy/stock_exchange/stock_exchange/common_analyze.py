import scrapy


# configs
body_target_css = 'table.infobox.vcard'
body_target_css_jp = 'table.infobox.plainlist'
body_target_css_cn = 'table.infobox.vcard'
website_string = 'Website'
website_string_jp = '外部リンク'
website_string_cn = '网站'
next_page_string = 'next page'
next_page_string_jp = '次のページ'
next_page_string_cn = '下一页'


# get text of an element with all child elements
convert_to_string = lambda tags : ' '.join([p.strip() for p in tags.extract() if p.strip()])

# get next page button string according to language
get_next_page_string = lambda lang : next_page_string if lang == 'en' else next_page_string_jp if lang == 'jp' else next_page_string_cn
# get website string and body tag string
get_web_body_string = lambda lang : (website_string, body_target_css) if lang == 'en' else (website_string_jp, body_target_css_jp) if lang == 'jp' else (website_string_cn, body_target_css_cn)


# analyze exchange info in wiki page
def anlayze_exchange(response):
    info_titles = [
        'Name', 
        # 'Type', 
        'Industry', 
        'Market cap', 
        'Number of listings', 
        'Number of employees', 
        'Website', 
        'Location', 
        'Volume', 
        # 'Founded', 
        # 'Owner',
    ]
    result = None
    infobox_tag = response.css(body_target_css)
    if infobox_tag is not None:
        caption = infobox_tag.css('caption::text').get()
        if caption is not None:
            caption = str(caption)
            result = { key : "" for key in info_titles}
            result['Name'] = caption
            for tr_tags in infobox_tag.css('tr'):
                th_tag = tr_tags.css('th')
                # th = tr_tags.css('th::text').get()
                th = tr_tags.xpath('.//th//text()').get()
                td = tr_tags.css('td::text').get()
                # td = tr_tags.xpath('.//td//text()').get()
                # if th is not "" and th in info_titles:
                if th_tag is not None:
                    th = str(th)
                    # print('  ----   th   ----  ', th)
                    if th == website_string:
                        td = ','.join(tr_tags.css('td a::attr(href)').getall())
                    elif th == "Type":
                        th = "Industry"
                        td = ','.join(tr_tags.css('td a::text').getall())
                    elif th == "Market cap" or th == "Location":
                        td = str(td) + ''.join(tr_tags.css('td a::text').getall())
                    elif "No." in th:
                        th = "Number of listings"
                    else :
                        td = str(td) if td is not None  else ""
                    if th in info_titles:
                        result[th] = td
    return result


# analyze infobox info in wiki page
def anlayze_infobox(response, info_titles, language_select='en'):
    result = None
    current_target_css = body_target_css
    current_website_string = website_string

    (current_website_string, current_target_css) = get_web_body_string(language_select)
    
    infobox_tag = response.css(current_target_css)
    if infobox_tag is not None:
        caption = infobox_tag.css('caption::text').get()
        if language_select == 'cn' and ( caption is None or caption == '' ):
            caption = infobox_tag.css('th::text').get()
        # print(caption)
        if caption is not None:
            caption = str(caption)
            result = { key : "" for key in info_titles}
            result['Name'] = caption
            for tr_tags in infobox_tag.css('tr'):
                th_tag = tr_tags.css('th')
                th = convert_to_string(tr_tags.xpath('.//th//text()'))
                td = convert_to_string(tr_tags.xpath('.//td//text()'))
                if th == current_website_string:
                    td = ','.join(tr_tags.css('td a::attr(href)').getall())
                # print(th, td)
                if th in info_titles:
                    result[th] = td
    return result


# common wiki spider
class CommonSpider(scrapy.Spider):
    name = ''
    start_urls = ['']

    # def __init__(self):
    #     self.info_titles = []
    #     self.stock_name = name
    #     self.language_select = 'en'
    #     super()

    def parse(self, response):
        # body tag
        body_tag = response.css('div#mw-pages')
        if body_tag is None or not body_tag:
            body_tag = response.css('div#bodyContent')
        # print('  --->   ', body_tag)

        # all pages urls
        for next_a_tag in body_tag.xpath('./a'):
            if next_a_tag.css('::text').get() == get_next_page_string(self.language_select):
                next_url = next_a_tag.css('::attr(href)').get()
                yield response.follow(next_url, callback=self.parse)

        # all company urls
        for li_tag in body_tag.css('li'):
            next_url = li_tag.css('a::attr(href)').get()
            if next_url is not None:
                yield response.follow(next_url, callback=self.show_com_page)

    def show_com_page(self, response):
        # show info
        show_result = anlayze_infobox(response, info_titles=self.info_titles, language_select=self.language_select)
        if show_result is not None:
            return show_result