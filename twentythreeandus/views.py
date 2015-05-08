#!/usr/bin/env python3

from flask import render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Required, Email
from twentythreeandus import app
from twentythreeandus import client

@app.route('/')
def index():
    db = client.testdb.testdb
    rec = db.find_one()
    return render_template('index.html', record=rec)

@app.route('/pool')
def pool():
    return render_template('pool.html')

