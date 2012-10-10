import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os, sys
import time
import socket
import library as lib
#from library import makeSession, SUBJS, load_json, save_json, createSubDir, get_node, set_node
import json_template as j
import buttonlib as bt

lookup = TemplateLookup(directories=['.','../cherrypy'],filesystem_checks=True,encoding_errors='replace',strict_undefined=True)

class MakoRoot:
    def __init__(self):
        self.history = "<ul><li>logged in</li></ul>"
        self.json = j.info
        self.subject = ""
        self.TabID = 99
        self.run = 99
        self.jsonpath = ""

    def index(self):
        lijson = {"time":time.ctime(),
                  # "loginbox":[{"name":"subject","prompt":"Subject:"},
                  #             {"name":"visit","prompt":"Visit #:"} ] 
                  }
        try:
            loginTmpl = lookup.get_template("login.html")
            return loginTmpl.render(**lijson)
        except:
            return exceptions.html_error_template().render()
    index.exposed = True

    def doMakoLogin(self,subject=None,visit=None):
        self.subject = subject    ## keep this accessible to other methods
        self.jsonpath = os.path.join(lib.SUBJS,subject,"%s_experiment_info.json"%subject)
        if os.path.exists(self.jsonpath):
            self.json = lib.load_json(self.jsonpath)
        else:
            lib.set_node(self.json,subject,j.SUBJID)
        visit = lib.get_node(self.json,j.TAB)

        ### if no sessiondir exists, create it 
        if not os.path.exists(os.path.join(lib.SUBJS,subject)):
            self.history = lib.createSubDir(subject) + self.history
        if not os.path.exists(os.path.join(lib.SUBJS,"%s/session%s/"%(subject,visit))):
            history = lib.makeSession(subject,visit)   # returns history
            self.history = history + self.history
        self.setTab(visit)          # activates the tab
        return self.renderAndSave()   # saves the json, and renders the page
    doMakoLogin.exposed = True

    def renderAndSave(self):
