import unittest
import json
from harc.system.RestRequest import RestRequest

class TestHarcRest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def post(self, url, message):
        headers = {"Content-Type": "application/json"}
        certificate = None
        proxies = None

        response = RestRequest.post(headers, url, message, certificate, proxies)
        return response

    def test_deploy(self):
        url = 'http://localhost:5000/deploy'
        message = dict()
        message['project'] = "mdp_api"
        response = self.post(url, message)

        status_code = str(response.status_code)
        expected = "200"
        self.assertEquals(status_code, expected, 'invalid status_code expected ' + expected + ' was ' + status_code)

        content = json.loads(response.content)
        print content

        status = str(content['status'])
        expected = "200"
        message = 'invalid status expected ' + expected + ' was ' + status
        self.assertEquals(status, expected, message)


        # keys = content.keys()
        # expected = "databases"
        # self.assertTrue(expected in keys, 'invalid key expected ' + expected)


if __name__ == '__main__':
    unittest.main()
