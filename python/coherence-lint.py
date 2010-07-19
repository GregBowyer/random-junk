import sys
import os

from lxml import etree

from ipaddr import IPAddress, IPNetwork

def lint_ipaddresses(doc, cluster_network = IPNetwork('10.61.34.0/24')):
    if doc.xpath('/coherence'):
        wka_addresses = doc.xpath('/coherence/cluster-config/unicast-listener/wll-known-addresses/socket-address')

        for wka_address in wka_addresses:
            address = IPAddress(wka_address.xpath('./address/text()')[0])
            port = int(wka_address.xpath('./port/text()')[0])

            assert port in (35501, 35502, 35503)
            assert address.is_private()
            assert address in cluster_network

def lint_cachecfgexists(doc):
    if doc.xpath('/coherence'):
        cache_config = doc.xpath('.//param-value[@system-property = "tangosol.coherence.cacheconfig"]/text()')
        assert os.path.exists(cache_config[0])

def lint_springcfgexists(doc):
    if doc.xpath('/coherence'):
        cache_config = doc.xpath('.//param-value[@system-property = "tangosol.coherence.springconfig"]/text()')
        assert os.path.exists(cache_config[0])

def lint_servicenamebound(doc):
    if doc.xpath('/cache-config'):
        cache_schemes = doc.xpath('//cache-mapping')

        bound_schemes = set(doc.xpath('//cache-mapping/scheme-name/text()'))
        registered_schemes = set(doc.xpath('//caching-schemes//scheme-name/text()'))
        assert bound_schemes.issubset(registered_schemes)

        for scheme in doc.xpath('//caching-schemes'):
            assert scheme.xpath('.//service-name')

def lint_licensemode(doc):
    if doc.xpath('/coherence'):
        assert doc.xpath('/coherence/license-config/license-mode/text() = "prod"')

def lint_logging(doc):
    if doc.xpath('/coherence'):
        assert doc.xpath('/coherence/logging-config/destination/text() = "log4j"')

LINT_CHECKS = [
    lint_ipaddresses,
    lint_licensemode,
    lint_logging,
    lint_cachecfgexists,
    lint_springcfgexists,
    lint_servicenamebound,
]

def run_lint_checks(doc):
    for lint_check in LINT_CHECKS:
        result = lint_check(doc)

def run_lint(files):
    for file in files:
        doc = etree.parse(file)
        run_lint_checks(doc)

if __name__ == '__main__':
    import sys
    run_lint(sys.argv[1:])
