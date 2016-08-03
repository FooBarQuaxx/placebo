"""Tests for main placebo interface and functionality."""
import json
import unittest
import requests
from placebo import Placebo


class GetMock(Placebo):
    # Test related data that will be used in tests.
    item = {'name': 'Huseyin', 'last_name': 'Yilmaz'}
    item2 = {'name': 'Mert', 'last_name': 'Yilmaz'}
    url2 = 'http://www.example2.com/api/item'
    # Data for placebo interface
    url = 'http://www.example.com/api/item'
    body = json.dumps(item)
    headers = {'content-type': 'application/json',
               'custom-header': 'OK'}


class StringValuesTestCase(unittest.TestCase):

    @GetMock.decorate
    def test_get(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), GetMock.item)
        self.assertEqual(response.headers, GetMock.headers)

    @GetMock.decorate(status=500)
    def test_get_update_status(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), GetMock.item)
        self.assertEqual(response.headers, GetMock.headers)

    @GetMock.decorate(body=json.dumps(GetMock.item2))
    def test_get_update_body(self):
        response = requests.get(GetMock.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), GetMock.item2)
        self.assertEqual(response.headers, GetMock.headers)