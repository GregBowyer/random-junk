from httplib2 import Http
import lxml.etree as etree

from time import sleep, time

import traceback

import unicodedata

from multiprocessing import JoinableQueue, Pool, Process

from Queue import Empty, Full

from urllib import urlencode
from urllib import quote_plus as quote

# The SAS instance / cluster to make API calls against
SAS_BASE = 'http://sasvip.sl2.shopzilla.seastg:7033/services/aggregator/v5/US/12'
SAS_BASE = 'http://127.0.0.1:6081/services/aggregator/v5/US/12'

# The number of processes that will be spawned to perform classify / search
# requests on SAS
# Be very careful with this setting it can drematically effect SAS cluster performance
NUM_FETCHERS = 24

# The data sets that we want to use for related searches
# One file will be created for each of these
DATA_SETS = (5, 10, 20, 25, 30, 40, 50, 60, 80, 100)

# The maximum amount of results to pull from SAS
MAX_FETCH = DATA_SETS[-1]

# Very important !
# The amount of time to wait in a worker between SAS api calls
# SAS appears to scale very badly to this program, so a wait is 
# essential to avoid harming the SAS cluster
SAS_RECOVERY_TIME = 0.4

# Enabled to monitor the average response time from SAS
# Should the time start to climb above the set values then
# backoff will be enabled and the script will increase the recovery time
# by the given amount
SAS_BACKOFF_ENABLED = True

# If a SAS query takes more than 500 ms, increase the RECOVERY_TIME by 
# a configured amount
SAS_BACKOFF_THRESHOLD = 2000

# Start reducing backoff when we hit this
SAS_BACKOFF_LOW_WATER_MARK = 700

# Increase the recovery time for SAS by the given amount if backoff kicks in
SAS_BACKOFF_RECOVERY_INCREASE = 0.1

# Decrease the recovery time for SAS by the given amount
SAS_BACKOFF_RECOVERY_DECREASE = 0.05

# When backoff happens immediatly pause for n secs to allow SAS to recover
SAS_BACKOFF_PAUSE_TIME = 0.5

# The following do not need to be adjusted
NAMESPACES = {
    'n' : 'http://www.shopzilla.com/services/aggregator'
}

STD_HEADERS = {
    'Accept' : 'application/xml,application/xhtml+xml,text/xml',
    'User-Agent' : 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.38 Safari/533.4',
}

def classify(query, 
        opss_path = etree.XPath('//*/n:classification/n:optimizer_metadata', namespaces = NAMESPACES),
        principal_cid_path = etree.XPath('//*/n:categories/n:category[1]/@id', namespaces = NAMESPACES),
        host=SAS_BASE + '/query_classification'):

    params = {
        'top_categories' : '1',
        'top_products' : '1',
        'rev' : '0',
        'search_conf_plugin' : '28',
        'search_conf_pid_weight' : '7',
        'search_conf_field_weight' : '10',
        'relevancy_score' : True,
        'search_meta' : True,
        'optimizer_meta' : True,
        'keyword' : query,
        #'ds' : 'astrobds001.shopzilla.laxhq:7005',
    }

    classification_search = '?'.join((host, urlencode(params)))

    h = Http()
    res, content = h.request(classification_search, headers=STD_HEADERS)

    if res.status > 400:
        raise Exception("Invalid response from classify: {%s} response: {%s}" %(sas_search, content))

    root = etree.fromstring(content)

    opss = opss_path(root)

    if opss and opss[0].attrib['status'] == 'R' :
        cid = opss[0].attrib['cid']
        if cid:
            return classification_search, cid
    
    return classification_search, principal_cid_path(root)[0]

def search(cid, phrase, 
    titles = etree.XPath('//*/n:title/text()', namespaces = NAMESPACES),
    host = SAS_BASE + '/product_search'):
    
    params = {
        'search_conf_pid_weight' : '7',
        'search_conf_field_weight' : '10',
        'skip' : '0',
        'rev_config' : '3:250,250,250',
        'search_conf_plugin' : '28',
        'append' : 'csp_data',
        'relevancy_config' : '1',
        'backfill' : '0:40',
        'search_meta' : True,
        'top' : MAX_FETCH,
        'keyword' : phrase,
        'cid' : cid,
        #'ds' : 'astrobds001.shopzilla.laxhq:7005',
    }

    sas_search = '?'.join((host, urlencode(params)))
    h = Http()
    res, content = h.request(sas_search, headers=STD_HEADERS)

    if res.status > 400:
        raise Exception("Invalid response from search request: {%s} response: {%s}" %(sas_search, content))

    root = etree.fromstring(content)
    return sas_search, titles(root)

def construct_rel_search_url(titles, cid, num_titles,
    url_template='/solr/v2/analyzed?phrase=%s&cid=%s&grp=12&num=5&wt=xml&indent=on\n'):

    unicode_safe_titles = (unicodedata.normalize('NFKC', unicode(title)).encode('latin9', 'ignore') \
            for title in titles[:num_titles])
    encoded_titles = (quote('"%s"' % title) for title in unicode_safe_titles)
    stripped_titles = (encoded_title.replace('/','').replace('"', '') for encoded_title in encoded_titles)
    search_titles = ';'.join(encoded_titles)
    return url_template %(search_titles, cid) 

