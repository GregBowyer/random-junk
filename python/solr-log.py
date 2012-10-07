from urlparse import parse_qs

def process_solr_log(solr_log):
    query_lines = (line for line in solr_log if 'QTime' in line)
    for line in query_lines:
        to_yeild = dict((token.split('=', 1) for token in line.split(' ') if '=' in token))
        to_yeild['params'] = parse_qs(to_yeild['params'][1:-1])
        yield to_yeild
