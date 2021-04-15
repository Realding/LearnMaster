import json
import unittest
import requests
import urllib.parse
from pprint import pprint

from test_tools import random_name,random_phone


class BaseRestfulTest(unittest.TestCase):
    base_url = 'http://localhost:5000/user/'
    item_id = None

    @classmethod
    def setUpClass(cls):
        print("execute setUpClass")
        cls.name = random_name()

    @classmethod
    def tearDownClass(cls):
        # print("execute tearDownClass")
        pass

    def setUp(self):
        # print("execute setUp")
        pass

    def tearDown(self):
        # print("execute tearDown")
        pass

    def test_create(self):
        print("execute test_create")
        url = self.base_url
        data = {
            'username': self.name,
            'password': self.name,
            'phone': random_phone(),
        }
        res = requests.post(url, json=data)
        pprint(res.content.decode(encoding='utf-8'))
        self.assertEqual(res.status_code, 200)
        BaseRestfulTest.item_id = json.loads(res.content.decode(encoding='utf-8')).get('id')
        print(self.item_id)

    def test_query(self):
        print("execute test_query")
        url = self.base_url
        res = requests.get(url)
        pprint(res.content.decode(encoding='utf-8'))
        self.assertEqual(res.status_code, 200)

    def test_modify(self):
        print("execute test_modify")
        url = urllib.parse.urljoin(self.base_url, str(self.item_id))
        print(url)
        data = {
            'username': self.name,
            'password': self.name,
            'phone': random_phone(),
        }
        res = requests.put(url, json=data)
        pprint(res.content.decode(encoding='utf-8'))
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        print("execute test_delete")
        print(self.item_id)
        url = urllib.parse.urljoin(self.base_url, str(self.item_id))
        res = requests.delete(url)
        self.assertEqual(res.status_code, 204)

    def test_get(self):
        print("execute test_get")
        url = urllib.parse.urljoin(self.base_url, str(self.item_id))
        res = requests.get(url)
        pprint(res.content.decode(encoding='utf-8'))
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(BaseRestfulTest('test_create'))
    suite.addTest(BaseRestfulTest('test_modify'))
    suite.addTest(BaseRestfulTest('test_get'))
    suite.addTest(BaseRestfulTest('test_delete'))
    suite.addTest(BaseRestfulTest('test_query'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
