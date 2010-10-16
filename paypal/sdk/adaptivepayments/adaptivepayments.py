
import socket
import urllib
import urllib2
from . import BaseConstants
from . import BaseAPIProfile
from . import PaymentException
#from .encoder import SoapEncoder
from ..response import Response
import sys
from urllib import urlencode


class AdapativePayments(object):

    def __init__(self, profile=None, encoder=None):
        """ @param API Profile
            @param encode (e.g. SOAP Encoder)
        """
        self.profile = profile
        self.payload = ""
        self.request_method = BaseConstants.REQUESTMETHOD
        self.encoder = encoder

        self.ap_endpoint = "" #??? TODO: figure out what this is

    #
    # API Actions
    #

    def pay(self, request):
        """ @param PayRequest
            @return PayResponse
        """
        return self._process_request(request, "Pay")

    def preapproval_details(self, request):
        """ @param PreapprovalDetailsRequest
            @return PreapprovalDetailsResponse
        """
        return self._process_request(request, "PreapprovalDetails")

    def refund(self, request):
        """ @param RefundRequest
            @param RefundResponse
        """
        return self._process_request(request, "Refund")

    def payment_details(self, request):
        """ @param PaymentDetailsRequest
            @param PaymentDetailsResponse
        """
        return self._process_request(request, "PaymentDetails")

    def preapproval(self, request):
        """ @param PreapprovalRequest
            @param PreapprovalResponse
        """
        return self._process_request(request, "Preapproval")

    def cancel_preapproval(self, request):
        """ @param CancelPreapprovalRequest
            @param CancelPreapprovalResponse
        """
        return self._process_request(request, "CancelPreapproval")

    def convert_currency(self, request):
        """ @param ConvertCurrencyRequest
            @param ConvertCurrencyResponse
        """
        return self._process_request(request, "ConvertCurrency")

    #
    # Shared Private Methods
    #

    def _process_request(self, request, endpoint):
        self.profile.EndPointAppend = self.ap_endpoint + endpoint
        self.payload = self.encoder.encode(request)
        response = self._call_api()

        if "Failure" in response['responseEnvelope']['ack']:
            raise PaymentException(response)
        return response

    def _call_api(self):
        assert self.payload, "Payload is required"
        assert self.profile, "API Profile is required"
        
        if self.profile.environment == 'sandbox':
            sandbox = 'sandbox.'
        else:
            sandbox = ""

        url = 'https://svcs.%spaypal.com/AdaptivePayments/%s' % (sandbox,
                                                               self.profile.EndPointAppend)
        headers = self._headers()

        # TODO: Add the certificate to HttpWebRequest obejct if Profile is certificate enabled
        #if self.profile.APIProfileType == ProfileType.Certificate:
        #    raise NotImplementedError("Does not yet support certificate authentication")
        #else:
        #    headers[BaseConstants.XPAYPALSECURITYSIGNATURE] = self.profile.APISignature
        headers[BaseConstants.XPAYPALSECURITYSIGNATURE] = self.profile.APISignature
        
        headers[BaseConstants.XPAYPALREQUESTDATAFORMAT] = self.encoder.FORMAT
        headers[BaseConstants.XPAYPALRESPONSEDATAFORMAT] = self.encoder.FORMAT
        
        self.payload = self.payload

        print >> sys.stderr, url
        print >> sys.stderr, headers
        print >> sys.stderr, self.payload
        request = urllib2.Request(url, self.payload, headers)

        timeout = self.profile.timeout
        if timeout < 1:
            timeout = BaseConstants.DEFAULT_TIMEOUT;
        #socket.setdefaulttimeout(timeout)

        response = urllib2.urlopen(request).read()
        #print >> sys.stderr, response
        response = self.encoder.decode(str(response))
        #print >> sys.stderr, response
        return response

    def _headers(self):
        # Adding Credential and payload request/resposne information
        headers = {}
        headers[BaseConstants.XPAYPALSECURITYUSERID] = self.profile.apiUsername
        headers[BaseConstants.XPAYPALSECURITYPASSWORD] = self.profile.apiPassword
        headers[BaseConstants.XPAYPALAPPLICATIONID] = self.profile.applicationID
        #headers[BaseConstants.XPAYPALDEVICEIPADDRESS] = self.profile.deviceIpAddress
        headers[BaseConstants.XPAYPALREQUESTDATAFORMAT] = BaseConstants.RequestDataformat
        headers[BaseConstants.XPAYPALRESPONSEDATAFORMAT] = BaseConstants.ResponseDataformat
        #headers[BaseConstants.XPAYPALMESSAGEPROTOCOL] = BaseConstants.RequestDataformat
        return headers
    
    def verify_ipn(self, data):
            # prepares provided data set to inform PayPal we wish to validate the response
            data = dict(data)
            data["cmd"] = "_notify-validate"
            params = urlencode(data)
    
            # sends the data and request to the PayPal Sandbox
           
            if self.profile.environment == 'sandbox':
                sandbox = 'sandbox.'
            else:
                sandbox = ""
    
            url = 'https://www.%spaypal.com/cgi-bin/webscr' % (sandbox)
    
            req = urllib2.Request(url, params)
            req.add_header("Content-type", "application/x-www-form-urlencoded")
            # reads the response back from PayPal
            response = urllib2.urlopen(req)
            status = response.read()
    
            # If not verified
            if not status == "VERIFIED":
                    return False
    
            # otherwise...
            return True
        
    def preapproval_url(self, preapprovalKey):
        if self.profile.environment == 'sandbox':
            sandbox = 'sandbox.'
        else:
            sandbox = ""
        url = "https://www.%spaypal.com/webscr?cmd=_ap-preapproval&preapprovalkey=%s"% (sandbox,preapprovalKey)
        return url

