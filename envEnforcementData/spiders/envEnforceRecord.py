# -*- coding: utf-8 -*-
import scrapy


class EnvenforcerecordSpider(scrapy.Spider):
    name = 'envEnforceRecord'
    allowed_domains = ['gov.cn']
    start_urls = ['http://gov.cn/']

    def parse(self, response):
        pass
