import os
import sys

generator = 'MadGraph5_aMCatNLO' #Powheg
path = sys.argv[1] #Cards/MadGraph5_aMCatNLO/DYJets/DYJets_0J_amcatnloFXFX-pythia8

if not os.path.exists(path):
    os.system("mkdir -p " + path)
else:
    sys.exit("error : " + path + " already exists")

process = path.split("/")[3]

skeleton_path = "Skeletons/" + generator + "/"

if (generator == "MadGraph5_aMCatNLO"):

    os.system("cp " + skeleton_path + "/skeleton.json " + path + "/" + process + ".json")
    os.system("cp " + skeleton_path + "/skeleton_madspin_card.dat " + path + "/" + process + "_madspin_card.dat")
    os.system("cp " + skeleton_path + "/skeleton_proc_card.dat " + path + "/" + process + "_proc_card.dat")
    os.system("sed -i '' 's|$process|" + process + "|g' " + path + "/" + process + "_proc_card.dat")

if (generator == "Powheg"):

    pass
