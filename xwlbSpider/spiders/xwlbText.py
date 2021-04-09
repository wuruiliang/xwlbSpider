import scrapy
import time
from datetime import datetime

from xwlbSpider.items import XwlbTextItem


class xwlbTextSpider(scrapy.Spider):
    name = 'xwlbText'
    allowed_domains = ['mrxwlb.com']
    start_urls = ['http://mrxwlb.com']
    date_format = '%Y年%m月%d日'
    proxy = None
    date = None

    def __init__(self, proxy=None, date=None, *args, **kwargs):
        super(xwlbTextSpider, self).__init__(*args, **kwargs)
        self.proxy = proxy
        self.date = date
        if self.date is None:
            self.date = datetime.today().date().strftime(self.date_format)

    def parse(self, response, **kwargs):
        end_date = int(time.mktime(time.strptime(self.date, self.date_format)))
        for each in response.xpath('//*/article'):
            header = each.xpath('header/h1[@class="entry-title"]/a/text()').extract_first().strip()
            if header is not None:
                post_date = int(time.mktime(time.strptime(header[0: 9], self.date_format)))
                if post_date < end_date:
                    return None
                open_url = each.xpath('header/h1[@class="entry-title"]/a/@href').extract_first()
                yield scrapy.Request(url=open_url, callback=self.parse_content)
        next_url = response.xpath('//*/nav/dev[@class="nav-links"]/a[@class="next"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(url=next_url, callback=self.parse, meta={})

    def parse_content(self, response):
        header = response.xpath('//*/header[@class="entry-header"]/h1[@class="entry-title"]/text()').extract_first()
        date = response.xpath('//*/header[@class="entry-header"]/span[@class="date"]/*/time[@class="entry-date"]/text()').extract_first()
        summary_list = response.xpath('//*/section[@class="entry-content"]/ul/li')
        content_list = response.xpath('//*/section[@class="entry-content"]/p')
        summary = ''
        content = ''
        for each in summary_list:
            summary += each.extract() + '\n'
        for each in content_list:
            content += each.extract() + '\n'
        item = XwlbTextItem()
        item['title'] = header
        item['url'] = response.request.url
        item['date'] = date
        item['summary'] = summary
        item['content'] = content
        yield item
