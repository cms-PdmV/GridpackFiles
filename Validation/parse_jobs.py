#!/usr/bin/env python3

import os
import sys
import time
import pickle
import argparse

FUDGE_FACTOR = 50
PREPID_HEADER = "GEN-Run3Summer22wmLHEGS"
MAXNEVENTS = 150000000
MINNEVENTS =    200000
FIXNEVENTS =        -1

def parse_arguments() :

    parser = argparse.ArgumentParser()

    parser.add_argument("dirname",\
                        action="store",\
                        help = "name of job submission directory")

    parser.add_argument("--maxnevents",\
                        action="store", dest="maxnevents", default=150000000,\
                        help = "max number of events to request")

    parser.add_argument("--minnevents",\
                        action="store", dest="minnevents", default=   200000,\
                        help = "min number of events to request")

    parser.add_argument("--fixnevents",\
                        action="store", dest="fixnevents", default=       -1,\
                        help = "fix number of events to request")

    return parser.parse_args()

def set_prepids(dirname) :

    dirname_files = os.listdir(dirname)

    prepids_to_parse = []

    for dirname_file in dirname_files :
        if dirname_file.endswith(".stderr") :
            prepid = dirname_file.replace(".stderr", "")
            prepids_to_parse.append(prepid)

    return prepids_to_parse

def parse_logfile(dirname, prepid) :

    pickle = {}

    with open(f"{dirname}/{prepid}.stderr") as f :
        for l in reversed(f.readlines()) :
            l = l.strip()
            if "total cross section" in l :
                if "Before matching:" in l :
                    before = float(l.split("=")[1].split("+-")[0])
                if "After matching:" in l :
                    after = float(l.split("=")[1].split("+-")[0])
            if "Avg event:" in l :
                time = float(l.split(":")[1])

        filtereff = round(after/before, 2)
        if filtereff < 0.1 :
            print (f"{prepid} very small in filtereff {filtereff} <====== WARNING")

        crosssection = after
        nevents = truncate(crosssection * 50 * 1000 * 1./4.5 * FUDGE_FACTOR)

        if FIXNEVENTS < 0 :
            if nevents < MINNEVENTS :
                print (f"{prepid} very small in nevents {nevents}, setting {MINNEVENTS}")
                nevents = MINNEVENTS
            if nevents > MAXNEVENTS :
                print (f"{prepid} very large in nevents {nevents}, setting {MAXNEVENTS} <====== WARNING")
                nevents = MAXNEVENTS
        else :
            print (f"{prepid} fixed to nevents {nevents}, setting {FIXNEVENTS}")
            nevents = FIXNEVENTS

        pickle['prepid'] = prepid
        pickle['filtereff'] = filtereff
        pickle['nevents'] = nevents
        pickle['time'] = time
    return pickle

def main() :

    args = parse_arguments()
    dirname = args.dirname

    global MAXNEVENTS
    MAXNEVENTS = int(args.maxnevents)
    global MINNEVENTS
    MINNEVENTS = int(args.minnevents)
    global FIXNEVENTS
    FIXNEVENTS = int(args.fixnevents)
    prepids_to_parse = set_prepids(dirname)

    pickles_parsed = []
    for prepid in prepids_to_parse :
        parse_pickle = parse_logfile(dirname, prepid)
        pickles_parsed.append(parse_pickle)

    with open(f'{dirname}/prepids.pickle', 'wb') as f:
        pickle.dump(pickles_parsed, f)
        print(pickles_parsed)
        print(f"pickle file dumped to {dirname}/prepids.pickle")
        os.system(f"xrdcp {dirname}/prepids.pickle root://eosuser.cern.ch//eos/cms/store/user/shjeon/Run3Sample/{dirname.replace('/','')}.pickle")

def truncate(nevents):

    round_number = 100000
    truncated = int(int((nevents + round_number-1) / round_number) * round_number)

    return truncated

if __name__ == "__main__" :

    main()
