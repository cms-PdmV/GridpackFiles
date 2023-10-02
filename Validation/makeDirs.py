import os
import sys

try:
    if (sys.argv[1] == "doit"):
        doit=True
    else:
        doit=False
except:
    doit=False

path = "/eos/cms/store/group/phys_generator/cvmfs/gridpacks/PdmV/"
campaigns = os.listdir("../Campaigns")
generators = os.listdir("../Cards")

for g in generators:
    processes = os.listdir(f"../Cards/{g}")
    for p in processes:
        for c in campaigns:
            fullpath = os.path.join(path, c, g, p)
            if not os.path.exists(fullpath):
                print (fullpath)
                if doit:
                    os.system(f"mkdir -p {fullpath}")
