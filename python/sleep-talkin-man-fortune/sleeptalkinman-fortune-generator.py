#!/usr/bin/env python
""" Random python program that is designed to produce the string file used for 
    generating sleep talking man as a fortune file """
import feedparser
from BeautifulSoup import BeautifulSoup

base_url = 'http://sleeptalkinman.blogspot.com/feeds/posts/default'

def strip_html(text):
    """ Strips out all HTML elements from a given text"""
    return ''.join(BeautifulSoup(text).findAll(text=True))

def flatten(x):
    """ Flattens down the atom tree to just have the contents we are interested in """
    for el in x:
        for child in el:
            quips = strip_html(child['value']).split('""')
            for quip in quips:
                if quip:
                    yield quip.strip('"')


def parse_feed(url=base_url):
    """ Given the sleep talkin man feed, produce a generator that can be used to extract fortunes """
    data = feedparser.parse(url)
    return flatten((entry.content for entry in data.entries))

def generate_fortune_lines(quips):
    """ Given a list of quips, produce a fortune file """
    for quip in quips:
        yield quip
        yield ''
        yield '\t -- Sleep Talking Man (http://sleeptalkingman.blogspot.com)'
        yield '%'

def main():
    print('\n'.join(generate_fortune_lines(parse_feed())))

if __name__ == '__main__':
    main()

# Do something clever ...
