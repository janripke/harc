import unittest
import json
from requests import post


class TestPropertyRepository(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_status(self):
        message = {"username": "harc@oxyma.nl", "password": "******"}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/login', json.dumps(message), headers=headers)
        self.assertEqual(response.status_code, 200, 'invalid response')

        content = json.loads(response.content)
        session = content['session']

        message = {"session": session, "job_name": "JOB$_8"}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/status', json.dumps(message), headers=headers)
        content = json.loads(response.content)

        if response.status_code == 200:
            for c in content:
                print c['logtype_code'], c['message']

    def test_job(self):
        message = {"username": "harc@oxyma.nl", "password": "******"}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/login', json.dumps(message), headers=headers)
        self.assertEqual(response.status_code, 200, 'invalid response')

        content = json.loads(response.content)
        session = content['session']

        message = {"command": "git:deploy", "session": session, "-u": "jan.ripke", "-p": "*Drapje01*", "-v": "1.0.0"}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/job', json.dumps(message), headers=headers)

        content = json.loads(response.content)
        print response.status_code, content['message'], content['job_name']
        self.assertEqual(response.status_code, 200, 'invalid response')

        message = {"session": session, "job_name": content['job_name']}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/status', json.dumps(message), headers=headers)
        content = json.loads(response.content)

        if response.status_code == 200:
            for c in content:
                print c['logtype_code'], c['message']

    def test_login(self):
        message = {"username": "harc@oxyma.nl", "password": "******"}
        headers = {'Content-Type': 'application/json'}
        response = post('http://127.0.0.1:5001/login', json.dumps(message), headers=headers)

        content = json.loads(response.content)
        print response.status_code, content['message']
        self.assertEqual(response.status_code, 200, 'invalid response')


if __name__ == '__main__':
    unittest.main()



