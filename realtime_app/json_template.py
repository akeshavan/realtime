# json_template.py
# Defines a base template for the experiment info JSON used by mako

import os
import subprocess
from copy import deepcopy
from processLib import SUBJS, RTSCRIPTSDIR, get_node, RTDIR, XFERDIR

## Common info
STUDY_INFO = {"study":"mTBI_rt","subject_id":"","group": "","rtVisits":4,"runsPerRtVisit":6,"activeTab":0,"resume":None}
VISIT_INFO = {"name":"","type": "", "complete":False, "progress":"","comments":[],"time":"","history":[]}
HIFILE = os.path.join(RTDIR,"mTBI_rt.py")         # relative to RTDIR in processLib
LOFILE = os.path.join(RTDIR,"mTBI_rt.py") # relative to RTDIR in processLib

## Common steps
TEST_FUNCLOC = {"ui":"button","parts":[{"text":"Test Equipment","action":"psychopy","file":os.path.join(XFERDIR,"FullTest.py"), "prereqFor":"psychopy"}]}
TEST_REALTIME = {"ui":"button","parts":[{"text":"Test Equipment","action":"psychopy","file":os.path.join(RTDIR,"FullTest_rt.py"), "prereqFor":"psychopy.murfi.servenii"}]}
ALIGNMENT = {"ui":"checkbox-group","parts":[{"text":"Acquire localizerBC", "prereqFor":"all"},
                                            {"text":"Acquire localizer32", "prereqFor":"all"},
                                            {"text":"Acquire AAScout", "prereqFor":"all"}]} 
STRUCTURAL = {"ui":"checkbox","parts":[{"text":"Acquire MEMPRAGE"}]}
REST_STATE = {"ui":"checkbox-group","parts":[{"text":"Acquire resting-state-fieldmap"},
                                             {"text":"Acquire resting-state"}]}
REALTIME = {"ui":"button-group","parts":[{"text":"Start Murfi","action":"murfi","run":1,"done":False},
                                         {"text":"Launch RT","action":"psychopy","file":""},   # use HIFILE and LOFILE to set based on group
                                         {"text":"Start Serve","action":"servenii"}]}

## Assemble the visit types
VISIT_INFO["type"] = "prepost"
PREPOST = {"visit_info": deepcopy(VISIT_INFO),
           "steps":[deepcopy(ALIGNMENT),
                    deepcopy(STRUCTURAL),
                    {"ui":"checkbox","parts":[{"text":"Acquire T2-flare"}]},
                    {"ui":"checkbox-group","parts":[{"text":"Acquire diffusion-fieldmap"},
                                                    {"text":"Acquire diffusion-scan"}]},
                    deepcopy(REST_STATE),
                    deepcopy(TEST_FUNCLOC),
                    {"ui":"button","parts":[{"text":"Launch 1-back-localizer","action":"psychopy","file":os.path.join(XFERDIR,"Bird_1back.py")}]},
#                    {"ui":"button","parts":[{"text":"Launch 1-back-localizer_2","action":"psychopy","file":os.path.join("localXfer","Bird_1back_2.py")}]},
                    {"ui":"button","parts":[{"text":"Launch 1-back-transfer","action":"psychopy","file":os.path.join(XFERDIR,"Letter_1back.py")}]},
                    {"ui":"button","parts":[{"text":"Launch 2-back-transfer","action":"psychopy","file":os.path.join(XFERDIR,"Letter_2back.py")}]}]}

# build realtime visit steps
RTSTEPS = [deepcopy(ALIGNMENT),
           deepcopy(STRUCTURAL),
           deepcopy(REST_STATE),
           deepcopy(TEST_REALTIME)]
for r in range(0,STUDY_INFO['runsPerRtVisit']):
    REALTIME['parts'][0]['run'] = r+1
    RTSTEPS.append(deepcopy(REALTIME))

VISIT_INFO["type"] = "realtime"
RTVISIT = {"visit_info": deepcopy(VISIT_INFO),
           "steps": RTSTEPS}
           
## Almost ready to assemble.... build the visit order
VISIT_LIST = [deepcopy(RTVISIT) for v in range(0,STUDY_INFO['rtVisits'])]
VISIT_LIST.insert(0,deepcopy(PREPOST))
VISIT_LIST.append(deepcopy(PREPOST))


## Assemble the whole study!
info = {"study_info": deepcopy(STUDY_INFO),
        "protocol": VISIT_LIST,
        "flotscript" : ""}


##---------------------------------------------------
## Processing


## Additional fields to add to each part
shared_fields = {"id":"","disabled":False,"time":"","history":[]}
checkb_fields = {"checked":False, "action":""}

# Calculate id for each part & add extra fields
for v,visit in enumerate(info['protocol']):
    for s,step in enumerate(visit['steps']):
        for p,part in enumerate(step['parts']): 
            if "checkbox" in step["ui"]:
                part.update(checkb_fields)
            shared_fields['id'] = "%d.%d.%d"%(v,s,p)
            part.update(deepcopy(shared_fields))


## -------------------------------------------------
## methods that are specific to this study and this json structure

def checkSubjDir(subject):
    mySubjDir = os.path.abspath(os.path.join(SUBJS,subject))
    if not os.path.exists(mySubjDir):
        if not os.path.exists(SUBJS):
            print SUBJS,"doesn't exist!"
            raise OSError("Can't find subjects directory.")
        else:
            os.mkdir(mySubjDir)
    return mySubjDir

def checkVisitDir(subject,visit,group,myJson):
    print SUBJS
    print RTSCRIPTSDIR
    v = int(visit)
    maxV = len(VISIT_LIST)  ## off-by-one error???
    if v > maxV:   ##obo danger
        print "ERROR checkVisitDir: requested",v, "but the max visit number is", maxV
        raise Exception("Invalid visit number requested.")
    if v < 0:  ## supports visits[-1] indexing
        v = maxV + 1 + v
    myVisitDir = os.path.abspath(os.path.join(SUBJS,subject,'session%d'%v))
    print myVisitDir
    if not os.path.exists(myVisitDir):
        if not os.path.exists(checkSubjDir(subject)):
            raise OSError("Can't find directory for this subject.")
        else:
            os.mkdir(myVisitDir)
            vType = get_node(myJson, "%s:%d:%s"%(FULLSTUDY, v, VTYPE))
            if vType == 'realtime':
                if not os.path.exists(os.path.join(SUBJS, subject, 'mask')):
                    os.rmdir(myVisitDir)
                    v = v - 1
                    myVisitDir = os.path.abspath(os.path.join(SUBJS, subject, 'session%d' % v ))
                else:
                    os.mkdir(os.path.join(myVisitDir, 'data'))  ## psychopy data directory.
                    ### this is dumb. i should make it an importable library.
                    for vis in range(v,7):
                        print "Trying to create rt session for visit", vis
                        subprocess.Popen(["python", "createRtSession.py", subject, str(vis), 'none', group], cwd=RTSCRIPTSDIR)
    return myVisitDir, v
    


## ---------------------------------------------------
## Useful paths
FULLSTUDY = 'protocol'
SUBJID = 'study_info:subject_id'
GROUP = 'study_info:group'
TAB = 'study_info:activeTab'
RTRUNS = 'study_info:runsPerRtVisit'
VCOMPLETE = 'visit_info:complete'
VPROGRESS = 'visit_info:progress'
VTYPE = 'visit_info:type'
RESUME = 'study_info:resume'
