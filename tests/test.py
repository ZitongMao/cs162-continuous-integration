#zhanchen
import unittest
import requests
from web.app import Expression

class IntergrationTest(unittest.TestCase):

    def test_right_expression(self):
        expression = "1 + 1"
        r = requests.post('http://web:5000', data = {'expression':expression})
        inserted = Expression.query.filter(text=expression).first()
        self.assertEqual(inserted.text, expression)

    def test_wrong_expression(self):
        expression = "12 ++ 2"
        r = requests.post('http://web:5000', data = {'expression':expression})
        inserted = Expression.query.filter(text=expression).first()
        self.assertEqual(inserted, None)
