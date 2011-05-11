from httplib2 import Http

SCANNER_DEF = '''<Scanner batch="%(batchSize)i">
<filter>{
    "latestVersion":  true,
    "qualifier":      "%(columnName)s",
    "family":         "%(columnFamily)s",
    "op":             "GREATER_OR_EQUAL",
    "type":           "SingleColumnValueFilter",
    "comparator":     {
        "value": "%(value)s",
        "type":  "BinaryComparator"
    }
}</filter>
</Scanner>'''

HEADERS = { 'Content-Type': 'text/xml' }

SCANNER_URL_BASE = 'http://hadstg023.shopzilla.lonstg:8080/%s/scanner'

h = Http()

def createScanner(columnName, columnFamily, value, batchSize=10):
    return SCANNER_DEF %({
        'columnName': columnName.encode('base64').strip(),
        'columnFamily': columnFamily.encode('base64').strip(),
        'value': str(value).encode('base64').strip(),
        'batchSize': batchSize})

def openScanner(table, scannerDef):
    url = SCANNER_URL_BASE %(table)
    print scannerDef
    resp, content = h.request(url, method='POST', headers=HEADERS, body=scannerDef)
    assert 200 <= int(resp['status']) < 400
    return resp['location']

def runScanner(scannerHandle):
    resp, content = h.request(scannerHandle, headers=HEADERS)
    return content

if __name__ == '__main__':
    scannerDef = createScanner('revenue_usd', 'revenue', 1)
    scannerHandle = openScanner('orion_keyword_metric_us', scannerDef)
    print runScanner(scannerHandle)
