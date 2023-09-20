# Miscelaneous
## Clone prepids from Run3Summer22 to Run3Summer23
You just have to use the  `clone_toRun3Summer23.py` as follows:
```
python3 clone_toRun3Summer23.py $GROUP 
```

Where $GROUP can be any of the entries in the `regexps` dictionary in the script. This will use the regular expression defined in that dictionary to fetch all the requests that match such expression. The reason for this method is to be safe on what we fetch (this way when GROUP=TT_powheg, we always fetch those that are TT*powheg* in McM, and we avoid user to mess up the regexp and cloning/modifying requests that are not supposed to be edited or cloned).

By default the script will only do the proper cloning when the option `--submit` is given.

### Example:
```
python3 clone_toRun3Summer23.py TT_powheg --submit
```
