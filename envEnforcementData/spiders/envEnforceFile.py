# -*- coding: utf-8 -*-
import scrapy
from scrapy import  Request
from urllib.parse import urlparse, urljoin
from datetime import datetime
import pandas as pd; import numpy as np
import json
from bs4 import BeautifulSoup

from envEnforcementData.utils import loadEntryUrls
from envEnforcementData.settings import ENTRY_URLS_FILE


class EnvenforcefileSpider(scrapy.Spider):
    name = 'env_enforce_file'
    allowed_domains = ['gov.cn']
    

    def start_requests(self):
        self.urls_df = loadEntryUrls(ENTRY_URLS_FILE)
        urls = []
        for i in range(self.urls_df.shape[0]):
            urls.append(Request(
                url = self.urls_df.loc[i, 'APILink'],
                dont_filter=True, meta={'try':'firstTry'}))
        #print(self.urls_df)
        #print(self.urls_df['APILink'])
        print(urls)
        return urls
    
    def parse(self, response):
        print(response.status)
        print(response.url)
        print(response.meta)
        pass

    
    def get_location(self, url):
        pass
