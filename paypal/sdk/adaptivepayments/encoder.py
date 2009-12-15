
class SoapEncoder(object):

    def encode(self, request):
        # TODO: implement this
        raise NotImplementedError
        
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
