#!env python2.6
# coding=utf-8

# Dont ask about the above, life gets better with python3

# Gregs quick and dirty template screencopy munger, takes the templates in
# produces a properties file, and dumps the altered html to disk 
# also trys to guess what the best key might be for the given bunch 'o' copy
import path as pth
import itertools
import string

import nltk
import codecs

from lxml import html 
from lxml.html import HtmlComment

from Sets import OrderedSet

TAL_NS = 'http://xml.zope.org/namespaces/tal'

webapp_files = '/Users/750062/work/bizrate.co.uk/webapp/src/main/webapp/'
dump_dir = '/tmp/dump/'
excluded_templates = ['logging', 'debugfooter', 'debugheader', 'debugfooter', 'debugheader', 'about', 'contact_info', 'contact_us', 
    'contact_us__form-type--business', 'legal', 'press_releases', 'privacy', 'sweepstakes', 'disablecookies',
    'ratings_guide', 'serverstatus', 'interstitial-static' ]

# Functions that generate a key, based on the incoming element
# These return thier best key and a score out of 100 for 
# their subjective measure as to if the key is really good
# returning None also works as the fns approach to saying I give up

# Fill these in later, such that we can derive resonable keys for the 
# text blobs, for now they do nothing
def genkey_tag(element, text):
    if element.tag in ('title',):
        return (100, 'title', 'title')

def genkey_id(element, text):
    if element.attrib.has_key('id'):
        return (85, element.attrib['id'], 'id')

def genkey_ancestors(element, text):
    pass

stopwords = nltk.corpus.stopwords.words('english')
print 'Building Word distribution tables'
print 'Processing Brown list - 1/6'
brown = nltk.FreqDist(nltk.corpus.brown.words())
print 'Processing Gutenberg list - 2/6'
guten = nltk.FreqDist(nltk.corpus.gutenberg.words())
print 'Processing Reuters list - 3/6'
news = nltk.FreqDist(nltk.corpus.reuters.words())
print 'Processing ABC TV list - 4/6'
abc = nltk.FreqDist(nltk.corpus.abc.words())
print 'Processing movies list - 5/6'
movie = nltk.FreqDist(nltk.corpus.movie_reviews.words())
print 'BizRate corpus list - 6/6'
bz_corp = nltk.corpus.PlaintextCorpusReader('/Users/750062/work', 'bizrate-corpus')
bz = nltk.FreqDist(bz_corp.words())
print 'Done!'

# Add a bit of weight to words common to the BZ site
manual_weights = { 'search' : 200, 'compare' : 350, 'store' : 400, 'certified' : 300, 'circle' : -4000, 'winner' : 30, 'found' : -100,
        'bizrate' : -300 , 'buyers' : 20 , 'i' : -4000, 'i' : -4000, 'quality' : - 20, 'often' : -400, 'oh' : -2000,
        'searches' : 200, 'sitemap' : 100, 'ratings' : 300, 'rated' : 300, 'rerated' : 300, 'error' : 100 , 'you' : -4000,
        'uk' : -4000, 'site' : 300, 'priority' : 200, 'standard' : 200, 'if' : -400, 'about' : 300, 'smilies' : 600,
        'smiley' : 600, 'visualise' : 200, 'research' : 200, 'shoppers' : 200, 'comparison' : 150 , 'don' : -4000,
        'scale' : 400, 'uh' : -44444, 'satisfaction' : 300, 'product' : 400, 'according' : -4000, 'overall' : 500,
        're' : -100, 'feedback' : 200, 'total' : 200, 'desired' : -600, 'mean' : -200, 'not' : 400, 'announces' : - 25,
        'purchase' : 300, 'availability' : 300, 'stated' : 50, 'charges' : 200, 'before' : -4000, 'adult' : 300
}

simple_order = { 'N' : 45, 'I' : 40, 'P' : 34, 'V' : 20, 'D' : 15, 'A' : 10, 'C' : 5 , 'J' : 5, 
        'R' : 10 , 'W' : -800, 'T' : 1 , 'E' : -100 , 'M' : 1 , 'L' : -600}

def sorter(lhs, rhs):
    a = lhs[0] + simple_order[lhs[1][:1]]
    b = rhs[0] + simple_order[rhs[1][:1]]
    return a - b

def manual_weight(text):
    if len(text) < 3:
        return -40

    if text in manual_weights:
        return manual_weights[text]
    else:
        return 0

