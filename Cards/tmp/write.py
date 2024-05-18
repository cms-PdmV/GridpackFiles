import os

name = "WtoLNu-2Jets_MLNu-XX1toXX2_amcatnloFXFX-pythia8"

mlnus = [120, 200, 400, 800, 1500, 2500, 4000, 6000, -1]

for i, mlnu in enumerate(mlnus):

    newname = name.replace("XX1", str(mlnus[i])).replace("XX2", str(mlnus[i+1]))
    print (newname)
    os.mkdir(newname)
    os.system(f"cp {name}/{name}.json {newname}/{newname}.json")
    os.system(f"cp {name}/{name}_proc_card.dat {newname}/{newname}_proc_card.dat")
    os.system(f"cp {name}/{name}_madspin_card.dat {newname}/{newname}_madspin_card.dat")
    os.system(f"cp {name}/{name}_cuts.f {newname}/{newname}_cuts.f")

    os.system(f"sed -i '' 's|XX1|{mlnus[i]}|g' {newname}/{newname}_proc_card.dat")
    os.system(f"sed -i '' 's|XX2|{mlnus[i+1]}|g' {newname}/{newname}_proc_card.dat")

    os.system(f"sed -i '' 's|XX1|{mlnus[i]}|g' {newname}/{newname}_cuts.f")
    os.system(f"sed -i '' 's|XX2|{mlnus[i+1]}|g' {newname}/{newname}_cuts.f")

    if mlnus[i+1] == -1:
        break
