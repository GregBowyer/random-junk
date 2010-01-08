from urllib2 import urlopen
from lxml import etree

terms = (('perfume.jpg','Perfume & Cologne','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13282'),
('laptop.jpg','Notebooks','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13969'),
('shoes.jpg','Women's Shoes','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13130'),
('tv.jpg','TVs','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=12948'),
('fridge.jpg','Fridges','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13027'),
('bedding.jpg','Bedding','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13167'),
('camera.jpg','Digital Cameras','http://astrosashoupr001.sl2.shopzilla.hou:7033/services/aggregator/v5/GB/10/category_search?cid=13635'))

for term in terms:
    et = etree.parse(urlopen(term[2]))
    print et.xpath('//categories/category/@alias')

