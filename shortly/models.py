import datetime

from flask import abort
from redis import Redis

from exceptions import URLExistsException

class Url(object):
    def __init__(self, short_url=None, request=None):
        self.r = Redis(db=0)
        
        self.short_url = short_url
        if self.short_url is not None:
            long_url = self.r.get('url:%s:long_url' % self.short_url)
            if long_url is not None:
                self.long_url = long_url
            else:
                abort(404)
            self.canonical = self.r.hget('global:url', self.long_url)

        if request is not None:
            self.r.zincrby('hits', self.canonical)
            if self.canonical != self.short_url:
                self.r.zincrby('hits', self.short_url)

        if self.short_url is not None:
            self.hits = int(self.r.zscore('hits', self.short_url))
            self.canonical_hits = int(self.r.zscore('hits', self.canonical))

    def alternates(self):
        alternate_urls = self.r.smembers('url:%s:alternates' % self.canonical)
        for url in alternate_urls:
            yield (url, int(Url(url).hits))
            
    def shorten(self, long_url, short_url=''):
        self.long_url = long_url
        exists = self.r.hexists('global:url', long_url) is True
        if exists:
            canonical = self.r.hget('global:url', long_url)
        else:
            canonical = '%x' % self.r.incr('next.url.id')
            self.r.hset('global:url', long_url, canonical)
            self.r.set('url:%s:long_url' % canonical, long_url)
            self.r.set('url:%s:created' % canonical, datetime.datetime.now())
            
        if short_url != '':
            if self.r.exists('url:%s:long_url' % short_url) == 1:
                existing_long = self.r.get('url:%s:long_url' % short_url)
                msg = 'The custom shortened URL "%s" already exists and' \
                    ' is pointing to %s.' % (
                    short_url,
                    existing_long,
                    )
                raise URLExistsException(msg)
            self.r.set('url:%s:long_url' % short_url, long_url)
            self.r.sadd('url:%s:alternates' % canonical, short_url)
            self.long_url = long_url
        else:
            short_url = canonical

        return short_url
