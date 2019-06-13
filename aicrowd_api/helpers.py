import requests
def make_api_call(auth_token, request_type, url, payload={}, debug=False):
    if debug:
        import logging
        try:
            import http.client as http_client
        except ImportError:
            # Python 2
            import httplib as http_client
        http_client.HTTPConnection.debuglevel = 1

        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    assert request_type in ['get', 'post', 'patch']
    headers = {
        'Authorization': 'Token token='+auth_token,
        "Content-Type": "application/vnd.api+json"
        }
    function = {}
    function["get"] = requests.get
    function["post"] = requests.post
    function["patch"] = requests.patch

    r = function[request_type](
                              url,
                              params=payload,
                              headers=headers,
                              verify=True
                              )
    return r
