import os

cwd = os.getcwd()
samples = os.listdir("./")
print (samples)


for sample in samples:

    if sample.endswith(".py") : continue

    os.chdir(sample)

    files = os.listdir("./")
    for file in files:
        os.system(f"mv {file} {file.replace('DYto2L', 'DYto2L-4Jets')}")
    os.system(f"sed -i '' 's|{file}|{file.replace('DYto2L', 'DYto2L-4Jets')}|g' *.dat")

    os.chdir(cwd)
    os.system(f"mv {sample} {sample.replace('DYto2L', 'DYto2L-4Jets')}")
