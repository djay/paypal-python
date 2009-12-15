
import socket
import urllib
import urllib2
from . import BaseConstants
from . import BaseAPIProfile
from . import PaymentException
#from .encoder import SoapEncoder

class AdapativePayments(object):

    def __init__(self, profile=None, encoder=None):
        """ @param API Profile
            @param encode (e.g. SOAP Encoder)
        """
        self.profile = profile
        self.payload = ""
        self.request_method = BaseConstants.REQUESTMETHOD
        self.encoder = encoder

    #
    # API Actions
    #

    def pay(self, request):
        """ @param PayRequest
            @return PayResponse
        """
        return self.process_request(request, "Pay")

    def preapproval_details(request):
        """ @param PreapprovalDetailsRequest
            @return PreapprovalDetailsResponse
        """
        return self.process_request(request, "PreapprovalDetails")

    def refund(request):
        """ @param RefundRequest
            @param RefundResponse
        """
        return self.process_request(request, "Refund")

    def payment_details(request):
        """ @param PaymentDetailsRequest
            @param PaymentDetailsResponse
        """
        return self.process_request(request, "PaymentDetails")

    def preapproval(request):
        """ @param PreapprovalRequest
            @param PreapprovalResponse
        """
        return self.process_request(request, "Preapproval")

    def cancel_preapproval(request):
        """ @param CancelPreapprovalRequest
            @param CancelPreapprovalResponse
        """
        return self.process_request(request, "CancelPreapproval")

    def convert_currency(request):
        """ @param ConvertCurrencyRequest
            @param ConvertCurrencyResponse
        """
        return self.process_request(request, "ConvertCurrency")

    #
    # Shared Private Methods
    #

    def _process_request(self, request, endpoint):
        self.profile.EndPointAppend = self.apEndpoint + endpoint
        self.payload = self.encoder.encode(request)
        response = self._call_api()

        if "<ACK>FAILURE</ACK>" in response.upper():
            raise PaymentException(response)
        return True

    def _call_api(self):
        assert self.payload, "Payload is required"
        assert self.profile, "API Profile is required"

        url = self.profile.Environment + self.profile.EndPointAppend
        headers = self._headers()

        # TODO: Add the certificate to HttpWebRequest obejct if Profile is certificate enabled
        if self.profile.APIProfileType == ProfileType.Certificate:
            raise NotImplementedError("Does not yet support certificate authentication")
        else:
            headers[BaseConstants.XPAYPALSECURITYSIGNATURE] = self.profile.APISignature

        request = urllib2.Request(url, self.payload, headers)

        timeout = self.profile.Timeout
        if timeout < 1:
            timeout = BaseConstants.DEFAULT_TIMEOUT;
        socket.setdefaulttimeout(timeout)

        response = Response(urllib2.urlopen(request).read())
        return response

    def _headers(self):
        # Adding Credential and payload request/resposne information
        headers = {}
        headers[BaseConstants.XPAYPALSECURITYUSERID] = self.profile.APIUsername
        headers[BaseConstants.XPAYPALSECURITYPASSWORD] = self.profile.APIPassword
        headers[BaseConstants.XPAYPALAPPLICATIONID] = self.profile.ApplicationID
        headers[BaseConstants.XPAYPALDEVICEIPADDRESS] = self.profile.DeviceIpAddress
        headers[BaseConstants.XPAYPALREQUESTDATAFORMAT] = BaseConstants.RequestDataformat
        headers[BaseConstants.XPAYPALRESPONSEDATAFORMAT] = BaseConstants.ResponseDataformat
        headers[BaseConstants.XPAYPALMESSAGEPROTOCOL] = BaseConstants.RequestDataformat
        return headers

