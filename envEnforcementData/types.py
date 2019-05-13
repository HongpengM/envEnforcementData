from collections import namedtuple

__all__ = ['EntryStartRequest','EntryNextResponse']
EntryNextResponse = namedtuple('EntryNextResponse', ['code','data'])
EntryStartRequest = namedtuple('EntryStartRequest',['url','meta'])
