# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from os import path as osp; import os
from urllib.parse import urlparse
import pickle

from envEnforcementData.settings import LOG_FOLDER
import envEnforcementData.utils as utils
import logging
logging.basicConfig(level=logging.INFO,
                    filemode='w',
                    filename=osp.join(LOG_FOLDER, 'download_middleware.log'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('downloadMiddleware')

class EnvEnforcementFileDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # Use store response first ############################################
        # Store it to download folder using `pickle`
        # If find stored, raise `IgnoreRequest` Exception and restore in exception handling
        # Else pass `downloaded_request_path` and `page` parameters to response and serialize response
        
        # Pass response path through request.meta
        # path constructing: DOWNLOAD_FOLDER + netloc + path + (page) + '.pkl'
        logger.info(request.meta)
        logger.info(utils.response_storage_path_generator(spider.settings,
                                                          request.url,
                                                          request.meta))
        downloaded_request_path = utils.response_storage_path_generator(spider.settings,
                                                          request.url,
                                                          request.meta)
        request.meta['store_path'] = downloaded_request_path
        # If find stored response, restore it!
        if osp.exists(downloaded_request_path):
            logger.info('File already downloaded:' + downloaded_request_path)
            raise IgnoreRequest('existed|' + downloaded_request_path)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

       

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.



        # If the exception is to restore the pre-downloaded response
        # Restore it!
        print(exception)
        response_path = request.meta['store_path']
        response = None
        if osp.exists(response_path):
            with open(response_path,'rb') as f:
                response = pickle.load(f)
        if response:
            return response

        
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
