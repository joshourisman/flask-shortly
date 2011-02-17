from redis import Redis

class Url(object):
    def __init__(self, short_url=None):
        self.r = Redis(db=0)
        
        if short_url is not None:
            self.s = short_url
            self.l = self.r.get('url:%s:id' % self.s)

    @property
    def short_url(self):
        return self.s

    @property
    def long_url(self):
        return 'http://www.google.com'

    def shorten(self, long_url):
        url_hash = '%x' % self.r.incr('next.url.id')
        self.r.set('url:%s:id' % url_hash, long_url)
        self.r.push('global:urls', url_hash)
        return url_hash
