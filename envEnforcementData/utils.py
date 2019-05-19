
import os, time, datetime
import os.path as osp
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, urlencode, unquote, quote, ParseResult
import re
from copy import copy
from bs4 import BeautifulSoup
import json,yaml

import pandas as pd
from validators.url import url as valid_url

from envEnforcementData import settings
from envEnforcementData.types import EntryNextResponse, EntryStartRequest

import logging
logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    filename=osp.join(settings.LOG_FOLDER, 'global_utils.log'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('Global Utils')

###############################################################################
#                                General Utils                                 #
###############################################################################


def get_url_last_path(url):
    ''' Get last split of url path
    
    Args: 
        url(str)

    Return:
        str (last path split)
    '''
    parsed = urlparse(url).path.split('/')
    return parsed[-1]


def build_new_url_from_parsed(parsed_url, options=None):
    ''' Build new URL from a parsed url object, options could overwrite the configuration in parsed object

    Args:
        parsed_url(object): ParseResult Object, See `urllib.parse` for more details
        options(dict): Overwrite options, will overwrite the same key name value in parsed_url object. 

    Return:
        str(new URL): new URL built
     '''

    # As `urllib.parse.ParseResult` is a named tuple, we need rebuild it
    new_scheme = options.get('scheme', '') if options.get(
        'scheme', '') or options.get('scheme', '') != '' else parsed_url.scheme
    new_netloc = options.get('netloc', '') if options.get(
        'netloc', '') or options.get('netloc', '') != '' else parsed_url.netloc
    new_path = options.get('path', '') if options.get(
        'path', '') or options.get('path', '') != '' else parsed_url.path
    new_params = options.get('params', '') if options.get(
        'params', '') or options.get('params', '') != '' else parsed_url.params
    new_query = options.get('query', '') if options.get(
        'query', '') or options.get('query', '') != '' else parsed_url.query
    new_fragment = options.get('fragment', '') if options.get(
        'fragment',
        '') or options.get('fragment', '') != '' else parsed_url.fragment

    #print((new_scheme, new_netloc, new_path, new_params, new_query,
    #       new_fragment),
    #      (type(new_scheme), type(new_netloc), type(new_path),
    #       type(new_params), type(new_query), type(new_fragment)))
    new_url = ParseResult(
        scheme=new_scheme,
        netloc=new_netloc,
        path=new_path,
        params=new_params,
        query=new_query,
        fragment=new_fragment)

    return new_url.geturl()

def get_file_updated_time(filePath):
    ''' Get a file modified time
    
    Args:
        filePath(str):\
    
    Return:
        datetime.datetime(Last Modifiedtime)
    '''
    if osp.exists(filePath):
        modified_status = os.stat(filePath)[-2]
        modified_timestamp = os.stat(filePath).st_mtime
        modified_time = datetime.datetime.fromtimestamp(modified_timestamp)
        return modified_time
    else:
        return None

###############################################################################
#                     Environment Enforcement File Utils                      #
###############################################################################


# Loading Entry Url ###########################################################
def loadEntryUrls(path):
    ''' Loading Entry URL excel file
    
    Args:
        path(str): Configured excel file path

    Return:
        pandas.DataFrame(Entry URL file): must have 'APILink' column. See `EnvenforcefileSpider.start_requests` for more details

    '''
    if osp.exists(path):
        df = pd.read_excel(path)
        print('[Entry URL File, "utils.py"]', settings.ENTRY_URLS_FILE)
        return df
    else:
        raise Exception('No configured Entry URL file!!!!!!!!!!')


# Handling XHR Response #######################################################
def extract_url_and_title_from_xhr(response):
    ''' Extract URL and title from XHR response
    
    Args:
        response(scrapy.http.Response): an XHR Response, must be in the `TextResponse` subclass

    Return:
        list(Crawlwed url & title): in `[{url:..., title:...}, ...]` format
    '''
    data = []
    response_data = text_response_to_json(response)
    for i in response_data['docs']:
        if valid_url(i.get('url', None) if i.get('url', False) else i.get('url2', None)):
            data.append({
                'url': i.get('url', None) if i.get('url', False) else i.get('url2', None),
                'title': i.get('title', None) if i.get('title', False) else i.get('title2', None)
            })
    return data

def text_response_to_json(response):
    ''' Convert an XHR response text to JSON object

    Args:
        response(scrapy.http.Response): an XHR Response, must be in the `TextResponse` subclass

    Return:
        dict (JSON object)
    '''
    return json.loads(
        re.sub(
            r'\s+', '',
            re.sub("#'", '#"',
                   re.sub("'#", '"#', re.sub(r'\n', '', response.text)))))

def is_query_dict_from_xhr(d):
    ''' Judging whether a query dict is from XHR Response
    
    Args:
        d(dict): query dict

    Return:
        boolean(True/False): True-xhr response, False-not xhr response
    '''
    return d.get('prepage', None) and d.get('page', None)


def is_xhr_response_pattern(response):
    ''' Judging whether a response is XHR type
    
    Args:
        response(scrapy.http.Response): an Response object    
    d(dict): query dict

    Return:
        boolean(True/False): True-xhr response, False-not xhr response
    '''
    parsed_url = urlparse(response.request.url)
    query_dict = parse_qs(parsed_url.query)
    return query_dict.get('prepage', None) and query_dict.get('page', None)

# Handling Static Page ########################################################
def extract_url_and_title_from_static_page(response):
    ''' Extract title and url for a static page response
    
    Args:
        response(scrapy.http.Response): an Static HTML Response, must be in the `TextResponse` subclass

    Return:
        list(Crawlwed url & title): in `[{url:..., title:...}, ...]` format
    '''
    data = []
    ul_li_a = response.xpath('//ul/li/a')
    for i in ul_li_a:
        url = i.xpath('@href').extract()
        title = i.xpath('@title').extract()
        if len(title) < 0:
            title = i.xpath('text()').extract()
        if len(url) > 0 and len(title) > 0:
            url__ = urljoin(response.request.url, url[0])
            if valid_url(url__):
                data.append({
                    'url':url__,
                    'title':title[0]
                }) 
    return data
    

def is_static_html_url_parttern(response):
    ''' Judging if a response is static type
    
    Args:
        response(scrapy.http.Response): an Response object    
    d(dict): query dict

    Return:
        False/dict(matched result):  the matched information{match:<re.match>Obj/None,pageNumebr:<int>}
    '''
    parsed_url = urlparse(response.request.url)
    # if the request url has query parameters, it isn't a static page
    if not parsed_url.query == '':
        return False
    last_path = get_url_last_path(response.request.url)
    # Currently there are 3 patterns for static page:
    #   1. index.htm index_1.htm
    #   2. list.htm list_1.htm
    #   3. news-179-1.htm, news-179-2.htm ...
    index_pattern_match = re.match(r'.*?index_?(?P<number>\d*)\.htm', last_path)
    list_pattern_match = re.match(r'.*?list_?(?P<number>\d*)\.htm', last_path)
    special179_pattern_match = re.match(r'.*news-179-(?P<number>\d*)\.htm', last_path)
    match = index_pattern_match or list_pattern_match or special179_pattern_match
    try:
        if not match:
            # If not match, raise Exception
            raise Exception('Static URL pattern parse error, maybe a new static URL pattern')
    except Exception as e:
        with open('urlpattern.log','a') as f:
            logInfo = "-"*20 + '\n'
            logInfo += str(e) + '\n'
            logInfo += 'whole URL: ' + response.request.url + '\n'
            logInfo += 'last path: ' + last_path +'\n'
            print(logInfo)
            f.write(logInfo)
            
    number = int(match.group('number')) if match.group('number') else None
    return {
        'match': match if match else None,
        'pageNumebr': number
    }

# Handling Simple Dynamic Page ################################################
def is_simple_dynamic_url_pattern(response):
    #TODO
    return False
def extract_url_and_title_from_simple_dynamic(response):
    #TODO
    return False
# Entry URL start request #####################################################
def enforcement_file_entry_start_request(url):
    #TODO
    ''' Given Enforcement File Entry URL, analyze the url pattern and format it to start 
    See `settings` EEFEUF section for more details.
    Environment Enforcement File Entry URL Formatting


    Args:
        url(str): entry url string

    Return:
        EntryStartRequest(formatted url, dict object): dict object includes parameters that will be passed to `Request.meta`
        See `envEnforcementData.types.EntryStartRequest` for more details.

    '''
    parsed_url = urlparse(url)
    query_dict = parse_qs(parsed_url.query)

    # Detect XHR request feature, if XHR request, get JSON
    if is_query_dict_from_xhr(query_dict):
        new_query_dict = copy(query_dict)
        new_query_dict['prepage'] = ['2000']
        new_query_dict['page'] = ['1']
        for k in new_query_dict.keys():
            new_query_dict[k] = ','.join(new_query_dict[k])
        new_url = build_new_url_from_parsed(
            parsed_url,
            {"query": unquote(urlencode(new_query_dict, quote_via=quote))})
        return EntryStartRequest(new_url, {
            'prepage': 2000,
            'page': 1,
            'enforceFileType': 'xhr'
        })

    return EntryStartRequest(url, {})


# Entry URL next steps ########################################################
def enforcement_file_entry_response_next(response):
    #TODO
    ''' Given Enforcement File Response, analyze the response and decide what to do

    Args:
        response(scrapy.http.Response): response after spider & downloader middleware

    Return:
        EntryNextResponse(EEFRO code, extracted information from the response): the extracted information is in two formats // 1. XHR JSON, 2. list of dict object {url: '', title: ''}
        See `envEnforcementData.types.EntryNextResponse` for more details

    '''
    
    # Detect XHR request feature, if XHR request, get JSON
    if is_xhr_response_pattern(response):
        data = extract_url_and_title_from_xhr(response)
        return EntryNextResponse(
            code=settings.EEFRO_NO_NEXT_TRY,
            data=data)
    if is_static_html_url_parttern(response):
        data = extract_url_and_title_from_static_page(response)
        print('-'* 20, data)
        return EntryNextResponse(
            code=settings.EEFRO_BUILD_NEXT_REQUEST_STATIC,
            data=data
        )
    if is_simple_dynamic_url_pattern(response):
        data = extract_url_and_title_from_simple_dynamic(response)
        return EntryNextResponse(
            code=settings.EEFRO_BUILD_NEXT_REQUEST_SIMPLE_DYNAMIC,
            data=data
        )
    
    return EntryNextResponse(
        code='',
        data='')


# Downloader Middleware Utils #################################################


def response_storage_path_generator(settings, url, meta, suffix='.pkl'):
    ''' Set a unique storage path for one response

    Args: 
        settings(spider.Settings): spider settings
        url(str): request url
        meta(Request.meta): a dict like meta
        suffix(str): suffix add to the saved file

    Return:
        str(A unique file storage path based on the request)
    '''
    meta_ = dict(meta)
    logger.info('*'*20 + str(meta) + str(meta_))
    meta_str = '___meta___'
    for k in meta_.keys():
        if k not in settings['DOWNLOADER_MIDDLEWARE_STORE_EXCLUDE']:
            v = meta_[k]
            if  isinstance(v, (tuple, list)):
                v = ','.join(v)
            meta_str += k + '_' + str(v) + '__'
            
            #logger.error(type(v))
            #raise Exception('Unable to deal this type in meta')
            
    storage_path = osp.join(
        settings['DOWNLOAD_FOLDER'],
        urlparse(url).netloc + urlparse(url).path.replace('/', ':') + quote(meta_str)
        + suffix)
    return storage_path


def main():
    loadEntryUrls('../entryUrls.xlsx')


if __name__ == '__main__':
    main()
