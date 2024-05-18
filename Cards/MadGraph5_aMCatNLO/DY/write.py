import os

template="DYto2L-4Jets_MLL-50_PTLL-XX1toXX2_madgraphMLM-pythia8"

ptlls = ["40", "100", "200", "400", "600", "-1"]

for j, h in enumerate(ptlls):
        if h == "-1":
            continue
        new_file = template.replace("XX1", ptlls[j]).replace("XX2", ptlls[j+1]).replace("to-1", "")
        os.system(f"mkdir -p {new_file}")

        os.system(f"cp temp/temp_proc_card.dat {new_file}/{new_file}_proc_card.dat")
        os.system(f"sed -i '' -e 's|__output__|{new_file}|g' {new_file}/{new_file}_proc_card.dat")

        os.system(f"cp temp/temp.json {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|XX1|{ptlls[j]}|g' {new_file}/{new_file}.json")
        os.system(f"sed -i '' -e 's|XX2|{ptlls[j+1]}|g' {new_file}/{new_file}.json")

