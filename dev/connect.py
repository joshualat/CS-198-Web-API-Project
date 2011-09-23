"""import httplib, urllib, urllib2
params = urllib.urlencode({'message': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}
conn = httplib.HTTPConnection("127.0.0.1:8000")
conn.request("POST", "/usb/test", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()"""

"""
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"}

proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)
print opener.open("http://localhost:8000/usb/test").read(100)"""

import urllib
import urllib2

"""
#url = 'http://localhost:8000/usb/test'
url = 'http://www.google.com'
values = {'message' : 'some test message' }

data = urllib.urlencode(values)
print data
#req = urllib2.Request(url, data)
#response = urllib2.urlopen(req)
#the_page = response.read()

proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)
#print opener.open(url,data).read(100)
print opener.open(url).read(100)"""

data = urllib.urlencode({'message': 'Status'})
u = urllib2.urlopen('http://localhost:8000/usb/test?'+data)
print u.read()

