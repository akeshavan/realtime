# define a base json template
# for a new subject, start w/ localizer as active tab
# fill in full protocol
from library import save_json
import time
from copy import deepcopy
json = {"subject_id":"",
        "placebo":False,
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer Training",
                     "active":True, 
                     "complete":False,
                     "ui":"loop",
		             "Steps":[{"text":"1-back training",
	                          "ui":"button","class":"btn",
	                          "disabled":False,
	                          "time":"",
	                          "history":[],
	                          "action":"lib.localizer()",
                              "clicked":False,
                              "enabled_when":None,
	                          "value":"0.0",
                              "on_click":"disabled = False"}
                            ]
                            },
                    {"name":"Transfer Training",
                     "active":False, 
                     "complete":False,
                     "ui":"loop",
		             "Steps":[{"text":"1-back training",
	                          "ui":"button","class":"btn",
	                          "disabled":False,
	                          "time":"",
	                          "history":[],
	                          "action":"lib.transfer1()",
                                  "clicked":False,
                                  "enabled_when":None,
	                          "value":"1.0",
                                  "on_click":"disabled = False"},
                                     {"text":"2-back training",
	                          "ui":"button","class":"btn",
	                          "disabled":False,
	                          "time":"",
	                          "history":[],
	                          "action":"lib.transfer2()",
                              "clicked":False,
                              "enabled_when":None,
	                          "value":"1.1",
                              "on_click":"disabled = False"}
                            ]
                            },  
                    {"name":"Realtime Training","ui":"loop",
                     "Steps":[{"text":"Realtime(Active)",
                                "ui":"button","class":"btn",
                                "disabled":False,
                                "time":"",
                                "history":[],"clicked":False,
                                "value":"2.0","on_click":"disabled = False",
                                "action":"lib.rtActive()","enabled_when":None},
                              {"text":"Realtime(Passive)",
                                "ui":"button","class":"btn",
                                "disabled":False,
                                "time":"",
                                "history":[],"clicked":False,
                                "value":"2.1","on_click":"disabled = False",
                                "action":"lib.rtPassive()","enabled_when":None}
                              ],
                     "stepIndex":{},
                     "active":False,
                     "complete":False}
                            ]} 

