#zhanchen
import unittest
import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
URI = 'postgresql://cs162_user:cs162_password@db/cs162'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    value = db.Column(db.Numeric)
    now = db.Column(db.TIMESTAMP)



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
