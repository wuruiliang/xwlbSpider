## 新闻联播文字内容爬取

### Install:
1. install python and scrapy
2. create table:
```sql
CREATE TABLE `xwlb_text`
(
    `ID`           BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `TITLE`        VARCHAR(1024) NOT NULL,
    `DATE`         BIGINT(20) NOT NULL,
    `SUMMARY`      TEXT,
    `CONTENT`      TEXT,
    `URL`          VARCHAR(256),
    `TIME_CREATED` BIGINT(20) NOT NULL,
    `TIME_UPDATED` BIGINT(20) NOT NULL,
    KEY `index__time_created` (`TIME_CREATED`),
    KEY `index__time_updated` (`TIME_UPDATED`),
    KEY `index__date` (`DATE`)
);
```

### Run:
`scrapy crawl xwlbText`
> summary and content are Base64 encrypted