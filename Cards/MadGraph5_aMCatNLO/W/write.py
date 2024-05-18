import os

template="WBtoLNuB-4Jets_MLNu-XX1toXX2_HT-YY1toYY2_madgraphMLM-pythia8"

masses = ["0", "120", "-1"]
hts = ["40", "100", "400", "800", "1500", "2500", "-1"]

for i, m in enumerate(masses):
    if m == "-1":
        continue
    for j, h in enumerate(hts):
        if h == "-1":
            continue
        new_file = template.replace("XX1", masses[i]).replace("XX2", masses[i+1]).replace("YY1", hts[j]).replace("YY2", hts[j+1]).replace("to-1", "")
        print (new_file)
        os.system(f"mkdir -p {new_file}")
        os.system(f"cp {template}/{template}_proc_card.dat {new_file}/{new_file}_proc_card.dat")
        os.system(f"sed -i '' -e 's|{template}|{new_file}|g' {new_file}/{new_file}_proc_card.dat")
        os.system(f"cp {template}/{template}.json {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|XX1|{masses[i]}|g' {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|XX2|{masses[i+1]}|g' {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|YY1|{hts[j]}|g' {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|YY2|{hts[j+1]}|g' {new_file}/{new_file}.json")

