import urllib
import urllib2
import webbrowser

# ConnectTools Class

class ConnectTools(object):

    """
    ConnectTools class

    Usable functions:
        request_get
        request_post
        browser_open
    """

    @classmethod
    def request_get(cls,url,params={}):
        data = urllib.urlencode(params)
        return urllib2.urlopen(url + "?" + data).read()

    @classmethod
    def request_post(cls,url,params={}):
        data = urllib.urlencode(params)
        return urllib2.urlopen(url, data).read()

    @classmethod
    def browser_open(cls,url,params={}):
        data = urllib.urlencode(params)
        web_url = url + "?" + data
        webbrowser.open(web_url)
        return web_url

