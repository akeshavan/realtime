# json_template.py
# Defines a base template for the experiment info JSON used by mako

from copy import deepcopy

## Common info
STUDY_INFO = {"study":"mTBI_rt","subject_id":"","group": "","rtVisits":4,"runsPerRtVisit":6,"activeTab":0}
VISIT_INFO = {"name":"","complete":False,"comments":[]}

## Common steps
TEST_EQUIP = {"ui":"button","parts":[{"text":"Test Equipment","action":"psychopy","file":"ButtonTest.py"}]}
LOCALIZER32_and_AASCOUT = {"ui":"checkbox-group","parts":[{"text":"Acquire localizer32"},
                                                          {"text":"Acquire AAScout"}]} 
STRUCTURAL = {"ui":"checkbox","parts":[{"text":"Acquire MEMPRAGE"}]}
REALTIME = {"ui":"button-group","parts":[{"text":"Start Murfi","action":"murfi","run":1,"done":False},
                                         {"text":"Launch RT","action":"psychopy","file":"mTBI_rt.py"},
                                         {"text":"Start Serve","action":"servenii"},
                                         {"text":"Redo Run","action":"redo"}]}

## Assemble the visit types

PREPOST = {"visit_info": deepcopy(VISIT_INFO),
           "steps":[deepcopy(TEST_EQUIP),
                    deepcopy(LOCALIZER32_and_AASCOUT),
                    deepcopy(STRUCTURAL),
                    {"ui":"checkbox","parts":[{"text":"Acquire T2-flare"}]},
                    {"ui":"checkbox-group","parts":[{"text":"Acquire diffusion-fieldmap"},
                                                    {"text":"Acquire diffusion-scan"}]},
                    {"ui":"checkbox-group","parts":[{"text":"Acquire resting-state-fieldmap"},
                                                    {"text":"Acquire resting-state"}]},
                    {"ui":"button","parts":[{"text":"Launch 1-back-localizer","action":"psychopy","file":"localXfer/Bird_1back.py"}]},
                    {"ui":"button","parts":[{"text":"Launch 1-back-transfer","action":"psychopy","file":"localXfer/Letter_1back.py"}]},
                    {"ui":"button","parts":[{"text":"Launch 2-back-transfer","action":"psychopy","file":"localXfer/Letter_2back.py"}]}]}

# build realtime visit steps
RTSTEPS = [deepcopy(TEST_EQUIP),
           deepcopy(LOCALIZER32_and_AASCOUT),
           deepcopy(STRUCTURAL)]
for r in range(0,STUDY_INFO['runsPerRtVisit']):
    REALTIME['parts'][0]['run'] = r+1
    RTSTEPS.append(deepcopy(REALTIME))

RTVISIT = {"visit_info": deepcopy(VISIT_INFO),
           "steps": RTSTEPS}
           
## Almost ready to assemble.... build the visit order
VISIT_LIST = [deepcopy(RTVISIT) for v in range(0,STUDY_INFO['rtVisits'])]
VISIT_LIST.insert(0,deepcopy(PREPOST))
VISIT_LIST.append(deepcopy(PREPOST))


## Assemble the whole study!
info = {"study_info": deepcopy(STUDY_INFO),
        "protocol": VISIT_LIST}


##---------------------------------------------------
## Processing


## Additional fields to add to each part
shared_fields = {"id":"","disabled":False,"time":"TIME","history":[]}
checkb_fields = {"checked":False}

# Calculate id for each part & add extra fields
for v,visit in enumerate(info['protocol']):
    for s,step in enumerate(visit['steps']):
        for p,part in enumerate(step['parts']): 
            if "checkbox" in step["ui"]:
                part.update(checkb_fields)
            shared_fields['id'] = "%d.%d.%d"%(v,s,p)
            part.update(shared_fields)


## ---------------------------------------------------
## Useful paths
TAB = 'study_info:activeTab'
SUBJID = 'study_info:subject_id'
