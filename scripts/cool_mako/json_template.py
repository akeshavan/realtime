# define a base json template
# for a new subject, start w/ localizer as active tab
# fill in full protocol
from library import save_json
import time
from copy import deepcopy
json = {"subject_id":"",
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer",
                     "Steps":[{"name":"Test Sounds","ui":"button","value":"TestSound","disabled":False},
                              {"name":"Test Display","ui":"button","value":"TestDisplay","disabled":False},
                              {"name":"Run localizer32", "ui":"checkbox","disabled":True},
                              {"name":"Run AAScout", "ui":"checkbox","disabled":True},
                              {"name":"Run MEMPRAGE", "ui":"checkbox","disabled":True},
                              {"name":"Run diffusion fieldmap", "ui":"checkbox","disabled":True},
                              {"name":"Run diffusion scan", "ui":"checkbox","disabled":True},
                              {"name":"Run resting state fieldmap", "ui":"checkbox","disabled":True},
                              {"name":"Run resting state", "ui":"checkbox","disabled":True},
                              {"name":"Start 1-back localizer","ui":"button","value":"1backlocalizer","disabled":True},
                              {"name":"Start 1-back transfer","ui":"button","value":"1backtransfer","disabled":True},
                              {"name":"Start 2-back transfer", "ui":"button","value":"2backtransfer","disabled":True}],
                     "active":True, 
                     "complete":False},
                    {"name":"Visit 1",
                     "Steps":[{"name":"Test Display","ui":"button","value":"TestDisplay","disabled":False},
                              {"name":"Run localizer32", "ui":"checkbox","disabled":True},
                              {"name":"Run AAScout", "ui":"checkbox","disabled":True},
                              {"name":"RT Session", "ui":"loop", "numLoops":6,
                               "Steps":[{"name":"Start Murfi","ui":"button","value":"Start Murfi","disabled":True},
                                        {"name":"Start Serve","ui":"button","value":"Start Serve","disabled":True},
                                        {"name":"RT Stimulus","ui":"button","value":"RT Stimulus","disabled":True},
                                        {"name":"End Serve","ui":"button","value":"End Serve","disabled":True},
                                        {"name":"End Murfi","ui":"button","value":"End Murfi","disabled":True}]}], 
                     "active":False, 
                     "activeRunNum":0,
                     "complete":False}]}
 

for i in range(2,5):
    json["Protocol"].append(deepcopy(json["Protocol"][1]))
    json["Protocol"][-1]["name"] = "Visit %d"%i

json["Protocol"].append(deepcopy(json["Protocol"][0]))
json["Protocol"][-1]["name"] = "Final Localizer"
json["Protocol"][-1]["active"] = False
