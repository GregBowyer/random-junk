import sqlite3
from httplib2 import Http

from lxml import etree

# This is a prebuikld sqllite database from ISS_FINAL.txt 
# Used to make such anlysis as below easier
with sqlite3.connect('./ISS_FINAL2.sqlite') as database:
    atoms = [str(tuple[0]) for tuple in database.cursor() \
        .execute('SELECT DISTINCT atomid FROM temp') \
        .fetchall()]

BUCKET_SIZE=100
TAXII_URL = 'http://taxiistage001.shopzilla.laxhq/2006/10/1/TaxonomyService/current/us/graph/12/atoms/attrs?visit_parents=1&id='

with open('./mappings', 'w') as mappings:

    mappings.write('atomID, cid\n')

    for i in xrange(len(atoms) / BUCKET_SIZE):
        bucket = i * 100
        atom_bucket = atoms[bucket : bucket + BUCKET_SIZE]

        taxii = Http()
        resp, content = taxii.request(TAXII_URL + '&id='.join(atom_bucket))

        doc = etree.fromstring(content)
        finder = etree.XPath(
            "//n:atom[@id=$atomID]/n:parents/n:nodeRef/@rid", 
            namespaces = {
                'n':'http://shopzilla.com/2006/10/1/TaxonomyService'
            }
        )

        for atom in atom_bucket:
            cids = finder(doc, atomID=atom)

            for cid in cids:
                mappings.write('%s,%s\n' % (str(atom), str(cid)))

        mappings.flush()
