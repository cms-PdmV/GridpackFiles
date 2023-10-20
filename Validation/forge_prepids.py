#!/usr/bin/env python3

import os
import sys
import time
import pickle
import argparse

sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

mcm = McM(dev=False)

CLONE_TARGETS = {
"Run3Summer22EEwmLHEGS" : 3.5,
"Run3Summer23wmLHEGS" : 2.,
"Run3Summer23BPixwmLHEGS" : 1.
}

def parse_arguments() :

    parser = argparse.ArgumentParser()

    parser.add_argument("pickle_file",\
                        action="store",\
                        help = "pickle file to submit to mcm")

    return parser.parse_args()

def edit_prepid(data) :

    prepid = data['prepid']
    filtereff = data['filtereff']
    nevents = data['nevents']
    time = data['time']

    request = mcm.get('requests', prepid)
    request['generator_parameters'][0]['filter_efficiency'] = filtereff
    request['total_events'] = nevents

    request['mcdb_id'] = 0
    request['generator_parameters'][0]['cross_section'] = 1.0
    request['generator_parameters'][0]['filter_efficiency_error'] = 0.0
    request['generator_parameters'][0]['match_efficiency'] = 1.0
    request['generator_parameters'][0]['match_efficiency_error'] = 0.0
    request['generator_parameters'][0]['negative_weights_fraction'] = 0.0
    request['size_event'][0] = 800.0
    request['time_event'][0] = time

    print (f"updating {prepid}")
    update=mcm.update('requests', request)

def clone_prepid(prepid) :

    print (f"cloning {prepid} ==========================")
    for CLONE_TARGET, SCALE in CLONE_TARGETS.items():
        request = mcm.get('requests', prepid)
        request["member_of_campaign"] = CLONE_TARGET
        request["total_events"] = request["total_events"] * SCALE

        clone_request = mcm.clone_request(request)
        print (f"\t{clone_request}")

def main() :

    args = parse_arguments()
    pickle_file = args.pickle_file

    data_to_submit = pickle.load(open(pickle_file, 'rb'))
    for data in data_to_submit :
        edit_prepid(data)
        clone_prepid(data['prepid'])

if __name__ == "__main__" :

    main()
