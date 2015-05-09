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

'''
freckles:
True
False

hairColor:
blonde
brown_black 
blonde
redhead

eyeColor:
blue
brown
black

brow:
unibrow
normal

chin:
True
False

ethnicity:
European: EUR (coding for image) - FIN, CEU, TSI, GBR, IBS 
African: AFR (coding for image) - YRI, LWK, GWD, MSL, ESN, ASW, ACB
America: AMR (coding for image) - MXL, PUR, CLM, PEL
South Asian: SAS (coding for image) - GIH, PJL, BEB, STU, ITU
East Asian: EAS (coding for image) - CHB, JPT, CHS, CDX, KHV
'''

class FindMatchForm(Form):
    """FindMatchForm is a WTForm Form object for searching for a 23andUs match"""
    # your_name = StringField('Your name:', validators=[Required()])

    brow = SelectField('Eyebrow:', choices=[('any', 'Any'), ('unibrow', 'Unibrow'), ('normal','Non-unibrow')], validators=[Required()])
    freckles = SelectField('Freckles?', choices=[('any', 'Any'), (True, 'Yes'), (False, 'No')], validators=[Required()])
    chin = SelectField('Chin dimple?', choices=[('any', 'Any'), (True, 'Yes'), (False, 'No')], validators=[Required()])
    hairColor = SelectField('Hair color:', choices=[('any', 'Any'), ('brown_black', 'Brown/Black'), ('blonde','Blonde'), ('redhead','Red')], validators=[Required()])
    eyeColor = SelectField('Eye color:', choices=[('any', 'Any'), ('black', 'Black'), ('brown','Brown'), ('blue','Blue')], validators=[Required()])
    ethnicity = SelectField('Ethnicity:', choices=[('any', 'Any'), ('EUR', 'European'), ('AFR', 'African'), ('AMR', 'American'), ('SAS', 'South Asian'), ('EAS', 'East Asian')])

    # opposite_sex = BooleanField('Only consider opposite sex matches')
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

            filters = {}
            filters['hairColor'] = findmatch_form.hairColor.data
            filters['eyeColor'] = findmatch_form.eyeColor.data
            filters['freckles'] = findmatch_form.freckles.data
            filters['chin'] = findmatch_form.freckles.data
            filters['brow'] = findmatch_form.brow.data
            filters['ethnicity'] = findmatch_form.ethnicity.data

            session['filters'] = filters

            return redirect(url_for('yourmatch'))

    return render_template('findmatch.html', vcf_filepath=session['vcf_filepath'], username=session['username'], form=findmatch_form)

@app.route('/yourmatch')
def yourmatch():

    vcf_file = session['vcf_filepath']
    person_list = genotypematchme.score_me(submitter_vcf = vcf_file,submitter_gender = 'male')

    num_persons = len(person_list)

    for person in person_list:
        # person.calc_features()
        print(person.personID)

    # filtering, if any
    filters = session['filters']
    for filter_param in filters:
        if filters[filter_param] != 'any':
            person_list = [person for person in person_list if person.filter_param == filters[filter_param]]
            # continue
        # else:
        #     # filter person_list by filter_param
        #     #
        #     # for example, filter_param could be a eye_color, and filters['eye_color'] == 'brown'
        #     # ...this list comprehension will filter by this filter_param
            

    print(filters)
    print(len(person_list))

    return render_template('yourmatch.html', person_list=person_list[:50], num_persons=num_persons, username=session['username'])

@app.route('/test')
def test():
    return render_template('test.html')

