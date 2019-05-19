# -*- coding: utf-8 -*-
import scrapy
from scrapy import  Request
from urllib.parse import urlparse, urljoin
from datetime import datetime
import pandas as pd; import numpy as np
import json
from bs4 import BeautifulSoup

import envEnforcementData.utils as utils 
import envEnforcementData.settings as settings
import envEnforcementData.items as items
from envEnforcementData.keywords import GLOBAL_KEYWORDS_LIST


class EnvenforcefileSpider(scrapy.Spider):
    name = 'env_enforce_file'
    allowed_domains = ['gov.cn']
    # Customized Settings, Use spider-specific Middleware
    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'envEnforcementData.middlewares.EnvEnforcementFileSpiderMiddleware': 543,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'envEnforcementData.middlewares.EnvEnforcementFileDownloaderMiddleware': 543,
            'random_useragent.RandomUserAgentMiddleware': 400,
        },
        'DOWNLOADER_MIDDLEWARE_STORE_EXCLUDE':['download_timeout',
                                               'download_slot',
                                               'download_latency',
                                               'store_path',]

    }

    def start_requests(self):
        self.urls_df = utils.loadEntryUrls(settings.ENTRY_URLS_FILE)
        urls = []
        for i in range(self.urls_df.shape[0]):
            meta = {'EEFRO': self.settings.get('EEFRO_FIRST_TRY')}
            url = self.urls_df.loc[i, 'APILink']
            formatted_url, extra_meta = utils.enforcement_file_entry_start_request(url)
            meta['Keywords'] = self.urls_df.loc[i, 'Keywords']
            for i in extra_meta.keys():
                meta[i] = extra_meta[i]
            urls.append(Request(
                url = formatted_url,
                dont_filter=True, meta=meta))
        #print(self.urls_df)
        #print(self.urls_df['APILink'])
        print(urls)
        return urls


    def parse(self, response):
        print('response status', response.status)
        print('response url', response.url)
        print('response meta', response.meta)
        print('response last path', utils.get_url_last_path(response.url))
        code, data=utils.enforcement_file_entry_response_next(response)
        # print('response content', response.text)
        print(data)
        print('response next step', code)

        #TODO
        if code == settings.EEFRO_BUILD_NEXT_REQUEST_STATIC:
            pass
        if code == settings.EEFRO_BUILD_NEXT_REQUEST_SIMPLE_DYNAMIC:
            pass
        if code == settings.EEFRO_USE_SELENIUM:
            pass
        print('Count ', len(data))

        # Extract EnvEnforcementFileItem
        for d in data:
            item = items.EnvEnforcementFileItem()
            keywords_list = response.meta['Keywords'].split(';') + GLOBAL_KEYWORDS_LIST
            keywords_hit = []
            for keyword in keywords_list:
                if keyword in d['title']:
                    keywords_hit.append(keyword)
            item['createdAt'] = datetime.now()
            item['updatedAt'] = datetime.now()
            item['pageLink'] = d['url']
            item['pageTitle'] = d['title']
            item['keywordHit'] =keywords_hit
            if len(keywords_hit) > 0:
                print(keywords_hit)
                print('='*20, 'Items: ',item)
                yield item
        pass


    def next_static_page(self, response):
        pass
    
    def get_location(self, url):
        pass
