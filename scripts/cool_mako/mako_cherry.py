import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os
import time
from library import makeSession, SUBJS, load_json, save_json, createSubDir
from json_template import json

lookup = TemplateLookup(directories=['.','../cherrypy'],filesystem_checks=True,encoding_errors='replace')

class MakoRoot:
    def __init__(self):
        self.history = "<ul><li>logged in</li></ul>"
        self.json = json
        self.TabID = 99
        self.jsonpath = ""

    def index(self):
        lijson = {"time":time.ctime(),
                  "loginbox":[{"name":"subject","prompt":"Subject:"},
                              {"name":"visit","prompt":"Visit #:"} ] }
        try:
            loginTmpl = lookup.get_template("login.html")
            return loginTmpl.render(**lijson)
        except:
            return exceptions.html_error_template().render()
    index.exposed = True

    def doMakoLogin(self,subject=None,visit=None):
        self.jsonpath = os.path.join(SUBJS,subject,"%s_experiment_info.json"%subject)
        if os.path.exists(self.jsonpath):
            self.json = load_json(self.jsonpath)
        else:
            self.json = json
            self.json['subject_id'] = subject 
        ### if no sessiondir exists, create it 
        if not os.path.exists(os.path.join(SUBJS,subject)):
            self.history = createSubDir(subject) + self.history
        if not os.path.exists(os.path.join(SUBJS,"%s/session%s/"%(subject,visit))):
            history = makeSession(subject,visit)   # returns history
            self.history = history + self.history
        self.setTab(visit)          # activates the tab
        return self.renderAndSave()   # saves the json, and renders the page
    doMakoLogin.exposed = True

    def renderAndSave(self):
        ## completion checks here
        self.completionChecks()   # activates the next relevant button
        save_json(self.jsonpath,self.json)
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(**self.json)
        except:
            return exceptions.html_error_template().render()
    renderAndSave.exposed=True

    def formHandler(self,button):
        if button[-1].isdigit():
            [action,program,target] = button.split(' ')
            self.run = int(target)
            self.buttonReuse(button)
        else:
            [action,program] = button.split(' ')

        if program == "Murfi":
            self.makoDoMurfi(action)
        elif program == "Serve":
            self.makoDoServe(action)
        elif program == "RT":
            pass
            # self.makoDoRT()
        elif program == "Run":  ## redo this run
            self.makoRedo()
        else:
            self.json['Protocol'][self.TabID]['Steps'][self.json[program]]['time'] = time.ctime()
