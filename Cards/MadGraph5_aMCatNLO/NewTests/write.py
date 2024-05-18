import os

template = "DYto2L-3Jets_MLL-50_PTLL-XX1toXX2_madgraphMLM-pythia8"

hts = [40, 100, 200, 400, 600, 1000, -1]

for i, htmin in enumerate(hts):
    if htmin == -1: continue
    htmax = hts[i+1]
    newname = template.replace('XX1',str(htmin)).replace('XX2',str(htmax)).replace('to-1', '')
    os.system(f"mkdir -p {newname}")
    os.system(f"cp {template}/{template}_proc_card.dat {newname}/{newname}_proc_card.dat")
    os.system(f"cp {template}/{template}.json {newname}/{newname}.json")
    os.system(f"sed -i '' 's|XX1|{htmin}|g' {newname}/{newname}_proc_card.dat")
    os.system(f"sed -i '' 's|XX2|{htmax}|g' {newname}/{newname}_proc_card.dat")

    os.system(f"sed -i '' 's|XX1|{htmin}|g' {newname}/{newname}.json")
    os.system(f"sed -i '' 's|XX2|{htmax}|g' {newname}/{newname}.json")

