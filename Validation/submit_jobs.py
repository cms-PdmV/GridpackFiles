#!/usr/bin/env python3

import os
import sys
import time
import argparse

CWD = os.getcwd()
PREPID_HEADER = "GEN-Run3Summer22wmLHEGS"

def parse_arguments() :

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--nevents",\
                        action="store", dest="nevents", default="400",\
                        help = "number of events to submit per job")

    parser.add_argument("-d", "--dirname",\
                        action="store", dest="dirname", required = True,\
                        help = "name of job submission directory")

    parser.add_argument("-i", "--prepids",\
                        action="store", dest="prepids", required = True,\
                        help = "prepids to submit")

    return parser.parse_args()

def set_prepids(prepids) :

    prepids_to_submit = []
    for prepid_ in prepids.split(","):
        if "-" in prepid_ :
            start = prepid_.split("-")[0]
            end = prepid_.split("-")[1]
            if int(start) > int(end) :
                sys.exit(f"ERROR :: Arrange prepids properly : smaller to larger number")
            for prepid in range(int(start), int(end)+1) :
                prepid = str(prepid).zfill(5)
                prepids_to_submit.append(f"{PREPID_HEADER}-{prepid}")
        else :
            prepid = str(prepid_).zfill(5)
            prepids_to_submit.append(f"{PREPID_HEADER}-{prepid}")

    print (f"LOG :: Parsing prepids {prepids}")
    for prepid in prepids_to_submit:
        print (f"LOG :: {prepid}")

    return prepids_to_submit

def set_nevents(nevents):

    nevents = int(nevents)

    nevents_gensim = min(max(nevents, 300), 1000)
    nevents_gen    = min(max(nevents*10, 5000), 10000)

    print (f"LOG :: Setting number of events")
    print (f"LOG :: Given nevents {nevents} with option")
    print (f"LOG :: Set nevents_gen {nevents_gen}")
    print (f"LOG :: Set nevents_gensim {nevents_gensim}")

    return nevents_gen, nevents_gensim

def submit_jobs(dirname, prepid, nevents) :

    nevents_gen, nevents_gensim = set_nevents(nevents)
 
    os.system(f"cp template/condor.jds {dirname}/{prepid}.jds")
    os.system(f"cp template/run.sh {dirname}/{prepid}.sh")

    os.system(f"sed -i 's|__nevents_gensim__|{nevents_gensim}|g' {dirname}/{prepid}.sh")
    os.system(f"sed -i 's|__nevents_gen__|{nevents_gen}|g' {dirname}/{prepid}.sh")

    os.system(f"sed -i 's|__prepid__|{prepid}|g' {dirname}/{prepid}.sh")
    os.system(f"sed -i 's|__prepid__|{prepid}|g' {dirname}/{prepid}.jds")

    os.chdir(dirname)
    os.system(f"condor_submit {prepid}.jds")
    os.chdir(CWD)

def main() :

    args = parse_arguments()
    prepids = args.prepids
    nevents = args.nevents
    dirname = args.dirname

    if os.path.exists(dirname) : 
        sys.exit(f"ERROR :: dirname {dirname} exists, try different name")
    os.system(f"mkdir {dirname}")

    prepids_to_submit = set_prepids(prepids)
    for prepid in prepids_to_submit :
        submit_jobs(dirname, prepid, nevents)

if __name__ == "__main__" :

    main()
