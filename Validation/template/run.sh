#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc10
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_12_4_11_patch3
cd CMSSW_12_4_11_patch3/src
eval `scram runtime -sh`

mkdir -p Configuration/GenProduction/python/
wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/__prepid__/0 -O __prepid__.py --no-check-certificate
mv __prepid__.py Configuration/GenProduction/python/

scram b

# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/__prepid__.py --python_filename run.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:output.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n __nevents__

cmsRun run.py

