"""
Minimal Fedora REST-API client.  
Gets pids.
Ingests foxml.
"""

#For pid getting and ingestion.
import requests

#Set this after import like:
#repo.USER = 'real'
#repo.PASSORD='pass
URL = 'http://localhost:8080/fedora'
USER = 'demo'
PASSWORD = 'pass'

fedora_url = URL
auth = (USER,
        PASSWORD)
headers = {'content-type': 'text/xml'}
conn = requests.session(auth=auth,
                     headers=headers,
                     verify=False)

def get_pid(*args, **kwargs):
    import urllib
    from lxml import etree
    from StringIO import StringIO
    #We're going to force XML as the response
    kwargs['format'] = 'XML'
    params = urllib.urlencode(kwargs)
    if not params:
        params = ''
    pidxml = conn.post(fedora_url +'/objects/nextPID?%s' % params)
    tree = etree.parse(StringIO(pidxml.content))
    return tree.xpath('/pidList/pid/text()')[0]

def ingest_foxml(foxml):
    r = conn.post(fedora_url + '/objects/new', data=foxml)
    if r.status_code != 201:
        raise IngestionError("""Fedora ingestion failed with status code %s.
                              API traceback -- %s""" % (r.status_code, r.text))
    else:
        return True
    
class IngestionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