#             if program == "Display":
# #                self.makoDisplayTest()
#             elif program == "Buttons":
# #                self.makoButtonsTest()
#             elif program == "Trigger":
# #                self.makoTriggerTest()
            
        return self.renderAndSave()
    formHandler.exposed=True
        
    def completionChecks(self):
        tab = self.TabID
        lastVisit = self.json["rtVisits"]+1   # only +1 because 0-indexed
        # -- tests should be done before any real runs/stimulus.
        # -- handle funcloc and rt runs differently.
        if (tab == 0) or (tab == lastVisit):  # funcloc
            checkList = ['Display','Buttons','Trigger','BirdSounds','LetterSounds']   ## need to add scans / get programatically?
            funcList = ['1-back-localizer','1-back-transfer','2-back-transfer']  ## autoget?
            totFunc = len(funcList)
            funcRoot = ""
        elif (tab > 0) and (tab < lastVisit): # rt visit
            checkList = ['Display','Buttons','Trigger']   ## eventually need to add scan Runs // get programatically?
            totFunc = self.json["runsPerRtVisit"]
            funcList = range(1,(totFunc+1))
            funcRoot = "Murfi "
            
        emptyStamps = [len(self.getTimeStamp(test)) for test in checkList].count(0)
        if emptyStamps == 0:
            scansLeft = [len(self.getTimeStamp(scan)) for scan in funcList].count(0)
            if scansLeft == 0:
                ## visit complete!
                pass
            else:
                nextScan = funcRoot + str(funcList[-scansLeft])
                self.setButtonState('null %s'%nextScan,'enabled')
        return

    def getTimeStamp(self,prog):
        if isinstance(prog,int):  ## RT run, add runNum to json lookup for rt runs 
            index = self.json['rtLookup'] + (prog - 1)
        elif isinstance(prog,str):  ## not an RT run, get program's json lookup
            index = self.json[prog]
        return self.json['Protocol'][self.TabID]['Steps'][index]['time']

    def makoDoMurfi(self,action):
        run = self.run
        if (action == "End"):
            ## call endMurfi
            ## attach RT run timestamp to End Murfi
            runIndex = self.json['rtLookup'] + (run - 1)  # run is 1-indexed, so subtract 1            
            self.json['Protocol'][self.TabID]['Steps'][runIndex]['time'] = time.ctime()
            self.setButtonState("null Murfi %d"%run,"disabled")
            self.setButtonState("null Serve %d"%run,"disabled")
            self.setButtonState("null RT %d"%run,"disabled")
            self.setButtonState("Redo Run %d"%run,"enabled")
            if (run < self.json["runsPerRtVisit"]):
                self.setButtonState("null Murfi %d"%(run+1),"enabled")
        else:
            ## call doMurfi here
            self.setButtonState("null Serve %d"%run,"enabled")
            self.setButtonState("null RT %d"%run,"enabled")
        return

    def makoDoServe(self,action):
        run = self.run
        if (action == "End"):
            ## call endServe
            self.setButtonState("null Murfi %d"%run,"enabled")
        else:
            ## call doServe
            self.setButtonState("null Murfi %d"%run,"disabled")
            return

    def makoRedo(self):
        self.setButtonState("Restart Murfi %d"%self.run,"enabled")
        self.setButtonState("Redo Run %d"%self.run,"disabled")
        return
    
    def setTab(self,tab):
        self.TabID = int(tab)
        if self.TabID > len(self.json['Protocol']):  ## visit must be defined in Protocol
            self.TabID = 0
        for (i,v) in enumerate(self.json['Protocol']):
            if i==self.TabID:
                v['active'] = True
            else:
                v['active'] = False
        if (self.TabID > 0) and (self.TabID < 5):
            print "\nTabID is %d\n"%self.TabID
        return self.renderAndSave()
    setTab.exposed=True

    def buttonReuse(self,button):
        ## When a button has been pressed, (say to start something),
        ## rename it to the opposite function (say, to end the thing)
        [act,prog,runNum] = button.split(' ')
        if (act == "Start") or (act == "Restart"):
            newText = "End %s"%prog
        elif act == "End":
            newText = "Restart %s"%prog   
        else:    ## not startable/endable
            return
        runIndex = self.json['rtLookup'] + (int(runNum) - 1)  # runNum is 1-indexed, so subtract 1
        self.json['Protocol'][self.TabID]['Steps'][runIndex]['Steps'][self.json[prog]]["text"] = newText
        return

    def setButtonState(self,button,state):
        ## goal: changes the value of a button's disabled value in the json.
        ## allows the use of "disabled" or "enabled", rather than T/F
        [act,prog,run] = button.split(' ')
        if state == "disabled":
            stateBool = True
        elif state == "enabled":
            stateBool = False
        runIndex = self.json['rtLookup'] + (int(run) - 1)  # run is 1-indexed, so subtract 1
        self.json['Protocol'][self.TabID]['Steps'][runIndex]['Steps'][self.json[prog]]['disabled'] = stateBool            
        return

if __name__ == "__main__":
    if (os.getlogin() == 'ss'):    ### sasen will use different port
        cherrypy.config.update({'server.socket_host': '18.93.5.27',
                                'server.socket_port': 8090
                                })
    config = {'/': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.getcwd()},
              '/css': {'tools.staticdir.on': True,
                       'tools.staticdir.dir': os.path.abspath('css/')},
              '/js': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('js/')},
              '/img': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('img/')}
              }
    cherrypy.tree.mount(MakoRoot(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