def search_terms(input, allowed_locales = ('US')):

    with open(input, 'r') as search_log:
        line_nu = 0
        for line in search_log:
            try:
                line_nu += 1
                tokens = line.strip().split('\t')
                type = tokens[-1]

                if type == 'PRODUCT':
                    term = tokens[16]
                    country = tokens[9]

                    if country in allowed_locales:
                        yield term.strip()
            except Exception as e:
                print 'Broken line in search log: ' + str(line_nu)
                traceback.print_exc(e)

def reject(reject_queue, reject_file):
    with open(reject_file, 'w+') as fp:
        while True:
            item = reject_queue.get()
            print 'Rejecting term ' + item
            fp.write(item)
            fp.write('\n')
            fp.flush()

def manage_backoff(request, last_req_time):

    global SAS_RECOVERY_TIME
    
    if SAS_BACKOFF_ENABLED and last_req_time > SAS_BACKOFF_THRESHOLD:
        SAS_RECOVERY_TIME += SAS_BACKOFF_RECOVERY_INCREASE

        print '********************************************************************************'
        print 'WARNING: SAS BACKOFF IN EFFECT !'
        print 'Time taken %s  - Last Request %s' %(str(last_req_time), request)
        print 'Adjusted backoff time to %s' %str(SAS_RECOVERY_TIME)
        print 'Waiting out for %s seconds to recover' %str(SAS_BACKOFF_PAUSE_TIME)

        sleep(SAS_BACKOFF_PAUSE_TIME)
    elif SAS_BACKOFF_ENABLED and last_req_time < SAS_BACKOFF_LOW_WATER_MARK:
        if SAS_RECOVERY_TIME > 0.1:
            SAS_RECOVERY_TIME -= SAS_BACKOFF_RECOVERY_DECREASE
    else:
        sleep(SAS_RECOVERY_TIME)


def fetch(fetch_queue, write_queues, reject_queue, num):
    
    print 'Fetcher ' + str(num)

    while True:
        try:
            term = fetch_queue.get()[0]
            print 'Fetcher [%s] - %s' %(str(num), term)
            # DO NOT REMOVE THESE SLEEPS !
            # Turns out even with a _very_ small number of workers
            # will be enough to destroy a SAS cluster if the requests do not wait 
            # briefly

            # It is a suspicion that this may have caused a full blown SAS outage in hou :(
            t1 = time()
            classify_req, cid = classify(term)
            classify_time = (time() - t1) * 1000
            manage_backoff(classify_req, classify_time)

            t1 = time()
            search_req, titles = search(cid, term)
            search_time = (time() - t1) * 1000
            manage_backoff(search_req, search_time)

            for write_queue in write_queues:
                write_queue.put(((cid, titles, term),))
        except Exception as e:
            traceback.print_exc(e)
            print 'Fetch error for term ' + term
            reject_queue.put(term, 100)

def write(write_queue, reject_queue, file_name, num_titles):

    with open(file_name, 'w+') as dataset:
        while True:
            cid, titles, term = write_queue.get(300)[0]
            if len(titles) >= num_titles:
                try:
                    uri = construct_rel_search_url(titles, cid, num_titles)
                    dataset.write(uri)
                    print 'Writer [%s] - wrote out uri for - %s' %(file_name, term)
                except Exception as e:
                    traceback.print_exc(e)
                    reject_queue.put(term, 100)
            else:
                print 'Writer [%s] - WARNING not enougth results found for test case num results %s required results %s' %(file_name, len(titles), num_titles)

def start_processes(processes):
    for process in processes:
        process.start()

def join_processes(processes):
    for process in processes:
        process.join()

def get_output_filename(num):
    return './test-data-%s-titles' % str(num)

def create_writer(reject_queue, num):
    queue = JoinableQueue()
    writer = Process(target=write, 
            args=(queue, reject_queue, get_output_filename(num), num), 
            name='related-search-test-writer-%s' % str(num))
    return queue, writer

def create_fetcher(fetch_queue, write_queue, reject_queue, num):
    return Process(target=fetch, 
            args=(fetch_queue, write_queue, reject_queue, num), 
            name='related-search-test-fetcher-%s' %str(num))

def job_creator(fetch_queue, file):
    for term in search_terms(file):
        fetch_queue.put((term, ))

def main():

    fetch_queue = JoinableQueue()
    reject_queue = JoinableQueue(maxsize = 1000)

    log_processor = Process(target=job_creator, args=(fetch_queue, './search_log_valid_2010_06_17'), name='log-processor')
    
    writers = [ ]
    write_queues = []

    for num in DATA_SETS:
        queue, writer = create_writer(reject_queue, num) 
        writers.append(writer)
        write_queues.append(queue)

    fetchers = [ create_fetcher(fetch_queue, write_queues, reject_queue, num) for num in xrange(NUM_FETCHERS) ]
    reject_writer = Process(target=reject, args=(reject_queue, './rejected-lines'), name='related-search-reject-writer')

    log_processor.start()
    reject_writer.start()
    start_processes(writers)
    start_processes(fetchers)

    log_processor.join()
    print 'DONE? '
    fetch_queue.join()
    write_queue.join()
    reject_writer.join()

if __name__ == '__main__':
    main()
