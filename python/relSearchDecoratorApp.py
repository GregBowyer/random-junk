#!/usr/bin/env python2.6
from urlparse import urlparse
from httplib2 import Http
from urllib import urlencode, quote_plus

import unicodedata

import lxml.html
import lxml.etree

import web
web.config.debug = True

RS_HOST = 'http://127.0.0.1:8080'
RS_RELATED_URL = RS_HOST + '/solr/v2/related'

rel_search_path = lxml.etree.XPath(
    '//n:relatedSearch[@id = $id]//n:searchTerm/@phrase',
    namespaces = {
        'n' : 'http://www.shopzilla.com/search/related/v2'
    }
)

urls = (
    '/(.*)', 'ProxyBizrate',
)
app = web.application(urls, globals(), autoreload=True)

def fetch_bizrate_page(url_part, data=None):
    h = Http()
    req_url = 'http://www.bizrate.co.uk/' + url_part
    if data:
        return h.request(req_url, 'POST', data)
    else:
        return h.request(req_url, 'GET')

def extract_catID(html):
    url = html.xpath('//a[contains(@href, "catId")]/@href')
    if url:
        rd2_url = urlparse(url[0])
        tokens = dict((tuple(t.split('=')) for t in rd2_url.query.split('&')))
        return int(tokens['catId'])

def extract_titles(html):
    return html.xpath('//div[@class = "product_title"]//a/@title')
    #return html.xpath('//div[@class = "description"]//a[@class = "reviews_description"]/text()')

def perform_rel_search(catID, titles):
    h = Http()

    unicode_handled_titles = (unicodedata.normalize('NFKD', unicode(title)).encode('ascii', 'ignore') for title in titles)

    params = {
        'phrase' : ';'.join(unicode_handled_titles),
        'category' : catID,
        'grp' : '6',
        'num' : '5',
        'timeAllowed' : '6000',
        'q.alt' : 'phrase_scrubbed:(shoes)',
    }

    rs_url = '?'.join((RS_RELATED_URL, urlencode(params)))
    resp, content = h.request(rs_url)
    return lxml.etree.fromstring(content)

def adapt_content(content, server_name):
    decoded = unicode(content, 'UTF-8')
    html = lxml.html.fromstring(decoded)

    del content
    del decoded

    catID = extract_catID(html)
    titles = extract_titles(html)
    if catID and titles:
        rel_searches = perform_rel_search(catID, titles)
        
        product_details = html.xpath('//li[@class = "rev"]/div[@class = "product_details_content"]/..')

        for pos, element in enumerate(product_details):
            rel_search_phrases = rel_search_path(rel_searches, id=pos)
            if rel_search_phrases:
                rel_search_div = lxml.html.Element('div')
                rel_search_div.attrib['style'] = 'margin-right: 50px; background-color: rgb(100, 230, 50); font-size: 16px; z-index: 100'
                for phrase in rel_search_phrases:
                    search_link = lxml.html.Element('a')
                    href = '/classify?search_box=1&cat_id=%s&sfsk=0&keyword=%s' %(catID, quote_plus(phrase))
                    search_link.attrib['href'] = href
                    search_link.attrib['style'] = 'z-index: 100'
                    search_link.text = phrase
                    rel_search_div.append(search_link)
                    spacer = lxml.html.Element('span')
                    spacer.text = ' '
                    rel_search_div.append(spacer)

                # We could find the element properly, but I know its at 5 and this is a hack :S
                element.insert(5, rel_search_div)

    def rewrite_link(link):
        if link.startswith('http://www.bizrate.co.uk'):
            return link[len('http://www.bizrate.co.uk'):]
        else:
            return link

    html.rewrite_links(rewrite_link)
    return lxml.html.tostring(html, encoding="UTF-8")

class ProxyBizrate(object):

    def copy_headers(self, headers):
        web.header('Content-Type', headers['content-type'])
        web.header('content-type', headers['content-type'])

    def GET(self, name):
        res, content = fetch_bizrate_page('?'.join((name, web.ctx.environ['QUERY_STRING'])))
        self.copy_headers(res)
        return adapt_content(content, web.ctx.environ['SERVER_NAME'])

    def POST(self, name):
        res, content = fetch_bizrate_page(name, data=web.data())
        self.copy_headers(res)
        return adapt_content(content, web.ctw.environ['SERVER_NAME'])

if __name__ == '__main__':
    app.run()