def genkey_summary(element, text):

    if text not in common_syms:
        processed = ''.join(ch for ch in text if ch not in set(string.punctuation))
        tokens = nltk.word_tokenize(processed.strip().replace('\n','').replace('\t','').replace(r'\.', '').replace("'",'').replace('-',''))
        tokens = [token for token in tokens if token not in stopwords and token.lower() is not u'uk' or token.lower() is not 'uk']
        soup = [(manual_weight(text.lower()) + bz[text] + min(30, news[text.lower()]) + min(30, guten[text.lower()])
            + brown[text.lower()]  + min(50, movie[text.lower()]) + abc[text.lower()]
            , tag, text)
                for text, tag in nltk.pos_tag(tokens) if tag.isalpha() and tag not in ('CD', 'CC') ]
        ordered = sorted(soup, sorter, reverse=True)
        candidates = [a for a in OrderedSet([w[2] for w in ordered if w[0] < 700 and w[0] > 0])]
        if len(ordered) < 4:
            candidates = [a for a in OrderedSet([w[2] for w in ordered])]
        print ordered
        print candidates
        limit = 4
        if len(candidates) <= 4:
            limit = 3
        candidate = '_'.join(candidates[0:limit]).lower()
        print candidate
        if candidate in common_syms:
            return None
        elif len(candidates) > 0:
            return (80, candidate, 'sum')
        else:
            return (25, candidate, 'sum')

def genkey_fallback(elephant, text):
    return (1, str(elephant.__hash__()), 'fallback')

common_syms = { u'...' : 'elipis', u'>' : 'gt', u'<' : 'lt', u'=' : 'equals', 
        u'.' : 'period', u'£' : 'ERROR_EMBEDDED_CURRENCY_SYM!', u'%' : 'percent' , u':' : 'colon' , u';' : 'semicolon',
        u'…' : 'elipis', u'|' : 'pipe', u'©' : 'copy' }
def genkey_syms(element, text):
    if text in common_syms:
        raise CommonSym('COMMON SYM: ' + text)

def genkey_wordbanger(element, text):
    tokens = nltk.word_tokenize(''.join(ch for ch in text if ch not in set(string.punctuation)))
    if len(tokens) <= 3:
        tokens = [token for token in tokens if token.strip().lower() is not u'uk' or token.strip().lower() is not 'uk']
        return (82, '_'.join(tokens[0:3]).lower(), 'wordbanger')
    else:
        return (30, '_'.join(tokens[0:3]).lower(), 'wordbanger')

generators = [genkey_tag, genkey_id, genkey_ancestors, genkey_fallback, genkey_summary, genkey_syms, genkey_wordbanger]

# Core program

def has_simple_children(element):

    for child in element.getchildren():
        try:
            if child.tag is not None and child.tag.lower() not in ('i', 'b', 'em', 'strong', 'cite'):
                return False
        except Exception as ex:
            print ex
            return False

        if child.getchildren():
            return False

        if child.attrib:
            return False

        return True

    return False

def htmlise_children(elements):
    for child in elements:
        htm = html.tostring(child, pretty_print=True, method='xml', encoding='utf-8').replace('\r','')
        if child.tail:
            yield htm + child.tail
        else:
            yield htm

