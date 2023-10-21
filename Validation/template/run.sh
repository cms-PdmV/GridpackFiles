#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc10
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_12_4_14_patch3
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

mkdir -p Configuration/GenProduction/python/
wget https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/__prepid__/0 -O __prepid__.py --no-check-certificate
mv __prepid__.py Configuration/GenProduction/python/

scram b

# run only GEN for better filter efficiency estimate
cmsDriver.py Configuration/GenProduction/python/__prepid__.py --python_filename run_gen.py --eventcontent RAW,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:output.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --step LHE,GEN --geometry DB:Extended --era Run3 --no_exec --mc -n __nevents_gen__

cmsRun run_gen.py &> __prepid__.run_gen.log

# run the proper GEN-SIM condition for time/event estimate
cmsDriver.py Configuration/GenProduction/python/__prepid__.py --python_filename run_gensim.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:output.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc -n __nevents_gensim__

cmsRun run_gensim.py &> __prepid__.run_gensim.log

mv __prepid__.run_*.log ../../

