#!/usr/bin/env python3

import subprocess

def convert_23andme(filepath):
    new_filename = filepath.split('/')[-1]
    new_filepath = 'data/{}.vcf'.format(new_filename)

    try:
        output = subprocess.check_output('bin/plink_mac/plink --23file {} --recode vcf --out data/{}'.format(filepath, new_filename), shell=True)
    except subprocess.CalledProcessError:
        print('plink call failed')
        raise

    subprocess.call('rm -rf data/*.hh', shell=True)
    subprocess.call('rm -rf data/*.log', shell=True)

    return new_filepath

def impute_sex(vcf_filepath):

    ## not working properly yet...

    try:
        output = subprocess.check_output('bin/plink_mac/plink --vcf {} --make-bed --imputesex --out data/{}'.format(vcf_filepath), shell=True)
    except subprocess.CalledProcessError:
        print('plink call failed')
        raise

    return 'Male'