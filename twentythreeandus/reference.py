#!/usr/bin/env python3

import pandas as pd

class References(object):

    def __init__(self):
        self._references = self.parse_reference_vcf()

    def parse_reference_vcf(self):
        df = pd.io.parsers.read_table('23andme.vcf_filtered_filtered', header=None)
        df.index = df[2]
        df = df.iloc[:,9:(len(df.columns))]
        # vcf_filename = '23andme.vcf_filtered_filtered'
        # with open(vcf_filename) as f:
        #     first_line = f.readline()
        #     number_of_genomes = len(first_line.split()[10:])

        # for genome_number in range(number_of_genomes):
        #     ref_dict = {}
        #     with open(vcf_filename) as f:
        #         column_number = genome_number+10
        #         for line in f:
        #             linesplit = line.split()
        #             rsid = linesplit[2]
        #             # ref_dict[rsid] = linesplit[10:]
        #             ref_dict[rsid] = linesplit[12] # only using single genome

        #     references.append()

        # return references

    def __iter__(self):
        for reference_genome in self._references:
            yield reference_genome