#!/usr/bin/env python3

# from reference import References

class Person(object):

    def __init__(self, filename):
        
        # Ancestry: http://www.1000genomes.org/faq/which-populations-are-part-your-study
        # One of ASW CEU CHB CHS CLM FIN GBR IBS JPT LWK MXL PUR TSI YRI (from hapmap3.8)
        self.ancestry = ''
        # One of ['EAS','EUR','AFR','AMR','SAS']
        self.super_population = ''

        self.good_bad_dict = self._make_good_bad_dict()
        self.rsid_dict = {}
        self._original_filename = filename
        # self._ref_dict = self._make_reference_dict()
        self._single_ref_dict = self._make_single_reference_dict()

        self.probability_dict = {}
        self.probability_dict['0/0_x_0/0'] = {'0/0': 1.0, '0/1': 0.0, '1/1': 0.0}

        self.probability_dict['0/0_x_0/1'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0}
        self.probability_dict['0/0_x_1/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0} #same as above

        self.probability_dict['0/0_x_1/1'] = {'0/0': 0.0, '0/1': 1.0, '1/1': 0.0}
        
        self.probability_dict['0/1_x_0/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0}
        self.probability_dict['1/0_x_0/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0} #same as above

        self.probability_dict['0/1_x_0/1'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25}
        self.probability_dict['1/0_x_0/1'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above
        self.probability_dict['1/0_x_1/0'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above
        self.probability_dict['0/1_x_1/0'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above

        self.probability_dict['0/1_x_1/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5}
        self.probability_dict['1/0_x_1/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5} #same as above

        self.probability_dict['1/1_x_0/0'] = {'0/0': 0.0, '0/1': 1.0, '1/1': 0.0}

        self.probability_dict['1/1_x_0/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5}
        self.probability_dict['1/1_x_1/0'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5} #same as above

        self.probability_dict['1/1_x_1/1'] = {'0/0': 0.0, '0/1': 0.0, '1/1': 1.0}

        with open(filename) as f: ## VCF file, 0/1 encoded version of 23andMe data
            for line in f:
                if not line.startswith('#'):
                    linesplit = line.split()
                    rsid, genotype = linesplit[2], linesplit[9]
                    # filter out all rsids for which we don't have magnitude info
                    if rsid in self.good_bad_dict:
                        self.rsid_dict[rsid] = genotype

    def _make_good_bad_dict(self):

        # read good/bad RSID file (with magnitudes)
        # good_bad_dict will have format like this:

        # dict[rs12345] = 1/0, 4.2

        good_bad_dict = {}

        with open('SNPs_goodORbad_commonSNPs_01encoding.txt') as f:
            f.readline() #throw away header
            for line in f:
                linesplit = line.split()
                rsid = linesplit[0]
                good_bad_dict[rsid] = linesplit[1], float(linesplit[2])

        return good_bad_dict

    # def _make_reference_dict(self):
    #     ref_dict = {}
    #     with open('23andme.vcf_filtered_filtered') as f:
    #         for line in f:
    #             linesplit = line.split()
    #             rsid = linesplit[2]
    #             ref_dict[rsid] = linesplit[10:]

    #     return ref_dict

    def _make_single_reference_dict(self):
        ref_dict = {}
        with open('23andme.vcf_filtered_filtered') as f:
            for line in f:
                linesplit = line.split()
                rsid = linesplit[2]
                # ref_dict[rsid] = linesplit[10:]
                ref_dict[rsid] = linesplit[12] # only using single genome

        return ref_dict

    def score_user_against_single_reference(self, single_ref_dict):
        
        ''' score user against a single reference genome 
        dict with format:
            { rsid1: genotype1,
              rsid2: genotype2,
              ...
              }
            '''

        total_score = 0.0
        for rsid in self.rsid_dict:
            user_genotype = self.rsid_dict[rsid]
            if rsid not in single_ref_dict:
                continue
            if '.' in user_genotype: # can't deal with './.' missing genotypes
                continue
            ref_genotype = single_ref_dict[rsid]
            cross = user_genotype+'_x_'+ref_genotype
            probs = self.probability_dict[cross]

            good_bad_match = self.good_bad_dict[rsid]
            prob_choice = probs[good_bad_match[0]]
            magnitude = good_bad_match[1]
            total_score += (prob_choice * magnitude)

        return total_score

    def score_user_against_all_genomes(self):
        length = len(self._ref_dict[0]) # number of columns
        for i in range(length):
            self.score_user_against_single_reference()