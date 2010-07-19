import networkx as nx
import lxml.etree as etree
import matplotlib.pyplot as plt

#TAXII_URL = 'http://taxiivip.shopzilla.lon/2006/10/1/TaxonomyService/current/gb/graph/6/node/16695/children/dist/infinity/attrs'
TAXII_URL = '/home/greg/taxii-tree.xml'
g = nx.Graph()
taxii_tree = etree.parse(TAXII_URL)

root = taxii_tree.getroot()

def yeild_atom(element):
    id = int(element.attrib['id'])
    props = element.attrib
    return id
atoms = (yeild_atom(element) for element in root.xpath('//n:atom', namespaces = { 'n' : root.nsmap[None] }))
g.add_nodes_from(atoms)

nodes = (yeild_atom(element) for element in root.xpath('//n:node', namespaces = { 'n' : root.nsmap[None] }))
g.add_nodes_from(nodes)

def edges():
    for node in root.xpath('//n:node', namespaces = { 'n' : root.nsmap[None] }):
        node_id = int(node.attrib['id'])
        for edge in node.xpath('./n:children/n:nodeRef/@rid', namespaces = { 'n' : root.nsmap[None] }):
            yield (node_id, int(edge))
 
g.add_edges_from(edges())

def plate():
    for node in root.xpath('//n:node', namespaces = { 'n' : root.nsmap[None] }):
        node_id = int(node.attrib['id'])
        for edge in node.xpath('./n:children/n:atomRef/@rid', namespaces = { 'n' : root.nsmap[None] }):
            yield (node_id, int(edge))

g.add_edges_from(plate())

disconnected_nodes = [n for n,d in g.degree_iter() if d == 0]
print disconnected_nodes

plt.figure(figsize=(10,10))
# draw nodes, coloring by distance from root

pos = nx.graphviz_layout(g, prog='neato', root=16695)
nx.draw(g,
    pos,
    node_color=[d for d,v in g.degree_iter()],
    with_labels=False,
    alpha=0.5,
    node_size=15)

# adjust the plot limits
xmax = 1.02 * max(xx for xx, yy in pos.values())
ymax = 1.02 * max(yy for xx, yy in pos.values())
plt.xlim(0, xmax)
plt.ylim(0, ymax)
plt.draw()
