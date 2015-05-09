#!/usr/bin/env python3

# from reference import References
from random import randint
from collections import defaultdict
HETERO = ['1/0','0/1','0/0']
female_names = ['Sophia','Emma','Olivia','Ava','Isabella','Mia','Zoe','Lily','Emily','Madelyn','Madison','Chloe','Charlotte','Aubrey','Avery','Abigail','Kaylee','Layla','Harper','Ella','Amelia','Arianna','Riley','Aria','Hailey','Hannah','Aaliyah','Evelyn','Addison','Mackenzie','Adalyn','Ellie','Brooklyn','Nora','Scarlett','Grace','Anna','Isabelle','Natalie','Kaitlyn','Lillian','Sarah','Audrey','Elizabeth','Leah','Annabelle','Kylie','Mila','Claire','Victoria','Maya','Lila','Elena','Lucy','Savannah','Gabriella','Callie','Alaina','Sophie','Makayla','Kennedy','Sadie','Skyler','Allison','Caroline','Charlie','Penelope','Alyssa','Peyton','Samantha','Liliana','Bailey','Maria','Reagan','Violet','Eliana','Adeline','Eva','Stella','Keira','Katherine','Vivian','Alice','Alexandra','Camilla','Kayla','Alexis','Sydney','Kaelyn','Jasmine','Julia','Cora','Lauren','Piper','Gianna','Paisley','Bella','London','Clara','Cadence']
male_names = ['Jackson','Aiden','Liam','Lucas','Noah','Mason','Ethan','Caden','Jacob','Logan','Jayden','Elijah','Jack','Luke','Michael','Benjamin','Alexander','James','Jayce','Caleb','Connor','William','Carter','Ryan','Oliver','Matthew','Daniel','Gabriel','Henry','Owen','Grayson','Dylan','Landon','Isaac','Nicholas','Wyatt','Nathan','Andrew','Cameron','Dominic','Joshua','Eli','Sebastian','Hunter','Brayden','David','Samuel','Evan','Gavin','Christian','Max','Anthony','Joseph','Julian','John','Colton','Levi','Muhammad','Isaiah','Aaron','Tyler','Charlie','Adam','Parker','Austin','Thomas','Zachary','Nolan','Alex','Ian','Jonathan','Christopher','Cooper','Hudson','Miles','Adrian','Leo','Blake','Lincoln','Jordan','Tristan','Jason','Josiah','Xavier','Camden','Chase','Declan','Carson','Colin','Brody','Asher','Jeremiah','Micah','Easton','Xander','Ryder','Nathaniel','Elliot','Sean','Cole']
import random

class Person: ## new from Naisha
    '''Person class has the following attributes:
    personID,gender, avatarImage, ethnicity, freckles,hairColor,eyeColor,brow,chin,matchScore'''
    def __init__(self,personID,gender="male",avatarImage="image/default.jpg",
                 ethnicity=None,freckles=False,hairColor="black",
                 eyeColor="darkBrown",brow="normal",chin="normal",
                 genotype=None,matchScore=0):
        self.personID=personID
        self.gender = gender
        self.avatarImage=avatarImage
        self.ethnicity=ethnicity
        self.freckles=freckles
        self.hairColor=hairColor
        self.eyeColor=eyeColor
        self.brow=brow
        self.chin=chin
        self.matchScore=matchScore
        self.genotype = genotype
        
        if self.gender == 'male':
            self.personName = random.choice(male_names)
        else:
            self.personName = random.choice(female_names)

    def get(self, attr):
        return self.attr        
        
    def _calc_freckles(self):
        """
        True if freckles
        """
        genotype = self.genotype
        freckles = {'rs1042602': ['0/0'], 'rs4911414': HETERO, 'rs1015362':['0/0'], 'rs1015362':HETERO, 'rs4778138': ['0/0']}
        no_freckles = {'rs2153271': ['0/0'], 'rs4911414': ['1/1'], 'rs1015362':['A/A']}    
        
        freckles_score = 0
        for rsid,g in genotype.items():
            if rsid in freckles and g in freckles[rsid]:
                freckles_score +=1
            if rsid in no_freckles and g in no_freckles[rsid]:
                freckles_score -=1
            
        return freckles_score > 0
        
    def _calc_hair(self):
        hair = {'blonde': {'rs9544611': ['0/0'], 'rs12821256': ['1/1'], 'rs35264875': ['0/0'], 'rs12896399': ['0/1','1/0'], 'rs3829241': ['0/1','1/0'], 'rs1805005': ['1/1']},
                'brown_black': {'rs1667394': ['0/0'], 'rs16891982': ['0/0','0/1','1/0']},
                'redhead': {'rs1805009': ['0/1','1/0'], 'rs1805007': ['1/1'], 'rs1805008': ['1/1'], 'rs11547464': HETERO}}
        return score_feature(hair, self.genotype)
    
    def _calc_eye(self):
        eye = {'brown': {'rs1800401': ['0/1', '1/1', '1/0'], 'rs7495174': HETERO},
               'blue': {'rs1800401': ['0/0'], 'rs7495174': ['0/0']}}
        return score_feature(eye, self.genotype)
    
    def _calc_brow(self):
        brow = {False: {'rs649057': HETERO}, True: {'rs649057': '0/0'}}
        return score_feature(brow, self.genotype)
        
    def _calc_chin(self):
        chin = {False: {'rs10985112': HETERO}, True: {'rs10985112': '0/0'}}
        return score_feature(chin, self.genotype)
    
    def calc_features(self):
        self.freckles = self._calc_freckles()
        self.hairColor = self._calc_hair()
        self.eyeColor = self._calc_eye()
        self.brow = self._calc_brow()
        self.chin = self._calc_chin()
    
def score_feature(feature_dict, genotype):
    possibilities = list(feature_dict.keys())
    scores = defaultdict(int)
    for color, color_dict in feature_dict.items():
        for rsid,g in genotype.items():
            if rsid in color_dict and g in color_dict[rsid]:
                scores[color] += 1
    if len(scores) == 0 or max(scores.values()) == 0:
        return possibilities[randint(0,len(scores))]
    return sorted(scores, key = lambda x: x[1])[0]

     
    
class Person_old(object):

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
            
    