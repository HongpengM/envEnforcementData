import pandas as pd
import os
import os.path as osp
import yaml
from urllib.parse import urlparse, urljoin, urlencode, parse_qs, urlencode, unquote, quote, ParseResult
from envEnforcementData import settings
import re
import json
from bs4 import BeautifulSoup
from copy import copy
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
    ''' Judging if a urlparse.query dict is from an XHR Response
    
    Args:
        d(dict): query dict

    Return:
        boolean(True/False): True-xhr response, False-not xhr response
    '''
    return d.get('prepage', None) and d.get('page', None)


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
    parsed_url = urlparse(response.request.url)
    query_dict = parse_qs(parsed_url.query)
    # Detect XHR request feature, if XHR request, get JSON
    if is_query_dict_from_xhr(query_dict):
        return EntryNextResponse(
            code=settings.EEFRO_NO_NEXT_TRY,
            data=text_response_to_json(response))

    return EntryNextResponse(
        code=parsed_url.query, data=parse_qs(parsed_url.query))


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
