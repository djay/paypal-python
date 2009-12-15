"""
This is my first pass at attempting at implementing a client
in python for the PayPal adaptive payments API.
"""

__id__ = "$Id: $"


from ..exceptions import ApiError as PaymentException


class BaseConstants(object):

        #
        # WARNING: Do not embed plaintext credentials in your application code.
        # Doing so is insecure and against best practices.
        #
        # Your API credentials must be handled securely. Please consider
        # encrypting them for use in any production environment, and ensure
        # that only authorized individuals may view or modify them.
        #

        XPAYPALREQUESTDATAFORMAT = "X-PAYPAL-REQUEST-DATA-FORMAT"
        XPAYPALRESPONSEDATAFORMAT = "X-PAYPAL-RESPONSE-DATA-FORMAT"
        XPAYPALSERVICEVERSION = "X-PAYPAL-SERVICE-VERSION"
        XPAYPALREQUESTSOURCE = "X-PAYPAL-REQUEST-SOURCE"
        XPAYPALSECURITYUSERID = "X-PAYPAL-SECURITY-USERID"
        XPAYPALSECURITYPASSWORD = "X-PAYPAL-SECURITY-PASSWORD"
        XPAYPALSECURITYSIGNATURE = "X-PAYPAL-SECURITY-SIGNATURE"
        XPAYPALMESSAGEPROTOCOL = "X-PAYPAL-MESSAGE-PROTOCOL"
        XPAYPALAPPLICATIONID = "X-PAYPAL-APPLICATION-ID"
        XPAYPALDEVICEIPADDRESS = "X-PAYPAL-DEVICE-IPADDRESS"
        XPAYPALSANDBOXEMAILADDRESS = "X-PAYPAL-SANDBOX-EMAIL-ADDRESS"

        # Data Request format specified here
        RequestDataformat="SOAP11"
        ResponseDataformat="SOAP11"

        REQUESTMETHOD = "POST"
        PAYPALLOGFILE = "PAYPALLOGFILE"

        DEFAULT_TIMEOUT = 3600000


class BaseAPIProfile(object):

        # The username used to access the PayPal API
        apiUsername = ""

        # The password used to access the PayPal API
        apiPassword = ""

        # The name of the entity on behalf of which this profile is issuing calls
        subject = ""

        #  The PayPal environment (Live, Sadnbox)
        environment = "sandbox"

        #  The connection timeout in milliseconds
        timeout = 30000

        #  The maximum number of retries
        maximumRetries = 3

        #  The delay time bewteen each retry call in milliseconds
        delayTime = 1000

        # The API signature used in three-token authentication
        apiSignature = ""

        # The username used to access the PayPal API

        # The certificate used to access the PayPal API
        certificateFile = ""

        # The certificate used to access the PayPal API
        certificate = None # ??? byte[] in .net client

        # The privateKeyPassword used
        privateKeyPassword = ""

        # Type of profile used to authenticate
        apiProfileType = None # ??? ProfileType in .net client, either ThreeToken or Certificate

        # To specify trust all certificate
        isTrustallCertificate = True
        deviceIpaddress = ""
        sandboxMailAddress = ""

        # Paypal request and response Data format.
        XPAYPALREQUESTDATAFORMAT = BaseConstants.XPAYPALREQUESTDATAFORMAT
        XPAYPALRESPONSEDATAFORMAT = BaseConstants.XPAYPALRESPONSEDATAFORMAT
        XPAYPALSERVICEVERSION = BaseConstants.XPAYPALSERVICEVERSION
        XPAYPALREQUESTSOURCE = BaseConstants.XPAYPALREQUESTSOURCE
        XPAYPALAPPLICATIONID = BaseConstants.XPAYPALAPPLICATIONID

        # Endpoint to Append to URL
        EndPointAppend = ""