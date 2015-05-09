#!/usr/bin/env python3

from flask import render_template, session, request, redirect, url_for, flash, Markup
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField, HiddenField
from wtforms.validators import Required

from werkzeug import secure_filename
from flask_wtf.file import FileField, FileRequired

from twentythreeandus import app
from twentythreeandus import client
# from twentythreeandus.person import Person
from twentythreeandus.vcf_tools import convert_23andme
from twentythreeandus import genotypematchme

class SubmitForm(Form):
    """SubmitForm is a WTForm Form object for searching for uploading 23andMe data"""
    your_name = StringField('Your name:', validators=[Required()])
    # opposite_sex = BooleanField('Only consider opposite sex matches')
    data_file = FileField('Your 23andMe data file', validators=[Required()])
    submit = SubmitField('Upload Data')

class FindMatchForm(Form):
    """FindMatchForm is a WTForm Form object for searching for a 23andUs match"""
    # your_name = StringField('Your name:', validators=[Required()])

    # EyeColor
    HairColor = SelectField('Hair color:', choices=[('any', 'Any'), ('black', 'Black'), ('brown','Brown'), ('blond','Blond'), ('red','Red')], validators=[Required()])

    opposite_sex = BooleanField('Only consider opposite sex matches')
    # data_file = FileField('Your 23andMe data file', validators=[Required()])

    submit = SubmitField('Find My Match')

@app.route('/', methods=['GET', 'POST'])
def index():

    submit_form = SubmitForm()

    # db = client.testdb.testdb
    # rec = db.find_one()

    if submit_form.validate_on_submit():
        # session['filename'] = secure_filename(submit_form.data_file.name)

        if request.method == 'POST':
            message = Markup('File successfully uploaded and converted! <a href="{}">Click here to continue</a>'.format(url_for('findmatch')))
            flash(message)

        session['username'] = submit_form.your_name.data
        session['filename'] = submit_form.your_name.data+'_'+secure_filename(submit_form.data_file.name)

        new_filepath = app.config['UPLOAD_FOLDER'] + '/' + session['filename']
        submit_form.data_file.data.save(new_filepath)

        session['uploaded'] = True

        # convert new file to VCF
        vcf_filepath = convert_23andme(new_filepath)
        session['vcf_filepath'] = vcf_filepath

        return redirect(url_for('index'))

    return render_template('index.html', form=submit_form)

@app.route('/findmatch', methods=['GET', 'POST'])
def findmatch():

    findmatch_form = FindMatchForm()

    if findmatch_form.validate_on_submit():
        if request.method == 'POST':
            # message = Markup('Working on your match...')
            # flash(message)
            return redirect(url_for('yourmatch'))

    return render_template('findmatch.html', vcf_filepath=session['vcf_filepath'], username=session['username'], form=findmatch_form)

@app.route('/yourmatch')
def yourmatch():

    vcf_file = session['vcf_filepath']
    person_list = genotypematchme.score_me(submitter_vcf = vcf_file,submitter_gender = 'male')

    return render_template('yourmatch.html', person_list=person_list, username=session['username'])

@app.route('/pool')
def pool():
    return render_template('pool.html')

