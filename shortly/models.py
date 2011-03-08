import datetime

from flask import abort
from redis import Redis

from exceptions import URLExistsException

class Url(object):
    def __init__(self, short_url=None):
        self.r = Redis(db=0)
        
        if short_url is not None:
            self.short_url = short_url
            long_url = self.r.get('url:%s:long_url' % self.short_url)
            if long_url is not None:
                self.long_url = long_url
            else:
                abort(404)
            self.canonical = self.r.get('url:%s:canonical' % self.short_url)
            self.alternates = self.r.smembers('url:%s:alternates' % \
                                                  self.canonical)

    def shorten(self, long_url, short_url=''):
        self.long_url = long_url
        exists = self.r.hexists('global:urls', long_url) == True
        if exists:
            canonical = self.r.hget('global:urls', long_url)
        else:
            canonical = '%x' % self.r.incr('next.url.id')
            self.r.hset('global:url', long_url, canonical)
            self.r.set('url:%s:long_url' % canonical, long_url)
            self.r.set('url:%s:created' % canonical, datetime.datetime.now())
            self.r.set('url:%s:canonical'% short_url, canonical)
            
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
            self.r.set('url:%s:canonical' % short_url, canonical)
            self.r.sadd('url:%s:alternates' % canonical, short_url)
            self.long_url = long_url

        return canonical
