# define a base json template
# for a new subject, start w/ localizer as active tab
# fill in full protocol
from library import save_json
import time
from copy import deepcopy
json = {"subject_id":"",
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer",
                     "Steps":[{"name":"Test Sounds","type":"button","value":"TestSound","disabled":False},
                              {"name":"Test Display","type":"button","value":"TestDisplay","disabled":False},
                              {"name":"Run localizer32", "type":"checkbox","disabled":True},
                              {"name":"Run AAScout", "type":"checkbox","disabled":True},
                              {"name":"Run MEMPRAGE", "type":"checkbox","disabled":True},
                              {"name":"Run diffusion fieldmap", "type":"checkbox","disabled":True},
                              {"name":"Run diffusion scan", "type":"checkbox","disabled":True},
                              {"name":"Run resting state fieldmap", "type":"checkbox","disabled":True},
                              {"name":"Run resting state", "type":"checkbox","disabled":True},
                              {"name":"Start 1-back localizer","type":"button","value":"1backlocalizer","disabled":True},
                              {"name":"Start 1-back transfer","type":"button","value":"1backtransfer","disabled":True},
                              {"name":"Start 2-back transfer", "type":"checkbox","disabled":True}],
                     "active":True, 
                     "complete":False},
                    {"name":"Visit 1",
                     "Steps":[{"name":"Test Display","type":"button","value":"TestDisplay","disabled":False},
                              {"name":"Run localizer32", "type":"checkbox","disabled":True},
                              {"name":"Run AAScout", "type":"checkbox","disabled":True},
                              {"name":"RT Session", "type":"loop",
                                                    "Steps":[{"name":"Start Murfi","type":"button","value":"Start Murfi","disabled":True},
                                                             {"name":"Start Serve","type":"button","value":"Start Serve","disabled":True},
                                                             {"name":"Start Stimulus","type":"button","value":"RT Stimulus","disabled":True},
                                                             {"name":"End Serve","type":"button","value":"End Serve","disabled":True},
                                                             {"name":"End Murfi","type":"button","value":"End Murfi","disabled":True}]}], 
                     "active":False, 
                     "activeRunNum":0,
                     "complete":False}]}
 

for i in range(2,5):
    json["Protocol"].append(deepcopy(json["Protocol"][1]))
    json["Protocol"][-1]["name"] = "Visit %d"%i

json["Protocol"].append(deepcopy(json["Protocol"][0]))
json["Protocol"][-1]["name"] = "Final Localizer"
json["Protocol"][-1]["active"] = False