#        self.completionChecks()   # activates the next relevant button
        lib.save_json(self.jsonpath,self.json)
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(**self.json)
        except:
            return exceptions.html_error_template().render()
    renderAndSave.exposed=True

    def setTab(self,tab=0):
        self.TabID = int(tab)
        lib.set_node(self.json,self.TabID,j.TAB)
        return self.renderAndSave()
    setTab.exposed=True

    def formHandler(self,button):
        print "received",button
        button_value = str(button).split(' ')
        btn_id = button_value[0]
        bNode = bt.btn_node(btn_id, self.json)
        bt.timeStamp(bNode)
        
        if bNode.has_key('action'):
            bAction = str(bNode['action'])   # argh unicode
            if bAction == 'murfi':
                self.run = bNode['run']
                self.makoMurfiHandler(button_value, bNode)
            elif bAction == 'psychopy':
                self.makoDoStim(button_value, bNode)
            elif bAction == 'servenii':
                self.makoDoServ(button_value, bNode)
            elif bAction == 'redo':
                pass
            else: 
                print 'mako_cherry: Unrecognized action from button: %s'%bAction
                sys.exit("mako_cherry.py did not recognize button's action keyword.")                
        else:    # It must be a checkbox if it has no action key.
            # self.makoCheckboxHandler(btn_id) # i shouldn't need to pass checked!
            pass
        return self.renderAndSave()
    formHandler.exposed=True

    ###########----------------------------------------
    ## sub-handlers for formHandler go below this point
    ###########----------------------------------------

    def makoMurfiHandler(self, btn_value, node):
        ## Handle "Start" & "End" differently
        if ('Start' in btn_value) or ("Restart" in btn_value):  ## why do we need restart anymore?
            murfLog = bt.nameLogfile(node, self.subject)
            try:
                self.murfProc, self.murfOUT, h = lib.doMurfi(self.subject, self.TabID, self.run, murfLog)
            except:
                self.murfProc.kill()
                self.murfOUT.close()
                raise
            lib.set_here(node,'text','End Murfi')  ## could do this better
            ## NOTDONE enable serve + psychopy buttons 
        elif "End" in btn_value:
            lib.endMurfi(self.murfProc, self.subject, self.TabID, self.run, self.murfOUT)
            lib.set_here(node,'text','Restart Murfi')
            ## NOTDONE check if 159 TRs collected here?
            ## maybe enable redo? disable this run, enable next run,
        else:
            print "mako_cherry: Can't handle this murfi button value:",btn_value
        return

    def makoDoStim(self,btn_value,node):
        if ('Launch' in btn_value):
            murfNode = bt.sib_node(node['id'], self.json, 0)
            stimLog = bt.nameLogfile(node, self.subject, murfNode)
            self.stimProc, h = lib.doStim(self.subject, self.TabID, self.run, stimLog)
            lib.set_here(node,'text','End RT')  ## could do this better
        elif ('End' in btn_value):
            self.stimProc.kill()
            lib.set_here(node,'text','Launch RT')
        else:
            print "mako_cherry: Can't handle this stimulus button value:",btn_value
        return

    def makoDoServ(self,btn_value,node):
        ## Handle "Start" & "End" differently
        if ('Start' in btn_value) or ("Restart" in btn_value):  ## why do we need restart anymore?
            murfNode = bt.sib_node(node['id'], self.json, 0)
            servLog = bt.nameLogfile(node, self.subject, murfNode)
            print "servLog:",servLog
            self.servProc, self.servOUT, h = lib.doServ(self.subject, self.TabID, self.run, servLog)
            # try:
            #     self.servProc, self.servOUT, h = lib.doServ(self.subject, self.TabID, self.run, servLog)
            # except:  ## NOTDONE write a safe-close method for this
            #     self.servProc.kill()
            #     self.servOUT.close()
            #     raise
            lib.set_here(node,'text','End Serve')  ## could do this better
        elif "End" in btn_value:
            lib.endServ(self.servProc, self.subject, self.TabID, self.run, self.servOUT)
            lib.set_here(node,'text','Restart Serv')
        else:
            print "mako_cherry: Can't handle this servenii button value:",btn_value
        return

    def makoDoNBack(self,program):
        self.setButtonState("Launch %s"%program,"disabled")
        return 


    def makoCheckboxHandler(self,action,program,checked,progIndex):
        # checkboxes should be enabled one at a time.
        # checkboxes should have timestamps collected
        self.timeStamp(progIndex)
        ## toggle its status from unchecked to checked, etc...
        self.json['Protocol'][self.TabID]['Steps'][progIndex]['checked'] = not self.json['Protocol'][self.TabID]['Steps'][progIndex]['checked']
        ## disable once checked, enable next step if it's a checkbox
        if self.json['Protocol'][self.TabID]['Steps'][progIndex]['checked']:
            self.json['Protocol'][self.TabID]['Steps'][progIndex]['disabled'] = True
            if self.json['Protocol'][self.TabID]['Steps'][progIndex+1]['text'][0:7] == action:
                self.json['Protocol'][self.TabID]['Steps'][progIndex+1]['disabled'] = False
        return
    makoCheckboxHandler.exposed = True


    def setSuiteState(self,suite,state):
        ## GOAL: in this tab, enable/disable all steps of a certain suite.
        ## -- suites: "Test", "Acquire","Launch","[Re]Start" (action keywords)
        ## -- -- except "RT Run" to access Redo Run buttons
        ## -- uses human readable states ("disabled", "enabled","reset")
        tab = self.TabID
        stepNames = [st['text'] for st in self.json['Protocol'][tab]['Steps']]  ## get all step names
        for n,name in enumerate(stepNames):
            args = name.split(' ')  # [action, program] or ['RT','Run', runNum]
            if args[0] == suite: # does the step action match the suite name?
                print "trying to %s %s"%(state, name),
                progIndex = get_node(self.json,["Protocol",tab,"stepIndex",name])
                newName = "%s %d"%(suite,progIndex)
                print newName
                self.setButtonState(newName,state)
                # if (suite == "Test") and (state == disable):                    
            elif name == suite:   ## RT Run
                self.setButtonState("Redo Run %d"%(n+1-self.json['rtLookup']),state)  ## inverse of runIndex computations elsewhere
        return
    setSuiteState.exposed = True
        
    def completionChecks(self):
        tab = self.TabID
        lastVisit = self.json["rtVisits"]+1   # only +1 because 0-indexed
        ##### Enable tab only if prev visit complete AND this visit incomplete 
        ### BUG: final localizer's tests are stuck enabled!
        if tab == 0:
            if not self.json["Protocol"][tab]['complete']:
                self.setSuiteState('Test','enabled')  ## activate initial tests
                self.setSuiteState('Acquire','enabled')
        elif tab > 0:            
            if self.json['Protocol'][tab-1]['complete'] and (not self.json['Protocol'][tab]['complete']): 
                ## BUG: unless we're in the middle of running something?
                self.setSuiteState('Test','enabled') ## activate tests on this tab
                self.setSuiteState('Acquire','enabled')
            else:
                self.setSuiteState('Test','disabled') ## deactivate tests on this tab?
                self.setSuiteState('Acquire','disabled')
        ##### Create lists of Tests and Functional Scans
        # -- Based on tab, we can handle funcloc and rt runs differently.
        # -- checkList: tests should be done before any anatomical / functional runs.
        # -- funcList: functional/task scans, in sequential order
        # -- funcRoot + visitType: strings to help us handle RT runs differently
        if (tab == 0) or (tab == lastVisit):  # funcloc
            checkList = ['Display','Buttons','Trigger','BirdSounds','LetterSounds']   ## need to add scans / get programatically?
            funcList = ['1-back-localizer','1-back-transfer','2-back-transfer']  ## autoget?
            funcRoot = ""
            visitType = ""
        elif (tab > 0) and (tab < lastVisit): # rt visit
            checkList = ['Display','Buttons','Trigger']   ## eventually need to add scan Runs // get programatically?
            funcList = range(1,(self.json["runsPerRtVisit"]+1))
            funcRoot = "Murfi "
            visitType = "RT"
        ####### Ensure all pre-tests in checkList are complete (have timestamps)
        # -- list comprehension to get length of timestamp
        # -- any 0-length timestamps are incomplete. using count(0) to find them.
        emptyStamps = [len(self.getTimeStamp(test)) for test in checkList].count(0)  
        if emptyStamps == 0:
            ####### Determine progress through functional scan list in funcList
            # -- now the count of 0-length timestamps tells us how many scans are left
            # -- use scansLeft as a negative index into funcList to get name of next scan
            # -- rt runs need "Murfi" added to the runNum to produce next scan name
            # -- enable button for next scan via the scan name we just produced
            scansLeft = [len(self.getTimeStamp(scan)) for scan in funcList].count(0)
            ## BUG: 0-length doesn't work after redos.... is that OK?
            if scansLeft == 0: ## visit complete!
                self.json['Protocol'][tab]['complete'] = True 
                self.setButtonState('Complete %sVisit'%visitType,'enabled')
                self.setSuiteState('Test','disabled')
            else:
                nextScan = funcRoot + str(funcList[-scansLeft])
                self.setButtonState('null %s'%nextScan,'enabled')
        return   ## end def completionChecks()
    completionChecks.exposed=True
    
    def makoRedoRun(self):  ## disable the redo button + next action, enable relevant actions
        self.setButtonState("Redo Run %d"%self.run,"disabled")
        ### BUG: actually, all other Redos and all other starts should be disabled
        if self.run < self.json['runsPerRtVisit']:
        ### BUG: couldn't get this to work in an RT visit
            self.setButtonState("null Murfi %d"%(self.run+1),"disabled")                
        self.setButtonState("Restart Murfi %d"%self.run,"enabled")
        return
    makoRedoRun.exposed = True

    def makoRedoVisit(self,prog):  ## disable the redo button + next action, enable relevant actions
        self.setButtonState("Redo %s"%prog,"disabled")
        self.buttonReuse("Redo %s -"%prog)
        self.json['Protocol'][self.TabID]['complete'] = False
        self.setSuiteState('Test','reset')  ## reactivate tests on this tab
        self.setSuiteState('Acquire','reset')  ## reactivate structurals on this tab
        ### BUG: fails to reactivate functional scans
        return
    makoRedoVisit.exposed = True
    

    def buttonReuse(self,button):
        ## When a button has been pressed, (say to start something),
        ## rename it to the opposite function (say, to end the thing)
        [act,prog,runNum] = button.split(' ')
        if (act == "Start") or (act == "Restart"):
            newText = "End %s"%prog
        elif act == "End":
            newText = "Restart %s"%prog  
        elif act == "Complete":
            self.json['Protocol'][self.TabID]['Steps'][self.json[prog]]['text'] = "Redo %s"%prog
            return
        elif act == "Redo":
            self.json['Protocol'][self.TabID]['Steps'][self.json[prog]]['text'] = "Complete %s"%prog
            return
        else:    ## not startable/endable
            return
        runIndex = self.json['rtLookup'] + (int(runNum) - 1)  # runNum is 1-indexed, so subtract 1
        self.json['Protocol'][self.TabID]['Steps'][runIndex]['Steps'][self.json[prog]]["text"] = newText
        return
    buttonReuse.exposed = True

    def setButtonState(self,button,state):
        ## goal: changes the value of a button's disabled value in the json.
        ## -- allows the use of "disabled" or "enabled", rather than T/F
        ## -- "reset" is a state that means "enabled", and clears the timestamp to allow Redo
        if state == "disabled":
            stateBool = True
        elif (state == "enabled") or (state == "reset"):
            stateBool = False
        btnArgs = button.split(' ')  # button could have 2 or 3 arguments
        if len(btnArgs) == 2: 
            [act,prog] = btnArgs
            try:
                progIndex = self.json[prog]
            except:
                progIndex = int(prog)
            if state == "reset":   ## only tests and funcloc scans can be reset
                self.clearTimeStamp(prog)
            self.json['Protocol'][self.TabID]['Steps'][progIndex]['disabled'] = stateBool
        elif len(btnArgs) == 3:
            [act,prog,run] = btnArgs
            runIndex = self.json['rtLookup'] + (int(run) - 1)  # run is 1-indexed, so subtract 1
            self.json['Protocol'][self.TabID]['Steps'][runIndex]['Steps'][self.json[prog]]['disabled'] = stateBool
        return
    setButtonState.exposed = True

if __name__ == "__main__":
    if (os.getlogin() == 'ss'):    ### sasen will use different port
        cherrypy.config.update({'server.socket_host': '18.93.5.27',
                                'server.socket_port': 8090
                                })
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('mit.edu', 0))
    myHost = s.getsockname()[0]
    cherrypy.config.update({'server.socket_host': myHost,
                            'server.socket_port': 8080
                            })

    config = {'/': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.getcwd()},
              '/css': {'tools.staticdir.on': True,
                       'tools.staticdir.dir': os.path.abspath('css/')},
              '/js': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('js/')},
              '/img': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('img/')},
              '/flot': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('../flot/')},
              '/subjects': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':lib.SUBJS},
              }
    cherrypy.tree.mount(MakoRoot(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
