from httplib2 import Http
import lxml.etree as etree

def gen_full_url(search_results, host='http://relatedsearchesbuilderstage001.sl2.shopzilla.seastg:8983'):
    return '/'.join((host, construct_rel_search_url(search_results)))

def construct_rel_search_url(search_results, 
        url_template='solr/suggest/v2/analyzed?phrase=%s&cid=-1&grp=33&num=10&atomIDs=%s&wt=xml&indent=on&timeAllowed=20'):

    h = Http()
    res, content = h.request(search_results)
    root = etree.fromstring(content)
    titles = etree.ETXPath('//*/{http://www.shopzilla.com/services/aggregator}title')
    atoms = etree.ETXPath('//*/{http://www.shopzilla.com/services/aggregator}atom')
    query_text = ';'.join( set(('"%s"' %(title.text) for title in titles(root))) )
    atom_filter = ';'.join( set((atom.text for atom in atoms(root))) )
    return url_template %(query_text, atom_filter)
