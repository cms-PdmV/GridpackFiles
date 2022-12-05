import os

cwd = os.getcwd()
samples = os.listdir("./")
print (samples)


for sample in samples:

    if sample.endswith(".py") : continue

    os.chdir(sample)

    files = os.listdir("./")
#    for file in files:
#        os.system(f"mv {file} {file.replace('DYto2L', 'DYto2L-4Jets')}")

    os.chdir(cwd)
    print(f"sed -i '' 's|{sample.replace('-4Jets', '')}|{sample.replace('-4Jets', '').replace('DYto2L', 'DYto2L-4Jets')}|g' {sample}/{sample}_proc_card.dat")

#    os.system(f"mv {sample} {sample.replace('DYto2L', 'DYto2L-4Jets')}")
