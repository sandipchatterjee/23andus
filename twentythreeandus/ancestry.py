
#ancestry_file = "/home/gstupp/23andme/iadmix/sandip.populations.ID001.input.ancestry"
import subprocess

def ancestry_from_iadmix(ancestry_file):
    """
    reads in output of iadmix
    outputs a dict where keys are populations, values are float, range 0-1
    representing fraction of each population
    """
    with open(ancestry_file) as file:
        for line in file:
            if not line.count("FINAL_NZ_PROPS"):
                continue
            line_split = line.strip().split()
            ancestry = dict()
            for x in line_split[:-1]:
                pop, per = x.split(':')
                ancestry[pop] = float(per)
    return ancestry
    
# imagemagick command  
# composite -blend 30x70% 1.jpg 2.jpg out.jpg
    
def generate_avatar(ancestry):
    # Take top two populations and blend representative images
    anc1, anc2 = sorted(ancestry.items(), key = lambda x: x[1], reverse = True)[:2]
    
    # get image representing anc1 / 2
    anc1_path = "1.jpg"
    anc2_path = "2.jpg"
    out_path = "out_1.jpg"
    
    command = ["composite", "-blend", str(int(anc1[1]*100))+'x'+str(int(anc2[1]*100))+'%', anc1_path, anc2_path, out_path]
    
    subprocess.call(command)
    
def calculate_population(path_to_23_file, name):
    """
    Do this stuff:
    Command to convert 23andme to ped/map
    >plink --23file genome_Sandip_Chatterjee_Full_20150507203425.txt --recode --out sandip --make-bed
    Run ancestry
    python runancestry.py --freq hapmap3.allchroms.shared.matrix --plink sandip --out sandip.ancestry
    """
    pass

    # convert 23andme to bed/bim/bam
    command = ['plink', '--23file', path_to_23_file, '--record','--out', name, '--make-bed']
    subprocess.call(command)
    
    # run ancestry
    command = ['python', 'runancestry.py', '--freq', 'hapmap3.allchroms.shared.matrix', '--plink', name, '--out', name + '.ancestry']
    subprocess.call(command)
    
    