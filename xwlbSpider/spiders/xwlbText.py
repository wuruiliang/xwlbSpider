import scrapy
import time
from ..utils import open_connection
from ..utils import close_connection

from xwlbSpider.items import XwlbTextItem


class xwlbTextSpider(scrapy.Spider):
    name = 'xwlbText'
    allowed_domains = ['mrxwlb.com']
    start_urls = ['http://mrxwlb.com']
    date_format = '%Y年%m月%d日'
    proxy = None
    last_date = None

    def __init__(self, proxy=None, last_date=None, *args, **kwargs):
        super(xwlbTextSpider, self).__init__(*args, **kwargs)
        self.proxy = proxy
        self.last_date = last_date

    def parse(self, response, **kwargs):
        last_date = None
        for each in response.xpath('//*/article'):
            header = each.xpath('header/h1[@class="entry-title"]/a/text()').extract_first().strip()
            if header is not None:
                date = header.replace('新闻联播文字版', '')
                exists = self.get_exist_data(int(time.mktime(time.strptime(date, self.date_format))))
                last_date = date
                if exists is None or not exists:
                    open_url = each.xpath('header/h1[@class="entry-title"]/a/@href').extract_first()
                    yield scrapy.Request(url=open_url, callback=self.parse_content)
        if self.last_date is not None and int(time.mktime(time.strptime(last_date, self.date_format))) > int(
                time.mktime(time.strptime(self.last_date, self.date_format))):
            next_url = response.xpath(
                '//*/nav/div[@class="nav-links"]/a[@class="next page-numbers"]/@href').extract_first()
            if next_url is not None:
                yield scrapy.Request(url=next_url, callback=self.parse, meta={})

    def parse_content(self, response):
        header = response.xpath('//*/header[@class="entry-header"]/h1[@class="entry-title"]/text()').extract_first()
        summary_list = response.xpath('//*/section[@class="entry-content"]/ul/li')
        content_list = response.xpath('//*/section[@class="entry-content"]/p')
        summary = ''
        content = ''
        for each in summary_list:
            summary += each.extract() + '\n'
        for each in content_list:
            content += each.extract() + '\n'
        item = XwlbTextItem()
        item['title'] = header.strip() if header is not None else None
        item['url'] = response.request.url
        item['date'] = header.strip().replace('新闻联播文字版', '') if header is not None else None
        item['summary'] = summary
        item['content'] = content
        yield item

    def get_exist_data(self, date):
        db = open_connection()
        cursor = db.cursor()
        sql = 'select * from xwlbText where date=%s' % date
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        finally:
            close_connection(db)
