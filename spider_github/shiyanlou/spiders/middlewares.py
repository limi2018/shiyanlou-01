# -*- coding: utf-8 -*-
from scrapy import signals
import scrapy
from shiyanlou.items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['shiyanlou.com']
   # start_urls = ['http://shiyanlou.com/']


    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        for course in response.css('div.course-body'):
            item = CourseItem({
                                'name': course.css('div.course-name::text').extract_first(),                                                                        
                                'id': course.css('div.course-desc::text').extract_first(),
                                'update_time': course.css('div.course-desc::text').extract_first()                                                                                                         'type': course.css('div.course-footer span.pull-right::text').extract_first(default='??'),                                                                                     'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*') 
                               })
            yield item
