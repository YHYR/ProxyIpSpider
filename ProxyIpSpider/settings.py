# -*- coding: utf-8 -*-

# Scrapy settings for ProxyIpSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ProxyIpSpider'

SPIDER_MODULES = ['ProxyIpSpider.spiders']
NEWSPIDER_MODULE = 'ProxyIpSpider.spiders'


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'ProxyIpSpider.middlewares.UserAgentMiddleware': 401,
}


# Obey robots.txt rules
ROBOTSTXT_OBEY = True


'''
MySQL Setting
'''
host = 'localhost'
user_name = 'root'
pass_word = 'root'
port = 3306
db_name = 'cloud_music_db'


''' IP有效性校验测试URL'''
request_check_url = 'http://music.163.com/api/artist/top?offset=0&limit=100&total=false'
