import asyncore
import sys
import itertools
from SimpleAsyncHTTP import AsyncHTTP
from multiprocessing import Pool, Process

from time import time
import os

#host = 'http://greg-perf-tuning-fwdsrv.shopzilla.laxhq:7117/'
#host = 'http://ctrfwdstagevip.sl1.shopzilla.seastg:7117/'
#host = 'http://10.40.212.89:7117/'
#uri = host + 'services/clickrate/v3/services/clickThroughRate/trackingEvent?logToFile=true'

host = 'http://10.40.45.74:8086/'
uri = host + 'v3/services/clickThroughRate/trackingEvent?logToFile=true'

#host = 'http://127.0.0.1:8080/'
#uri = host + 'v3/services/clickThroughRate/trackingEvent?logToFile=true'

data = '''
<ctr:event xmlns:ctr="http://www.shopzilla.com/services/clickrate"
    ctr:type="IMPRESSION"
    ctr:brand="BR"
    ctr:country="7Y"
    ctr:session="421653456124564"
    ctr:request="req12222">
    <ctr:page ctr:token="7Y" ctr:template="hotSearch.html" ctr:number="3" ctr:itemsPerPage="30">
        <ctr:pod ctr:name="productListpod"
            ctr:template="pods/productListpod.html">
            <ctr:list ctr:name="visible">
                %s
            </ctr:list>
        </ctr:pod>
    </ctr:page>
</ctr:event>
'''

item = '''
<ctr:item
    ctr:seq="12" ctr:id="%s"
    ctr:type="OFFER" ctr:brand="4567"
    ctr:mid="1234" ctr:cat="3254"
    ctr:rel="1234.999"/>
'''

class TestChecker(object):
    '''Simple class that serves as the callback / errback for asynccore
        allowing us to consume the response without having to serialise on
        the I/O'''

    def __init__(self):
        self.num = 0

    def http_header(self, request):
        '''Handles the header checking for sucess from the host'''
        if request.status is None:
            raise IOError('No connection !')
        else:
            #print "status", "=>", request.status
            if request.status != '200':
                raise IOError('Error in request: ' + request.data) 

    def feed(self, data):
        '''Handle incoming data, which may 'dribble' from the host'''
        print len(data)

    def close(self):
        ''' Handles the end of data / socket fin'''
        self.num += 1
        #print 'Request: %s-%s' %(os.getpid(), self.num)

def run(worker_num, start):
    '''Entry point for forked subworkers, effectivly handles the child end of the 
        fork() call'''

    checker = TestChecker()
    ticker = 0
    pid = os.getpid()

    for i in xrange(start, start * 100000):
        
        t = time()

        requests = []
        for j in xrange(BATCH_SIZE):
            #print [i + j * x for x in xrange(20)]
            items = '\n'.join([item %(i + j * x ) for x in xrange(20)])
            post_data = data %(items)
            requests.append(AsyncHTTP(uri, post_data, checker))
            # Run asynccore for the batchsize, this blocks while 
            # the select() loop handles the associated channels 
        asyncore.loop()

        ticker += BATCH_SIZE

        print "Worker [%s] managed %s requests in %s" %(pid, str(BATCH_SIZE), time() - t)
        print "Total requests for worker [%s] so far : %s" %(pid, ticker)
    return

if __name__ == '__main__':

    # The size of batches that each worker will fire async to the host
    # this is done with select() / asyncore so care should be taken not 
    # to annilate the remote since the client can generate a _lot_ of traffic
    BATCH_SIZE = 50

    # Number of parallel workers to fork on the OS
    NUM_WORKERS = 3

    # Number of requests to service per worker
    NUM_REQUESTS = 100000

    workers = []
    splits = zip(itertools.count(), xrange(1, NUM_REQUESTS * NUM_WORKERS, NUM_REQUESTS))
    for worker_num, start in splits:
        worker = Process(target=run, args=(worker_num, start))
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()

    #pool.map(run, xrange(1, NUM_WORKERS, NUM_REQUESTS), 1)
