#!/usr/bin/env python3

from flask import render_template, session, request, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Required

from werkzeug import secure_filename
from flask_wtf.file import FileField, FileRequired

from twentythreeandus import app
from twentythreeandus import client

class SubmitForm(Form):
    """SubmitForm is a WTForm Form object for searching for a 23andUs match"""
    your_name = StringField('Your name:', validators=[Required()])
    opposite_sex = BooleanField('Only consider opposite sex matches')
    data_file = FileField('Your 23andMe data file', validators=[Required()])
    submit = SubmitField('Match')

@app.route('/', methods=['GET', 'POST'])
def index():

    submit_form = SubmitForm()

    # db = client.testdb.testdb
    # rec = db.find_one()

    if submit_form.validate_on_submit():
        # session['filename'] = secure_filename(submit_form.data_file.name)
        session['filename'] = submit_form.your_name.data+'_'+secure_filename(submit_form.data_file.name)

        new_file_path = app.config['UPLOAD_FOLDER'] + '/' + session['filename']
        submit_form.data_file.data.save(new_file_path)

        # do something with new file
        with open(new_file_path) as f:
            pass

        return redirect(url_for('index'))

    return render_template('index.html', form=submit_form)

@app.route('/pool')
def pool():
    return render_template('pool.html')

