# -*- coding: utf-8 -*-
import sys
import lucene

from itertools import groupby
from collections import Counter, defaultdict
from lucene import MMapDirectory, File, IndexReader, NumericUtils, Term

INDEX_DIR = "/home/greg/solr-index/data/index/index/"

# Ok so as I wrote this code I got a little λ heavy, prehaps I *should*
# have persevered with clojure and just wrote it in lisp

# Its going to look like soup to most people, python ideas you need to know would be
# 1) Higher order, functional programming
# 2) Generators + iterators
# 3) Generator and List Comprehensions
# 4) some lucene
# 5) Pythons bizarre but closable lambda

try:
    if 'vm' not in locals() or 'vm' not in globals():
        print lucene.CLASSPATH
        vm = lucene.initVM(classpath=lucene.CLASSPATH, vmargs='-XX:+TieredCompilation,-XX:+DoEscapeAnalysis,-XX:+UseCompressedOops', initialheap='4G', maxheap='6G')
except ValueError:
    print 'VM already initialised for this process'

index_directory = MMapDirectory.open(File(INDEX_DIR))
reader = IndexReader.open(index_directory, True)

def frequency(termDocs):
    ''' Dumb count of the frequency for the given termDocEnum '''
    count = 0
    while termDocs.next():
        count += 1
    return count

def filtered_term_enum(reader, filter, decoder):
    ''' Given a filter (which will be passed Term as its only argument and is expected to
        return True/False) this will return a tuple of form (field, term_decoded, freq) '''
    original_term_enum = reader.terms()
    while original_term_enum.next():
        t = original_term_enum.term()
        if filter(t):
            termDocs = reader.termDocs(t)
            yield t.field(), decoder(t), frequency(termDocs)

field_names = [f for f in reader.getFieldNames(IndexReader.FieldOption.INDEXED) if f.startswith('att')]
term_enum = filtered_term_enum(reader, \
        lambda t: t.field().startswith('att'), \
        lambda t: NumericUtils.prefixCodedToInt(t.text()))

field_term_dict = dict([(k, [t[1:] for t in list(g)]) for k, g in groupby(term_enum, lambda x: x[0])])
unused_fields = set(field_names).difference(field_term_dict.keys())
doc_counts = map(lambda x: (x[0], sum((term[1] for term in x[1]))), field_term_dict.iteritems())
doc_counts = sorted(doc_counts, key=lambda x: x[1], reverse=True)

term_counts = sorted(((x[0], len(x[1])) for x in field_term_dict.iteritems()), \
        key=lambda x: x[1], \
        reverse=True)

field_multiterm_count = defaultdict(Counter)

for feild_name, terms in field_term_dict.iteritems():
    for term in terms:
        term_docs = reader.termDocs(Term(feild_name, NumericUtils.intToPrefixCoded(term[0])))

        while term_docs.next():
            doc_id = term_docs.doc()
            field_multiterm_count[feild_name][doc_id] += 1

# Everything from this point here is scopied out of my ipython history, so its going to look icky
def munge():
    to_delete = []
    to_delete = [field for field, count in field_multiterm_count.iteritems() \
            if sum(count.values()) == len(count.values())]
    for i in to_delete:
        del field_multiterm_count[i]
    to_delete = []
    for field, count in field_multiterm_count.iteritems():
        for key in count.keys():
            if count[key] == 1:
                to_delete.append((field, key))
    for field, counter_name in to_delete:
        del field_multiterm_count[field][counter_name]

    doc_cache = {}
    with open('/tmp/attribute-counts', 'w') as output:
        for field, counts in field_multiterm_count.iteritems():
            output.write('%s ->\n' %(attr_tree[field[3:]]))
            for docid, count in counts.iteritems():
                if docid in doc_cache:
                    doc = doc_cache[docid]
                else:
                    lucene_doc = reader.document(docid)
                    doc = lucene_doc.getFieldable('docid').stringValue()
                    doc_cache[docid] = doc
                output.write('\tLucene_Doc [%s], SZ_DOC [%s], Field [%s], Term_Count[%d]\n' \
                        %(docid, doc, field, count))

    def decode(f):
        if f:
            if attr_tree[f[3:]] and attr_tree[f[3:]].name:
                return attr_tree[f[3:]].name.decode('utf8', 'replace')

    def total_doc_count(f):
        return sum(x[1] for x in field_term_dict[f])

    with uopen('/tmp/sorted-multivalue-attributes-by-num-docs', 'w', encoding='UTF8') as output:
        output.write('attribute\tFriendly Name\tNumber of documents with multiple values\tTotal Num Documents with attribute\tNumber of attribute terms\n')
        values = (u'%s\t%s\t%d\t%d\t%d\n' %(f, decode(f), sum(c.values()), total_doc_count(f), len(field_term_dict[f])) for f, c in sorted(field_multiterm_count.iteritems(), key=lambda x: x[1], reverse=True))
        output.writelines(values)

# vim: set et fenc=utf-8 ff=unix sts=4 sw=4 ts=4 :
