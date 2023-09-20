#!/usr/bin/env python3

import os
import sys
import time
import pickle
import argparse
import re

sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *

mcm = McM(dev=False)

# This dictionary defines changes to be applied between different campaigns
# Note: the lumi_sf is taken into account considering Run3Summmer22 as a 
#       reference.

CLONE_TARGETS = {
    "Run3Summer23wmLHEGS" : {
        "lumi_sf" : 2.0,
        "tags" : ["CloneTT23"] 
    },
    "Run3Summer23BPixwmLHEGS" : {
        "lumi_sf" : 1.0,
        "tags" : ["CloneTT23Bpix"] 
    },
}

# This dictionary defines regexpressions to match with McM queries
regexps = {
    "TT_powheg" : "TT*powheg*",
    "TW_powheg" : "TW*powheg*"
}

def parse_arguments() :

    parser = argparse.ArgumentParser()

    parser.add_argument("group",\
                        action="store",\
                        help = "Group of prepids to be fetch from McM.\
                                See into the regexps dictionary to see \
                                which ones are available")
    parser.add_argument("--submit",\
                        action="store_true",\
                        default = False,
                        help = "Group of prepids to be fetch from McM.\
                                See into the regexps dictionary to see \
                                which ones are available")

    return parser.parse_args()

def check_fragment_mmaxgamma(request):
    """ Function to fix mmaxgamma issue """ 
    # Extract processParameters block
    fragment = request["fragment"]
    match = re.search(r"processParameters = cms\.vstring\(([^)]+)\),", fragment)
    if not match:
        return fragment  # Return unchanged fragment if the block is not found

    block = match.group(1)
    if re.search(r"TimeShower:mMaxGamma = \S+", block):
        # Replace its value with 4
        new_block = re.sub(r"TimeShower:mMaxGamma = \S+", "TimeShower:mMaxGamma = 4", block)
    else:
        # If not present, append it before the closing parenthesis
        new_block = block.replace("\n", ",\n") + "'TimeShower:mMaxGamma = 4'\n        "
    
    # Replace the original block with the modified block in the main fragment
    request["fragment"] = fragment.replace(block, new_block)
    return

def clone_prepid(prepid, submit):
    """ Take a prepid as an input. Modify parameters and clone """
    # Clone for 2023 and 2023BPix
    for target, metadata in CLONE_TARGETS.items():
        print("    + Cloning request: %s into %s"%(prepid, target))

        # Get the request
        request = mcm.get('requests', prepid)
        
        # Modify parameters
        request["member_of_campaign"] = target
        request["total_events"] = request["total_events"] * metadata["lumi_sf"]
        check_fragment_mmaxgamma(request)

        if submit:
            clone_request = mcm.clone_request(request)
            print (f"\t{clone_request}")
        print(" --- ")

def main() :
    """ Main function to be executed """
    args = parse_arguments()
    group = args.group
    submit = args.submit

    # Fetch the prepids:
    regexp = regexps[group]
    prepids = [r["prepid"] for r in mcm.get("requests", query="pwg=GEN&member_of_campaign=Run3Summer22wm*&dataset_name={}*&status=done".format(regexp))] 

    print(" >> Going to clone %d prepids"%len(prepids)) 
    for prepid in prepids:
        clone_prepid(prepids, submit)

if __name__ == "__main__" :

    main()
