import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

from gensim import corpora, models

def prepare_dict(documents, cid, stopwords, output='/datasets/gensim-dict-%(cid)s'):
    """ Prepares the dict for gensim, presently this does stupid simple scrubbing of the following
        rules:

            tokenise on whitespace
            stopword removal
            lowercase
            abandon unique grams
            abandon anything none A-Z
    """

    # remove common words and tokenize
    def normalise(t):
        toreturn = []
        for c in t:
            if c.isalpha():
                toreturn.append(c)

        return ''.join(toreturn)

    texts = [[normalise(t) for t in d.split() \
            if t not in stopwords] for d in documents]
    print 'found tokens: ', len(texts)
    print 'getting terms'

    # remove words that appear only once
    all_tokens = sum(texts, [])
    print 'unique tokens: ', len(all_tokens)
    print 'determing tokens'
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

    def isgood(word):
        if not word:
            return False

        if len(word) <= 3:
            return False

        if word in tokens_once:
            return False

        return word.isalpha()

    texts = [[word for word in text if isgood(word)] for text in texts]
    print 'found tokens: ', len(texts)

    print 'preparing dictionary'

    dictionary = corpora.Dictionary(texts)

    print 'saving dictionary'

    # store the dictionary, for future reference
    dictionary.save(output %{'cid' : cid})
    return dictionary

def load_stopwords(input):
    with open(input, 'r') as stopwords:
        return set((t for t in stopwords))

def load_raw_data(data, cid):
    with open(data, 'r') as lines:
        docid = -1
        atom = -1
        title = None

        for line in (l.strip() for l in lines):
            oid, key, value = line.split('\t', 3)

            if docid != oid:
                docid = oid
                if title and atom == cid:
                    yield title.lower()
                    atom = -1
                    title = None

            if key == 'title':
                title = value

            if key == 'atom':
                atom = int(value)


if __name__ == '__main__':
    atom = int(sys.argv[1])
    stopwords = load_stopwords('/home/greg/work/solr-prototype/conf/en_US/stopwords.txt')
    to_index = load_raw_data('/datasets/out4', atom)
    corpus = prepare_dict(to_index, atom, stopwords)
    raise 'e'

    tf_idf = models.TfidfModel(corpus)
    lsi = models.LsiModel(tf_idf[corpus], id2word=corpus, num_topics=500)