def process_element(element, name, excluded_tags=('style', 'script')):
    ''' Walks the given element, finding text nodes, and mangling them '''

    accum = []

    simple_child_processing = has_simple_children(element)
    orig_text = None
    
    if not [at for at in element.attrib if at.startswith('tal:content') 
            or at.startswith('tal:attribute(alt') or at.startswith('metal:use-macro')
            or at.startswith('tal:replace')]:

        try:
            if simple_child_processing:
                if element.text:
                    orig_text = element.text + ''.join(htmlise_children(element.getchildren()))
                else:
                    orig_text = ''.join(htmlise_children(element.getchildren()))

            if element.text and element.text.strip() != '':
                if simple_child_processing:
                    key, key_raw = generate_key(element, element.text_content().strip().replace('UK', ''), name)
                else:
                    orig_text = element.text
                    key, key_raw = generate_key(element, element.text.strip().replace('UK', ''), name)

                if key != name + '.' and key not in (name + '.' + str(i) for i in range(0,100)):
                    accum.append((key, orig_text))

                    if not simple_child_processing:
                        if element.getchildren():
                            child = element.makeelement('span')
                            child.text = 'SC:' + element.text
                            element.text = '\n '
                            child.attrib['tal:replace'] = "structure localiser/get('{0}', '{1}')".format(name, key_raw)
                            child.tail = '\n'
                            element.insert(0, child)
                        else:
                            element.attrib['tal:content'] = "structure localiser/get('{0}', '{1}')".format(name, key_raw)
                    else:
                        element.attrib['tal:content'] = "structure localiser/get('{0}', '{1}')".format(name, key_raw)

            if element.tail and element.tail.strip() != '':
                key, key_raw = generate_key(element, element.tail.strip().replace('UK',''), name)
                if key != name + '.' and key not in (name + '.' + str(i) for i in range(0,100)):
                    accum.append((key, element.tail.strip()))

                    element.tail = None
                    child = element.makeelement('span')
                    child.attrib['tal:replace'] = "structure localiser/get('{0}', '{1}')".format(name, key_raw)
                    child.text = element.text
                    child.tail = '\n'
                    element.tail = '\n'
                    element.addnext(child)

                    #else:
                    #    # Is this likly to occur ???
                    #    element.attrib['tal:content'] = "localiser/get('{0}', '{1}')".format(name, key_raw)
                    #    element.tail = '$$SC$$' + key + '$$'

            if 'alt' in element.attrib:
                if element.attrib['alt'] != '':
                    key, key_raw = generate_key(element, element.attrib['alt'].strip(), name)
                    key = key + '.alt'
                    key_raw = key_raw + '.alt'
                    if key != name + '.' and key not in (name + '.' + str(i) for i in range(0,100)):
                        accum.append((key, element.attrib['alt']))
                        if 'tal:attributes' in element.attrib:
                            txt = element.attrib['tal:attributes']
                            if 'localiser/get' not in txt:
                                txt = txt + ";alt localiser/get('{0}','{1}')".format(name, key_raw)
                                element.attrib['alt'] = 'SC: ' + element.attrib['alt']
                                element.attrib['tal:attributes'] = txt
                        else:
                            element.attrib['tal:attributes'] = "alt localiser/get('{0}', '{1}')".format(name, key_raw)

            if 'value' in element.attrib and element.tag is 'input' and 'submit' in element.attrib:
                if element.attrib['value'] != '':
                    key, key_raw = generate_key(element, element.attrib['value'].strip(), name)
                    key = key + '.value'
                    key_raw = key_raw + '.value'
                    if key != name + '.' and key not in (name + '.' + str(i) for i in range(0,100)):
                        accum.append((key, element.attrib['value']))
                        if 'tal:attributes' in element.attrib:
                            txt = element.attrib['tal:attributes']
                            if 'localiser/get' not in txt:
                                txt = txt + ";value localiser/get('{0}','{1}')".format(name, key_raw)
                                element.attrib['value'] = 'SC: ' + element.attrib['value']
                                element.attrib['tal:attributes'] = txt
                        else:
                            element.attrib['tal:attributes'] = "value localiser/get('{0}', '{1}')".format(name, key_raw)


            if element.tag == 'img' and 'alt' not in element.attrib:
                element.attrib['alt'] = ''

        except CommonSym as ex:
            pass

    if not simple_child_processing:
        for child in element.getchildren():
            if not isinstance(child, HtmlComment) and child.tag not in excluded_tags:
                accum.extend(process_element(child, name))

    return accum

class CommonSym(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def generate_key(element, text, name, key_generators=generators):
    ''' Given a bunch of functions that are able to deduce keys, return the one that
        scores best '''
    if text not in common_syms:
        keys = (tuple for tuple in (fn(element, text) for fn in key_generators) if tuple)
        ordered = sorted(keys, lambda left, right: right[0] - left[0])
        print ordered
        best_candidate = ordered[0]
        key = best_candidate[1].lower()
        return (name + '.' + key, key)
    else:
        raise CommonSym('Common sym')

def line_splitter(line, size=60):
    cutpoints = [line.find(' ', point) for point in xrange(0, len(line), size)]
    for i in xrange(0, len(cutpoints)):
        if cutpoints[i] != -1 and len(line) > size:
            if len(cutpoints) - 1 == i:
                yield line[cutpoints[i] :].strip()
            else:
                yield line[cutpoints[i] : cutpoints[i+1]].strip()
        else:
            yield line.strip()

def main():

    prop_bundle = []
    for file in pth.path(webapp_files).walkfiles('*.html'):
        #template_name = file.namebase.lower()
        base = file.namebase.lower()
        template_name = str(file.abspath()).replace(webapp_files, '').replace('.html', '')
        print template_name 
        if base not in excluded_templates:
            with file.open() as fp:
                fp = file.open()
                template = html.parse(fp)
                root = template.getroot()

                sc_replacements = process_element(root, template_name)
                if sc_replacements:
                    prop_bundle.extend(sc_replacements)

                    with open(dump_dir + file.name, 'w') as fp:
                        fp.write(html.tostring(template, pretty_print=True, method='xml').replace('\r',''))
    
    map1 = dict(((k, v) for v, k in prop_bundle))

    print "Num gen filtered: " + str(len(map1))
    print "Num: " + str(len(prop_bundle))

    with codecs.open(dump_dir + 'sc.properties', encoding='utf-8', mode='w') as props:
        prop_lines = [unicode('{0}={1}\n').format(k, v) for k, v in prop_bundle]
        for line in prop_lines:
            props.write(line)

if __name__ == '__main__':
    main()
