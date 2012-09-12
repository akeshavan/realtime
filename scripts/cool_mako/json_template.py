# define a base json template
# for a new subject, start w/ localizer as active tab
# fill in full protocol
from library import save_json
import time
from copy import deepcopy
json = {"subject_id":"",
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer",
                     "Steps":[{"text":"Test Display","ui":"button","disabled":False,"time":"","history":[]},
                              {"text":"Test Buttons","ui":"button","disabled":False,"time":"","history":[]},                              
                              {"text":"Test Trigger","ui":"button","disabled":False,"time":"","history":[]},                              
                              {"text":"Test BirdSounds","ui":"button","disabled":False,"time":"","history":[]},                              
                              {"text":"Test LetterSounds","ui":"button","disabled":False,"time":"","history":[]},                              
                              {"text":"Acquire localizer32", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire AAScout", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire MEMPRAGE", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire diffusion-fieldmap", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire diffusion-scan", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire resting-state-fieldmap", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire resting-state", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Launch 1-back-localizer","ui":"button","disabled":True,"time":"","history":[]},
                              {"text":"Launch 1-back-transfer","ui":"button","disabled":True,"time":"","history":[]},
                              {"text":"Launch 2-back-transfer", "ui":"button","disabled":True,"time":"","history":[]},
                              {"text":"Complete Visit", "ui":"button","disabled":True,"time":"","history":[]}],
                     "active":True, 
                     "complete":False},
                    {"name":"Visit 1",
                     "Steps":[{"text":"Test Display","ui":"button","disabled":True,"time":"","history":[]},
                              {"text":"Test Buttons","ui":"button","disabled":True,"time":"","history":[]},                              
                              {"text":"Test Trigger","ui":"button","disabled":True,"time":"","history":[]},                              
                              {"text":"Acquire localizer32 ", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Acquire AAScout", "ui":"checkbox","disabled":False,"checked":False,"time":"","history":[]},
                              {"text":"Complete RTVisit","ui":"button","disabled":True,"time":"","history":[]},
                              {"text":"RT Run", "ui":"loop", "runNum":1,"time":"","history":[],
                               "Steps":[{"text":"Start Murfi","ui":"button","disabled":True},
                                        {"text":"Launch RT","ui":"button","disabled":True},
                                        {"text":"Start Serve","ui":"button","disabled":True},
                                        {"text":"Redo Run","ui":"button","disabled":True}] }],
                     "active":False, 
                     "complete":False}],
        "rtVisits":4,
        "runsPerRtVisit":6,
        "Display":0, # index of Test Display button in any visit
        "Buttons":1, # index of Test Button button in any visit
        "Trigger":2, # index of Test Trigger button in any visit
        "BirdSounds":3, # index of Test BirdSounds button in a funcloc visit
        "LetterSounds":4, # index of Test LetterSounds button in a funcloc visit
        "RTVisit":5, # index of Complete/Redo RTVisit in an RT Visit
        "rtLookup":6,# index of 1st RT Run Step in an RT Visit. change if more pre-RT steps are inserted
        "1-back-localizer":12,  # index of bird 1-back in a funcloc visit
        "1-back-transfer":13,  # index of letter 1-back in a funcloc visit
        "2-back-transfer":14,  # index of letter 2-back in a funcloc visit
        "Visit":-1,            # index of Complete/Redo Visit in a funcloc visit
        "Murfi":0,   # index of murfi button within RT Run Step
        "RT":1,      # index of RT Stimulus btn in RT Run
        "Serve":2,   # index of servenii button withtin RT Run Step
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
