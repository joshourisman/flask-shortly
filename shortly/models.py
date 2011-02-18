from redis import Redis

import datetime

class Url(object):
    def __init__(self, short_url=None):
        self.r = Redis(db=0)
        
        if short_url is not None:
            self.short_url = short_url
            self.long_url = self.r.get('url:%s:long_url' % self.short_url)

    def shorten(self, long_url, short_url=''):
        if short_url == '':
            url_hash = '%x' % self.r.incr('next.url.id')
        else:
            url_hash = short_url
            
        self.r.set('url:%s:long_url' % url_hash, long_url)
        self.r.set('url:%s:created' % url_hash, datetime.datetime.now())
        self.r.set('url:%s:short_url'% long_url, url_hash)
        self.r.push('global:urls', url_hash)
        return url_hash
