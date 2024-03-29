# Local validation scripts

## Submitting jobs locally

``./submit_jobs.py -D <DIRNAME> -i <PREPIDSTART>-<PREPIDEND>,<PREPID>,<PREPID> -n <NEVENTS>``

``#./submit_jobs.py -D QCDB -i 210-217,220,224-228,250 -n 1000``

`PREPID_HEADER` is defined in the python script which is set to "GEN-Run3Summer22wmLHEGS" by default.
This will collect the corresponding `PREPID` generator fragment files from McM and submit jobs from the `DIRNAME` directory, running `NEVENTS` to validate the samples locally.

## Parsing the job logs

``./parse_jobs.py <DIRNAME> # --maxnevents MAXNEVENTS --minnevents MINNEVENTS --fixnevents FIXNEVENTS``

``# ./parse\_jobs.py QCDB --fixnevents 100000``

- `--maxnevents MAXNEVENTS` will set upper boundary for number of events.
- `--minnevents MINNEVENTS` will set lower boundary for number of events.
- `--fixnevents FIXNEVENTS` will set flat number of events.

If above arguments are not given, `NEVENTS` will be set to `(CROSS_SECTION) X 50000 [/pb] X 1./4.5 X (FUDGE_FACTOR)` by default. `FUDGE_FACTOR` is defined in the python script which set to "20" by default. But if `FIXNEVENTS` is given "50000", no matter what the `CROSS_SECTION` is, it will set `NEVENTS` to "50000". In case if `MINNEVENTS` is given "100000", if the `CROSS_SECTION` scaled `NEVENTS` is smaller than "100000", it will force set `NEVENTS` to "100000". Conversely if "MAXNEVENTS" is given "1000000", if the `CROSS_SECTION` scaled `NEVENTS` is larger than "1000000", it will force set `NEVENTS` to "1000000".

## Forging PREPIDs (and cloning PREPIDs)

To edit the prepids in McM with given validation results.

``./forge_prepids.py <PICKLEFILE> --edit``

``#./forge_prepids.py QCDB/prepids.pickle --edit``

To clone the prepids in McM to different campaigns.

``./forge_prepids.py <PICKLEFILE> --clone``

``#./forge_prepids.py QCDB/prepids.pickle --clone``

To do both altogether.

``./forge_prepids.py <PICKLEFILE> --edit --clone``

``#./forge_prepids.py QCDB/prepids.pickle --edit --clone``

This script will collect the parsed `PREPID` inputs and modify, clone requests for "Run3Summer22wmLHEGS" and "Run3Summer22EEwmLHEGS". `NEVENTS` will be multipled by "3.5" for "Run3Summer22EEwmLHEGS".

## Long term fixes to be done

- `parse_jobs.py` : NEVENTS should be computed with various campaigns and luminosities rather than the fixed value "50000 /pb".

# Directory making script

- Execute `makeDirs.py` with `python3 makeDirs.py doit` command from time to time (or whenever we need new directories in EOS area). Automatically parses all generator, process, and campaign directories and creates them in EOS area.
