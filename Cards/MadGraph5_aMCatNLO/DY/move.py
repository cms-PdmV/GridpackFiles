import os

sample_old = "DYto2L-2Jets_0J_amcatnloFXFX-pythia8"
sample_new = "DYto2L-2Jets_2J_amcatnloFXFX-pythia8"

os.system(f"cp -r {sample_old} {sample_new}")

files = os.listdir(sample_new)
os.chdir(sample_new)
for file in files:
    os.system(f"mv {file} {file.replace('_0J_', '_2J_')}")

'''
cwd = os.getcwd()
samples = os.listdir("./")


for sample in samples:

    if sample.endswith(".py") : continue

    os.chdir(sample)

    files = os.listdir("./")
#    for file in files:
#        os.system(f"mv {file} {file.replace('DYto2L', 'DYto2L-4Jets')}")

    os.chdir(cwd)
    print(f"sed -i '' 's|{sample.replace('-4Jets', '')}|{sample.replace('-4Jets', '').replace('DYto2L', 'DYto2L-4Jets')}|g' {sample}/{sample}_proc_card.dat")

#    os.system(f"mv {sample} {sample.replace('DYto2L', 'DYto2L-4Jets')}")
'''
