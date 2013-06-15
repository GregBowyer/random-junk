

def process_solr_log(solr_log):
    with open(solr_log, 'r') as log:
        query_lines = (line for line in log if 'QTime' in line)
        
        for line in query_lines:
            yield dict((token.split('=', 1) for token in line.split(' ') if '=' in token))
