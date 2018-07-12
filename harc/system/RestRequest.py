from requests import post
from requests import get
import json


class RestRequest:
    def __init__(self):
        pass

    @staticmethod
    def get(headers, url, message, certificate, proxies):
        # retrieve the file locations of the crt and key.
        cert = None
        if certificate:
            cert = (certificate['crt'], certificate['key'])

        response = get(url, json.dumps(message), headers=headers, cert=cert, proxies=proxies)
        return response

    @staticmethod
    def post(headers, url, message, certificate, proxies):

        # retrieve the file locations of the crt and key.
        cert = None
        if certificate:
            cert = (certificate['crt'], certificate['key'])

        response = post(url, json.dumps(message), headers=headers, cert=cert, proxies=proxies)
        return response
