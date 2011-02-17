from redis import Redis

class Url(object):
    def __init__(self, short_url):
        self.r = Redis(db=0)
        self.s = short_url

    @property
    def short_url(self):
        return self.s

    @property
    def long_url(self):
        return 'http://www.google.com'
