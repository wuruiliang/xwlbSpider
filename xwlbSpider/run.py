from scrapy import cmdline

name = 'xwlbText'
last_date = '2021年3月28日'
cmd = 'scrapy crawl {0} -a last_date={1}'.format(name, last_date)
cmdline.execute(cmd.split())