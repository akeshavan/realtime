import numpy as np
import sys, os, copy

usageMessage = """Usage: python examineRun.py FILENAME [keylist]
  or in ipython: run examineRun.py FILENAME keylist
  where FILENAME = SUBJECTID_YYYY_MON_DD_run_00N.npz
  and keylist traces into the file structure.
  Empty keylist prints the top-level keys."""

### handle arguments. 1st check for filename
numArgs = len(sys.argv)
if numArgs < 2:
    print "Error: Please supply a filename!"
    print usageMessage
    sys.exit(0)

filename = sys.argv[1]
if not os.path.exists(filename):
    print "Error: %s does not exist."%filename
    print usageMessage
    sys.exit(0)

### load the run data file
npzdata=np.load(filename)
topKeys = npzdata.keys()

### collapse the numpy ndarrays
rundata = {}
for key in topKeys:
    rundata[key] = copy.copy(npzdata[key].tolist())

### examine data!
### -- depends on number of keys provided
### -- check key validity along the way

if numArgs == 2:
    print "Top level keys are:"
    print topKeys
elif numArgs >= 3:
    keylist = sys.argv[2:]

    ## iterate through keylist, navigating the data structure
    node = rundata   ## keeps track of current node
    nodeString = "TOP"  ## keeps track of location
    for lvl in keylist:    ## lvl is the key for this node/level
        try:
            below = node[lvl]   ## if "lvl" is valid, then "below" is under "node"
            nodeString += ".%s"%lvl
            node = below   ## recurse down a level
            # if isinstance(below,dict):
            #     node = below
        except:
            print "Error: \"%s\" isn't a valid key here. Try one of these."%lvl
            print node.keys()

    print below
    print "----Printed %s."%nodeString
    if isinstance(below,dict):
        print "Next level's keys are:"
        print below.keys()


    # topLvl = keylist[0]    
    # try:
    #     print rundata[topLvl]
    #     if not topLvl == "xml":
    #         print "Next level's keys are:"
    #         print rundata[topLvl].keys()
    # except:
    #     print "Error: \"%s\" isn't a valid key here. Try one of these."%topLvl
    #     print topKeys

try:
    print "----Captured %s TRs.----"%rundata['tr']['active'][-1]
except:
    pass

npzdata.close()

# foo.keys()
# zipped_tt = zip(foo['tr'].tolist()['active'],foo['trials'].tolist()['active'])

# f.open('sasensave.py','wb')
# for pair in zipped_tt:
#     qq = str(pair)
#     f.write(qq)
# f.close()


