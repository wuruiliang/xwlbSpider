# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import time
import base64
from datetime import datetime

from pymysql import MySQLError


class XwlbspiderPipeline:
    mysql_host = '127.0.0.1'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = ''
    mysql_db = 'xwlb'
    db = None
    def process_item(self, item, spider):
        if item['content'] is None or item['summary'] is None or item['title'] is None or item['url'] is None:
            print('content is empty. date=%s, url=%s' % (item['date'], item['url']))
            return
        cursor = self.db.cursor()
        now = int(datetime.now().timestamp())
        date = int(time.mktime(time.strptime(item['date'], spider.date_format)))
        sql = "insert into xwlbText(title,date,summary,content,url,time_created,time_updated) \
        values ('%s',%s,'%s','%s','%s',%s,%s)" \
        % (item['title'].strip(), date, str(base64.b64encode(item['summary'].encode('utf-8')), 'utf-8'), \
           str(base64.b64encode(item['content'].encode('utf-8')), 'utf-8'), \
           str(base64.b64encode(item['url'].encode('utf-8')), 'utf-8'), now, now)
        try:
            cursor.execute(sql)
            self.db.commit()
        except MySQLError:
            self.db.rollback()
            raise MySQLError
        finally:
            pass

    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_password,
            db=self.mysql_db,
            charset='utf8')

    def close_spider(self, spider):
        self.db.close()