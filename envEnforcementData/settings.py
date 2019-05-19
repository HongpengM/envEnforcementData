# -*- coding: utf-8 -*-
# Import Shell Utils Library
from shutil import which



# Scrapy settings for envEnforcementData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'envEnforcementData'

SPIDER_MODULES = ['envEnforcementData.spiders']
NEWSPIDER_MODULE = 'envEnforcementData.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'envEnforcementData (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#   'envEnforcementData.middlewares.EnvenforcementdataSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

# Scrapy-Selenium configuration
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS=['-headless']  # '--headless' if using chrome instead of firefox

DOWNLOADER_MIDDLEWARES = {
#    'envEnforcementData.middlewares.EnvenforcementdataDownloaderMiddleware': 543,
    'random_useragent.RandomUserAgentMiddleware': 400,
}
USER_AGENT_LIST = "./user-agents.txt"

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'envEnforcementData.pipelines.EnvenforcementdataPipeline': 300,
    'envEnforcementData.pipelines.MongoStoragePipeline':300,
}
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DB = 'envPunishment'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


###############################################################################
#                           Project Scope Definition                          #
###############################################################################

ENTRY_URLS_FILE = 'entryUrls_minimal2.xlsx'
FORCE_UPDATE_ENTRY_PICKLE = False
DOWNLOAD_FOLDER = './download'
LOG_FOLDER ='./logs'
# Environment Protection File Response

# Environment Protection Enforcement File Settings
EPEF_FILE_RESPONSE_TYPE = ['json', 'html', 'xls','xlsx', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'csv', 'undefined']


# Environment Protection Enforcement Record Settings
EPER_RECORD_PAGE_TYPE = ['htmlTable', 'text', 'pdf', 'png', 'jpg', 'jpeg', 'xls', 'xlsx', 'doc', 'docx', 'undefined']

EPER_ENTITY_TYPE = ['person', 'organization', 'company','institution']
EPER_ENTITY_CODE_TYPE = ['统一社会信用代码', '营业执照']

# Environment Enforcement File Entry URL Formatting
EEFEUF_XHR_REQUEST = 'xhr_request'


# Environment Enforcement File Request Try Order
EEFRO_FIRST_TRY = 'first-try'
EEFRO_NO_NEXT_TRY = 'no-next-try'
EEFRO_BUILD_NEXT_REQUEST_PARAM = 'build-next-request-param'
EEFRO_BUILD_NEXT_REQUEST_STATIC = 'build-next-request-static'
EEFRO_USE_SELENIUM = 'use-selenium'

