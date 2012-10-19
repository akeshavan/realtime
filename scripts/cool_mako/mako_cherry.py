import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os, sys
import time
import socket
import processLib as lib
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
        self.mySubjectDir = j.checkSubjDir(subject)
        self.jsonpath = os.path.join(self.mySubjectDir, "%s_experiment_info.json"%subject)
        if os.path.exists(self.jsonpath):
            self.json = lib.load_json(self.jsonpath)  
        else:
            lib.set_node(self.json,subject,j.SUBJID) ## get a fresh json_template
        visit = lib.get_node(self.json,j.TAB)
        self.visitDir = j.checkVisitDir(subject,visit) ### create & populate session dir        
        self.setTab(visit)          # activates the tab
        return self.renderAndSave()   # saves the json, and renders the page
    doMakoLogin.exposed = True

    def renderAndSave(self):
        self.completionChecks()   # activates the next relevant button
        lib.save_json(self.jsonpath,self.json)
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(cache_enabled=False, **self.json)
        except:
            return exceptions.html_error_template().render()
    renderAndSave.exposed=True

    def setTab(self,tab=0):
        self.TabID = int(tab)
        self.visitDir = os.path.join(self.mySubjectDir, "session%d"%self.TabID)
        lib.set_node(self.json,self.TabID,j.TAB)
        return self.renderAndSave()
    setTab.exposed=True

    def formHandler(self,button):
        print "received",button
        button_value = str(button).split(' ')
        btn_id = button_value[0]
        bNode = bt.btn_node(btn_id, self.json)
        bt.timeStamp(bNode)
        self.updateProgress(btn_id)
        
        if bNode.has_key('action'):
            bAction = str(bNode['action'])   # ensure it's a string, not unicode
            if bAction == 'murfi':
                self.run = bNode['run']
                self.makoMurfiHandler(button_value, bNode)
            elif bAction == 'psychopy':
                self.makoDoStim(button_value, bNode)
            elif bAction == 'servenii':
                self.makoDoServ(button_value, bNode)
            elif bAction == 'redo':
                pass
            elif bAction == "":    # Checkboxes have empty action fields
                self.makoCheckboxHandler(bNode)                
            else: 
                print 'mako_cherry: Unrecognized action from button: %s'%bAction
                sys.exit("mako_cherry.py did not recognize button's action keyword.")                
        else: 
            ## All buttons (including checkboxes) should have an action field. Something's wrong.
            print "mako_cherry: The button/checkbox you clicked is missing its action keyword."
            print "Check the json:",self.jsonpath
            print "You clicked on",button
        return self.renderAndSave()
    formHandler.exposed=True

    ###########----------------------------------------
    ## sub-handlers for formHandler go below this point
    ###########----------------------------------------

    def updateProgress(self,bid):
        bt.setProgress(bid, bt.get_visit(bid,self.json))
        return


    def makoMurfiHandler(self, btn_value, node):
        ## Handle "Start" & "End" differently
        if ('Start' in btn_value):
            murfLog = bt.nameLogfile(node, self.subject)
            try:
                self.murfProc, self.murfOUT, h = lib.doMurfi(self.subject, self.TabID, self.run, murfLog)
            except:
                self.murfProc.kill()
                self.murfOUT.close()
                raise
            lib.set_here(node,'text','End Murfi')  ## could do this better
            lib.writeFlots(self.subject, self.TabID, node['run'])  ## update jquery for murfi plots
            print "attempting to change flotmurfi.js to use " + str(node['run']) +"!\n\n"
            ## NOTDONE enable serve + psychopy buttons 
        elif "End" in btn_value:
            if hasattr(self, 'murfProc'):
                lib.endMurfi(self.murfProc, self.subject, self.TabID, self.run, self.murfOUT)
            lib.set_here(node,'text','Start Murfi')
            ## NOTDONE check if 159 TRs collected here?
            activeFile = os.path.join(self.visitDir,'data','run00%d_active.json'%self.run)
            if os.path.exists(activeFile):
                activeData = lib.load_json(activeFile)
                if len(activeData['data']) > 150:
                    node['done'] = True
                else:
                    lib.set_here(bt.sib_node(node['id'], self.json, 3), "disabled", False)
                
            ## maybe enable redo? disable this run, enable next run,
        else:
            print "mako_cherry: Can't handle this murfi button value:",btn_value
        return

    def makoDoStim(self,btn_value,node):
        if ('RT' in btn_value):
            return self.makoRealtimeStim(btn_value,node)
        else:
            psyFile = os.path.join(lib.RTDIR,node['file'])
            psyArgs = [self.subject, self.TabID]
            log = os.path.join(self.visitDir, "%s.log"%btn_value[-1])
            print psyFile, psyArgs, log
            self.stimProc, h = lib.startPsycho(psyFile, psyArgs, log)
            return

    def makoRealtimeStim(self,btn_value,node):
        if ('Launch' in btn_value):
            murfNode = bt.sib_node(node['id'], self.json, 0)
            stimLog = bt.nameLogfile(node, self.subject, murfNode)
            self.run = murfNode['run']   ## in case of accidental logout
            self.stimProc, h = lib.doStim(self.subject, self.TabID, self.run, stimLog)
            lib.set_here(node,'text','End RT')  ## could do this better
        elif ('End' in btn_value):
            if hasattr(self, 'stimProc'):
                self.stimProc.kill()
            lib.set_here(node,'text','Launch RT')
        else:
            print "mako_cherry: Can't handle this stimulus button value:",btn_value
        return

    def makoDoServ(self,btn_value,node):
        ## Handle "Start" & "End" differently
        if ('Start' in btn_value):
            murfNode = bt.sib_node(node['id'], self.json, 0)
            servLog = bt.nameLogfile(node, self.subject, murfNode)
            self.run = murfNode['run']  # in case of accidental logout
            self.servProc, self.servOUT, h = lib.doServ(self.subject, self.TabID, self.run, servLog)
            lib.set_here(node,'text','End Serve')  ## could do this better
        elif "End" in btn_value:
            if hasattr(self, 'servProc'):
                lib.endServ(self.servProc, self.subject, self.TabID, self.run, self.servOUT)
            lib.set_here(node,'text','Start Serv')
        else:
            print "mako_cherry: Can't handle this servenii button value:",btn_value
        return


    def makoCheckboxHandler(self,node):
        # checkboxes should be enabled one at a time.
        node['checked'] = not node['checked']  # toggle state
        return


    def subjectMoved(reason):
        print self.tab, reason
        infoNode = lib.get_node(self.json, ['Protocol',self.tab,'visit_info'])
        bt.timeStamp(infoNode)
        infoNode['comments'].append(reason)
        return self.renderAndSave()
    subjectMoved.exposed = True
        
    def completionChecks(self):
        tab = self.TabID
        progress = bt.getProgress(lib.get_node(self.json, [j.FULLSTUDY,tab]))
        if progress == "":    ## activate first step, deactivate all else
            ## TODO: (look for completion of prev step)            
            bt.enable1st(tab,self.json)
        else:
            bt.enableNext(progress,self.json)
        print "progress:", progress
        return
    completionChecks.exposed=True
        
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
    if len(sys.argv) == 3:
        cherrypy.config.update({'server.socket_host': str(sys.argv[1]),
                                'server.socket_port': int(sys.argv[2])
                                })        
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('mit.edu', 0))
    # myHost = s.getsockname()[0]
    # cherrypy.config.update({'server.socket_host': myHost,
    #                         'server.socket_port': 8080
    #                         })

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
                      'tools.staticdir.dir':os.path.abspath(lib.SUBJS)},
              }
    cherrypy.tree.mount(MakoRoot(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
