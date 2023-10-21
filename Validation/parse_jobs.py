#!/usr/bin/env python3

import os
import sys
import time
import pickle
import argparse

FUDGE_FACTOR = 30
PREPID_HEADER = "GEN-Run3Summer22wmLHEGS"
MAXNEVENTS = 150000000
MINNEVENTS =    500000
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
        if dirname_file.endswith(".sh") :
            prepid = dirname_file.replace(".sh", "")
            prepids_to_parse.append(prepid)

    return prepids_to_parse

def parse_logfile(dirname, prepid) :

    pickle = {}

    filter_eff = -1
    cross_section = -1
    with open(f"{dirname}/{prepid}.run_gen.log", encoding='utf-8') as f :
        for l in reversed(f.readlines()) :
            l = l.strip()
            if "cross section" in l :
                if "Before matching:" in l :
                    before = float(l.split("=")[1].split("+-")[0])
                if "After filter:" in l :
                    after = float(l.split("=")[1].split("+-")[0])
                    cross_section = after
        filter_eff = round(after/before, 2)

    time_per_event = -1
    with open(f"{dirname}/{prepid}.run_gensim.log", encoding='utf-8') as f :
        for l in reversed(f.readlines()) :
            l = l.strip()
            if "Avg event:" in l :
                time_per_event = float(l.split(":")[1])

    if filter_eff < 0:
        sys.exit(f"ERROR :: filter_eff {filter_eff} < 0")
    if cross_section < 0:
        sys.exit(f"ERROR :: cross_section {cross_section} < 0")
    if time_per_event < 0:
        sys.exit(f"ERROR :: time_per_event {time_per_event} < 0")

    if filter_eff < 0.1 :
        print (f"{prepid} very small in filter_eff {filter_eff} <====== WARNING")

    nevents = truncate(cross_section * 50 * 1000 * 1./4.5 * FUDGE_FACTOR)

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
    pickle['filter_eff'] = filter_eff
    pickle['nevents'] = nevents
    pickle['time_per_event'] = time_per_event

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
        for pickle_parsed in pickles_parsed:
            print(pickle_parsed)
        print(f"pickle file dumped to {dirname}/prepids.pickle")

def truncate(nevents):

    round_number = 100000
    truncated = int(int((nevents + round_number-1) / round_number) * round_number)

    return truncated

if __name__ == "__main__" :

    main()
