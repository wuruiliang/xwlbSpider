from scrapy import cmdline

name = 'xwlbText'
date = '2021年04月04日'
cmd = 'scrapy crawl {0} -a date={1}'.format(name, date)
cmdline.execute(cmd.split())