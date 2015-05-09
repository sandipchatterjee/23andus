#!/usr/bin/env python3

# Genotype Matching code

import pandas as pd
from twentythreeandus.person import Person

#Create a mendelian inheritance probability
def createProbDic():
    probability_dict = {}
    probability_dict['0/0_x_0/0'] = {'0/0': 1.0, '0/1': 0.0, '1/1': 0.0}
    probability_dict['0/0_x_0/1'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0}
    probability_dict['0/0_x_1/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0} #same as above
    probability_dict['0/0_x_1/1'] = {'0/0': 0.0, '0/1': 1.0, '1/1': 0.0}
    probability_dict['0/1_x_0/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0}
    probability_dict['1/0_x_0/0'] = {'0/0': 0.5, '0/1': 0.5, '1/1': 0.0} #same as above
    probability_dict['0/1_x_0/1'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25}
    probability_dict['1/0_x_0/1'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above
    probability_dict['1/0_x_1/0'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above
    probability_dict['0/1_x_1/0'] = {'0/0': 0.25, '0/1': 0.5, '1/1': 0.25} #same as above
    probability_dict['0/1_x_1/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5}
    probability_dict['1/0_x_1/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5} #same as above
    probability_dict['1/1_x_0/0'] = {'0/0': 0.0, '0/1': 1.0, '1/1': 0.0}
    probability_dict['1/1_x_0/1'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5}
    probability_dict['1/1_x_1/0'] = {'0/0': 0.0, '0/1': 0.5, '1/1': 0.5} #same as above
    probability_dict['1/1_x_1/1'] = {'0/0': 0.0, '0/1': 0.0, '1/1': 1.0}
    return probability_dict

def score_user_against_single_reference(submitter, single_ref_dict,probability_dict,matchmesnps):
    ''' score user against a single reference genome 
    dict with format:
        { rsid1: genotype1,
          rsid2: genotype2,
          ...
          }
        '''
    total_score = 0.0
    for rsid in submitter:
        user_genotype = submitter[rsid]
        if rsid not in single_ref_dict:
            continue
        if '.' in user_genotype: # can't deal with './.' missing genotypes
            continue
        ref_genotype = single_ref_dict[rsid]
        cross = user_genotype+'_x_'+ref_genotype
        probs = probability_dict[cross]

        good_bad_match = matchmesnps.loc[rsid]
        prob_choice = probs[good_bad_match[0]]
        magnitude = good_bad_match[1]
        total_score += (prob_choice * magnitude)

    return total_score

def score_me(submitter_vcf,submitter_gender):

    #Create Probability dict
    probability_dict=createProbDic()

    #Read SNPs that will be used to score the match
    matchmesnps= pd.read_table("data/SNPs_goodORbad_commonSNPs_01encoding.txt") #SNP_IDs,genotype,MaxMagnitude
    matchmesnps.set_index("SNP_IDs", inplace=True)

    #Read the reference pool to find the match
    referencePoolGeno = pd.read_table("data/23andme.vcf_filtered_filtered")
    referencePoolGeno.set_index("ID",inplace=True)

    #Read the gender and race information for the reference individuals
    referenceGenderRace = pd.read_table("data/referenceGenderRace2.txt")
    referenceGenderRace.set_index("IndividualID",inplace=True)

    #Read the submitter VCF file
    meGeno = pd.read_table(submitter_vcf,comment="#",header=None)
    meGeno.set_index(2,inplace=True)

    #Find common markers between all files
    t= meGeno.index.isin(matchmesnps.index) 
    t=meGeno.index[t]
    t1=meGeno.loc[t]
    t=t1.index.isin(referencePoolGeno.index)
    commonMarkers=t1.index[t]

    #print(matchmesnps.shape,referencePoolGeno.shape,meGeno.shape)

    matchmesnps=matchmesnps.loc[commonMarkers]
    referencePoolGeno=referencePoolGeno.loc[commonMarkers]
    meGeno=meGeno.loc[commonMarkers]

    #print(referenceGenderRace.head())
    #Find common reference sample with gender and race information
    if submitter_gender=="male":
        referenceGenderRace=referenceGenderRace[referenceGenderRace["Gender"]==2]
    else:
        referenceGenderRace=referenceGenderRace[referenceGenderRace["Gender"]==1]

    #print("\n",referenceGenderRace.shape,set(referenceGenderRace["Gender"]),referenceGenderRace.head())

    commonSamples=referenceGenderRace.index.isin(referencePoolGeno.columns[8:])
    commonSamples=referenceGenderRace.index[commonSamples]
    print(len(commonSamples))
    #print(matchmesnps.shape,referencePoolGeno.shape,meGeno.shape,set(referenceGenderRace.loc[commonSamples,"Gender"]))
    #print(matchmesnps.shape,matchmesnps.iloc[:5,:],matchmesnps.index[:5])
    #print("\n",referencePoolGeno.shape,referencePoolGeno.iloc[:3,:15]) #from 9 its genotypes
    #print("\n",meGeno.shape,meGeno.head()) #from 9 its genotypes
    #print("\n",referenceGenderRace.shape,referenceGenderRace.head())
    
    #Calculate match scores for all members of the reference pool
    submitter = meGeno[9].to_dict()

    score = {}
    for sample in commonSamples:
        single_ref_dict = referencePoolGeno[sample].to_dict()
        score[sample]=score_user_against_single_reference(submitter, single_ref_dict,probability_dict,matchmesnps)

    #print(type(score),len(score))

    #Sort the scores
    from collections import OrderedDict
    sorted_score=OrderedDict(sorted(score.items(), key=lambda item: item[1],reverse=True))

    # import Person

    person_list = []
    for sample in sorted_score.keys():
        #Create a Person object
        if referenceGenderRace.loc[sample,"Gender"]==2:
            gender="female"
        else:
            gender = "male"
        myPerson = Person(personID=sample,gender=gender,ethnicity=referenceGenderRace.loc[sample,"Population"],matchScore=sorted_score[sample]) #avatarImage="image/default.jpg",freckles=False,hairColor="black",eyeColor="darkBrown",brow="normal",chin="normal"
        #Add genotype
        myPerson.genotype = referencePoolGeno[sample].to_dict()
        #Add submitter_23 filename
        submitter_23=submitter_vcf.replace("data","upload")
        submitter_23=submitter_23.replace(".vcf","")
        myPerson.submitter_23 = submitter_23
        myPerson.calc_features()
        person_list.append(myPerson)
    
    ##Add more methods in the Person class once I get data from William
    
    return person_list