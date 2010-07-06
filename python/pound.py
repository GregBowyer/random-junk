import urllib
import urllib2

url = 'http://127.0.0.1:8080/v1/services/clickThroughRate/impression'

headers = { 'Content-Type' : 'application/xml', 'Accept' : 'text/javascript, text/xml, application/xml, text/plain, */*' }

fp = open('/home/greg/downloads/impression.xml')
data = fp.readlines()
fp.close()

for i in xrange(1, 10000):

    req = urllib2.Request(url, '\n'.join(data), headers)
    res = urllib2.urlopen(req)
    print res.read()
