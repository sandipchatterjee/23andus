#!/usr/bin/env python3

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask_wtf import Form
from pymongo import MongoClient

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
client = MongoClient('localhost', 27017)

import twentythreeandus.views
