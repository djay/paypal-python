
import urllib
import cgi


def flatten(r, name=None):
    r2 = {}
    for n,v in r.items():
        if name:
            n = name + "." + n
        if type(v) == type({}):
            r2.update(flatten(v,n))
        elif type(v) == type([]):
            for i,item in zip(range(len(v)),v):
                lname = "%(n)s(%(i)i)" % locals()                    
                r2[lname] = item
        else:
            r2[n] = v 
    return r2

def unflatten(r):
    r2 = {}
    for n,v in r.items():
        if '.' in n:
            n,n2 = n.split('.',1)
            r2.setdefault(n,{})[n2] = v
        else:
            r2[n] = v
    return r2


class NVPEncoder(object):
    def encode(self, request):
        return urllib.urlencode(flatten(request))
    FORMAT = 'NV'
    def decode(self,response):
        response = dict(cgi.parse_qs(response))
        return unflatten(response)
        
try:
    from ZSI.writer import SoapWriter
except:
    SoapWriter = None

if SoapWriter:
    class SoapEncoder(object):

        def encode(self, request):
            # TODO: implement this
            return SoapWriter().serialize(request)
        FORMAT = 'SOAP'


import simplejson as json

class JSONEncoder(object):
    def encode(self, request):
        return json.dumps(request)
    def decode(self, response):
        return json.loads(str(response))
        
    FORMAT = 'JSON'



class RequestFactory(object):

    # TODO: implement some way of generating requests

    def __init__(self):
        self.map = {
            'PayRequest': {},
        }
        

class ResponseFactory(object):

    # TODO: implement some way of turning SOAP responses into objects

    def __init__(self):
        self.map = {
            'PayResponse': {},
        }
