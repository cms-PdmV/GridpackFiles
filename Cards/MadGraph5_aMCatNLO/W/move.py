import os

cwd = os.getcwd()
samples = os.listdir("./")
print (samples)


for sample in samples:

    if sample.endswith(".py") : continue

    os.chdir(sample)

    files = os.listdir("./")
    for file in files:
        os.system(f"mv {file} {file.replace('DYto2L', 'WtoLNu')}")
        os.system(f"sed -i '' 's|{file.replace('DYto2L', 'WtoLNu')}|{file.replace('DYto2L', 'WtoLNu')}|g' *.dat")
    os.chdir(cwd)
    os.system(f"mv {sample} {sample.replace('DYto2L', 'WtoLNu')}")
