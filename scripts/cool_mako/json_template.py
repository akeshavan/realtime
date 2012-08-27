# define a base json template
# for a new subject, start w/ localizer as active tab
# fill in full protocol
from library import save_json
import time
from copy import deepcopy
json = {"subject_id":"",
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer",
                     "Steps":[{"text":"Test Sounds -","ui":"button","disabled":False},
                              {"text":"Test Display -","ui":"button","disabled":False},
                              {"text":"Run localizer32", "ui":"checkbox","disabled":True},
                              {"text":"Run AAScout", "ui":"checkbox","disabled":True},
                              {"text":"Run MEMPRAGE", "ui":"checkbox","disabled":True},
                              {"text":"Run diffusion fieldmap", "ui":"checkbox","disabled":True},
                              {"text":"Run diffusion scan", "ui":"checkbox","disabled":True},
                              {"text":"Run resting state fieldmap", "ui":"checkbox","disabled":True},
                              {"text":"Run resting state", "ui":"checkbox","disabled":True},
                              {"text":"Launch 1-back localizer","ui":"button","disabled":True},
                              {"text":"Launch 1-back transfer","ui":"button","disabled":True},
                              {"text":"Launch 2-back transfer", "ui":"button","disabled":True}],
                     "active":True, 
                     "complete":False},
                    {"name":"Visit 1",
                     "Steps":[{"text":"Test Display -","ui":"button","disabled":False},
                              {"text":"Run localizer32", "ui":"checkbox","disabled":True},
                              {"text":"Run AAScout", "ui":"checkbox","disabled":True},
                              {"text":"RT Run", "ui":"loop", "runNum":1,
                               "Steps":[{"text":"Start Murfi","ui":"button","disabled":True},
                                        {"text":"Start Serve","ui":"button","disabled":True},
                                        {"text":"Launch RT","ui":"button","disabled":True},
                                        {"text":"Redo Run","ui":"button","disabled":True}] }],
                     "active":False, 
                     "activeRunNum":0,
                     "complete":False}],
        "rtVisits":4,
        "runsPerRtVisit":6,
        "rtLookup":3,   # index of 1st RT Run Step in an RT Visit. change if more pre-RT steps are inserted
        "Murfi":0,   # index of murfi button within RT Run Step
        "Serve":1,   # index of servenii button withtin RT Run Step
        "RT":2,      # index of RT Stimulus btn in RT Run
        "Run":3}     # index of Redo Run btn in RT Run

for r in range(2,json["runsPerRtVisit"]+1):
    json["Protocol"][1]["Steps"].append(deepcopy(json["Protocol"][1]["Steps"][json["rtLookup"]]))
    json["Protocol"][1]["Steps"][-1]["runNum"] = r
    
for i in range(2,json["rtVisits"]+1):
    json["Protocol"].append(deepcopy(json["Protocol"][1]))
    json["Protocol"][-1]["name"] = "Visit %d"%i

json["Protocol"].append(deepcopy(json["Protocol"][0]))
json["Protocol"][-1]["name"] = "Final Localizer"
json["Protocol"][-1]["active"] = False
