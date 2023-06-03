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

    if "-" in prepids :

        start = prepids.split("-")[0]
        end = prepids.split("-")[1]
        if int(start) > int(end) :
            sys.exit(f"arrange prepids properly : smaller to larger number")

        for prepid in range(int(start), int(end)+1) :
            prepid = str(prepid).zfill(5)
            prepids_to_submit.append(f"{PREPID_HEADER}-{prepid}")
    else :
        prepids_to_submit.append(f"{PREPID_HEADER}-{prepids}")

    return prepids_to_submit

def submit_jobs(dirname, prepid, nevents) :

    os.system(f"cp template/condor.jds {dirname}/{prepid}.jds")
    os.system(f"cp template/run.sh {dirname}/{prepid}.sh")

    os.system(f"sed -i 's|__nevents__|{nevents}|g' {dirname}/{prepid}.sh")
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
        sys.exit(f"{dirname} exists, try different name")
    os.system(f"mkdir {dirname}")

    prepids_to_submit = set_prepids(prepids)
    for prepid in prepids_to_submit :
        submit_jobs(dirname, prepid, nevents)

if __name__ == "__main__" :

    main()
