# -*- coding: utf-8 -*-
import scrapy


class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['shiyanlou.com']
    start_urls = ['http://shiyanlou.com/']

    def parse(self, response):
        pass
