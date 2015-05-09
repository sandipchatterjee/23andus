
genotype = {'rs4911414': '0/0', 'rs4778138': '1/1', 'rs1015362': '0/1', 
'rs12821256': '0', 'rs1805007': '0/1', 'rs1805008': '1/1'}


from random import randint
from collections import defaultdict
HETERO = ['1/0','0/1','0/0']
def calc_freckles(genotype):
    """
    True if freckles
    """
    
    freckles = {'rs1042602': ['0/0'], 'rs4911414': HETERO, 'rs1015362':['0/0'], 'rs1015362':HETERO, 'rs4778138': ['0/0']}
    no_freckles = {'rs2153271': ['0/0'], 'rs4911414': ['1/1'], 'rs1015362':['A/A']}    
    
    freckles_score = 0
    for rsid,g in genotype.items():
        if rsid in freckles and g in freckles[rsid]:
            freckles_score +=1
        if rsid in no_freckles and g in no_freckles[rsid]:
            freckles_score -=1
        
    return freckles_score > 0
    
def calc_hair(genotype):
    hair = {'blonde': {'rs9544611': ['0/0'], 'rs12821256': ['1/1'], 'rs35264875': ['0/0'], 'rs12896399': ['0/1','1/0'], 'rs3829241': ['0/1','1/0'], 'rs1805005': ['1/1']},
            'brown_black': {'rs1667394': ['0/0'], 'rs16891982': ['0/0','0/1','1/0']},
            'redhead': {'rs1805009': ['0/1','1/0'], 'rs1805007': ['1/1'], 'rs1805008': ['1/1'], 'rs11547464': HETERO}}
    return score_feature(hair, genotype)

def calc_eye(genotype):
    eye = {'brown': {'rs1800401': ['0/1', '1/1', '1/0'], 'rs7495174': HETERO},
           'blue': {'rs1800401': ['0/0'], 'rs7495174': ['0/0']}}
    return score_feature(eye, genotype)

def calc_brow(genotype):
    brow = {False: {'rs649057': HETERO}, True: {'rs649057': '0/0'}}
    return score_feature(brow, genotype)
    
def calc_chin(genotype):
    chin = {False: {'rs10985112': HETERO}, True: {'rs10985112': '0/0'}}
    return score_feature(chin, genotype)
    
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

    
    
    
    
    
    
def calc_features(genotype):
    
    freckles = calc_freckles(genotype)
    hairColor = calc_hair(genotype)
    eyeColor = calc_eye(genotype)
    brow = calc_brow(genotype)
    chin = calc_chin(genotype)
    
    return 
    