import cherrypy
from mako.lookup import TemplateLookup
from mako import exceptions
import json
import os, sys
import time
from copy import deepcopy
import processLib as lib
import json_template as j
import buttonlib as bt

lookup = TemplateLookup(directories=['templates'], 
                        filesystem_checks=True, encoding_errors='replace',
                        strict_undefined=True)

class AppRoot(object):
    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        self.mySubjectDir = None
        self.visitDir = None
        self.history = "<ul><li>logged in</li></ul>"
        self.json = deepcopy(j.info)
        self.subject = None
        self.TabID = 99
        self.run = 99
        self.jsonpath = ""

    @cherrypy.expose
    def index(self,_=None):
        if not self.subject:
            raise cherrypy.HTTPRedirect('/login')
        return self.processLogin()

    @cherrypy.expose
    def login(self, subject=None):
        print subject, '-', self.subject, '-'
        if self.subject:
            raise cherrypy.HTTPRedirect('/')
        if subject:
            self.subject = subject
            raise cherrypy.HTTPRedirect('/')
        login_data = {"time": time.ctime()}
        try:
            loginTmpl = lookup.get_template("login.html")
            return loginTmpl.render(**login_data)
        except:
            return exceptions.html_error_template().render()

    def processLogin(self):
        subject = self.subject
        print 'SUBJECT['+ subject+']'
        self.mySubjectDir = j.checkSubjDir(subject)
        j.dirStructure(subject)  # verify/create subject's directory structure (visits, etc.)
        self.jsonpath = os.path.join(self.mySubjectDir,
                                     "%s_experiment_info.json" % subject)
        if os.path.exists(self.jsonpath):
            self.json = lib.load_json(self.jsonpath)
            self.json['flotscript'] = ''
            if 'flotscript_header' in self.json:
                del self.json['flotscript_header']
        else:
            lib.set_node(self.json, subject, j.SUBJID) ## get a fresh json_template
        ##   check complete key of visit+1 (until we find one that's incomplete)
        ##   then set activeTab to that visit number.
        v = 0
        self.setTab(v)
        while lib.get_node(self.json, self.vNodePath + j.VCOMPLETE):
            v += 1
            self.setTab(v)
        visit = v
        # handle subject's group assignment and create visit/session dir based on group, if needed.
        group = lib.get_node(self.json, j.GROUP)
        if not group == "":
            ### create & populate session dir
            self.visitDir, correctVisit = j.checkVisitDir(subject, visit, group, self.json)
            if not correctVisit == visit:
                self.subjectMoved("<b>Cannot move on to next visit without ROI masks!</b>", "false")
            self.setTab(correctVisit)
            return self.renderAndSave()   # saves the json, and renders the page
        else:
            return self.modalthing()  # render modal to assign group -> call setgroup() -> save json & render normally

    def modalthing(self):
        try:
            subregTmpl = lookup.get_template("group_modal.html")
            return subregTmpl.render(cache_enabled=False, **self.json)
        except:
            return exceptions.html_error_template().render()

    @cherrypy.expose
    def LogOut(self):
        print "LOGGING OUT!!!!"
        self._reset_state()
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def setgroup(self, group=None):
        ## Responds to result of modalthing's form submission. 
        ## Uses group value to create session dir.
        ## Note: group might not be assigned if "Cancel" is pressed
        if group:
            lib.set_node(self.json, group, j.GROUP)
            self.visitDir, rightVisit = j.checkVisitDir(self.subject, self.TabID, group,
                                            self.json) ### create & populate session dir
            self.setTab(rightVisit)
        return self.renderAndSave()

    def renderAndSave(self):
        self.completionChecks()   # activates the next relevant button
        self.flotJavascript()
        lib.save_json(self.jsonpath, self.json)
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(cache_enabled=False, **self.json)
        except:
            return exceptions.html_error_template().render()

    @cherrypy.expose
    def setTab(self, tab=0):
        ## NB: Clicking on a tab in the web-interface updates the json properly, but
        ##     the mako template (subreg.html) is not re-rendered, so "what you get" is NOT
        ##     "what you see". You must either cause the form to be submitted (click a button)
        ##     or logout and login again for the website to catch up to the json's reality.
        self.TabID = int(tab)
        self.visitDir = os.path.join(self.mySubjectDir,
                                     "session%d" % self.TabID)
        self.vNodePath = j.FULLSTUDY + ":%d:" % self.TabID
        lib.set_node(self.json, self.TabID, j.TAB)
        #return self.renderAndSave()

    @cherrypy.expose
    def getFlotInfo(self, button,_):
        print "received", button
        button_value = str(button).split(' ')
        btn_id = button_value[0]
        bNode = bt.btn_node(btn_id, self.json)
        print bNode
        if bNode.has_key('action'):
            bAction = str(bNode['action'])   # ensure it's a string, not unicode
            print "!!!!!!!!!!!!!!!!! ",bAction
            if bAction == 'psychopy':
                visit = self.TabID
                run = self.run#bNode['run']
                active_url = 'subjects/%s/session%s/data/run%03d_active.json' %\
                             (self.subject, visit, run)
                reference_url = 'subjects/%s/session%s/data/run%03d_reference.json' %\
                                (self.subject, visit, run)
                placeholder = '#rtmodal'#'#rtgraph%d_%d' % (visit, run)
                return json.dumps({'active_url': active_url,
                                   'reference_url': reference_url,
                                   'placeholder': placeholder})

    @cherrypy.expose
    def formHandler(self, button,_=None):
        print "LOOK HERE: received", button
        button_value = str(button).split(' ')
        btn_id = button_value[0]
        bNode = bt.btn_node(btn_id, self.json)
        bt.timeStamp(bNode)
        if bNode.has_key('action'):
            bAction = str(bNode['action'])   # ensure it's a string, not unicode
            if bAction == 'murfi':
                self.run = bNode['run']
                self.makoMurfiHandler(button_value, bNode)
            elif bAction == 'psychopy':
                self.makoDoStim(button_value, bNode)
            elif bAction == 'servenii':
                self.makoDoServ(button_value, bNode)
            elif bAction == "":    # Checkboxes have empty action fields
                self.makoCheckboxHandler(bNode)                
            else: 
                print 'mako_cherry: Unrecognized action from button: %s'%bAction
                sys.exit("realtime_app.py did not recognize button's action keyword.")
        else: 
            ## All buttons (including checkboxes) should have an action field. Something's wrong.
            print "mako_cherry: The button/checkbox you clicked is missing its action keyword."
            print "Check the json:",self.jsonpath
            print "You clicked on",button
        return self.renderAndSave()

    ###########----------------------------------------
    ## sub-handlers for formHandler go below this point
    ###########----------------------------------------

    def updateProgress(self,bid):
        """
        Only call this once an action (or structural scan) is done.
        """
        # do nothing if progress > bid (because we're redoing something)
        curProg= lib.get_node(self.json, self.vNodePath + j.VPROGRESS)
        if curProg == "":    # beginning of a visit, or we're in redo mode.
            bt.setProgress(bid, bt.get_visit(bid,self.json))
        elif bt.compareBids(curProg, bid):   # step
            print "new progress will be",bid
            bt.setProgress(bid, bt.get_visit(bid,self.json))
        else:
            print "completed", bid, ", but that's less than", curProg
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
            lib.set_here(bt.sib_node(node['id'], self.json, 1), "disabled", False)  ## activate psychopy
            lib.set_here(bt.sib_node(node['id'], self.json, 2), "disabled", False)  ## activate servenii
        elif "End" in btn_value:
            ## End must also clean up after servenii & rt psychopy, if needed.
            lib.set_here(bt.sib_node(node['id'], self.json, 1), "disabled", True)  ## disable psychopy
            lib.set_here(bt.sib_node(node['id'], self.json, 2), "disabled", True)  ## disable servenii
            ## close errant process handles
            if hasattr(self, 'murfProc'):
                lib.endMurfi(self.murfProc, self.subject, self.TabID, self.run, self.murfOUT)
            if hasattr(self, 'stimProc'):
                self.stimProc.kill()
            if hasattr(self, 'servProc'):
                lib.endServ(self.servProc, self.subject, self.TabID, self.run, self.servOUT)
            lib.set_here(node,'text','Start Murfi')
            ## check if RT run is done yet:
            ## -- 150ish TRs collected in results JSON? ==> done; update progress.
            ## -- otherwise, allow Murfi restart for this run.
            activeFile = os.path.join(self.visitDir,'data','run00%d_active.json'%self.run)
            if os.path.exists(activeFile):
                activeData = lib.load_json(activeFile)
                print "activeData's length is:", len(activeData['data'])
                if len(activeData['data']) > 150:
                    bt.rtDone(self.json, node['id'])  ## bt.updateProgress gets called in here.
                else:
                    lib.set_here(node, "disabled", False) ## ensure murfi can be restarted
        else:
            print "realtime_app: Can't handle this murfi button value:",btn_value
        return


    def makoDoStim(self,btn_value,node):
        print btn_value
        if ('RT' in btn_value):
            return self.makoRealtimeStim(btn_value,node)
        else:
            if ('Launch' in btn_value) or ('Test' in btn_value):
                psyFile = node['file']
                psyArgs = [self.subject, self.TabID, bt.getTimestamp(node)]
                log = os.path.join(self.visitDir, "%s.log"%btn_value[-1])
                print psyFile, psyArgs, log
                self.stimProc, h = lib.startPsycho(psyFile, psyArgs, log)
                if ('Launch' in btn_value):
                    lib.set_here(node, 'text', 'End '+ btn_value[-1])
                elif ('Test' in btn_value):
                    self.updateProgress(btn_value[0])
            elif ('End' in btn_value):
                ## decide whether to allow restart or to disable!
                if bt.checkPsychoDone(self.subject, node):
                    self.updateProgress(btn_value[0])
                    lib.set_here(node,'disabled',True)
                else:
                    lib.set_here(node, 'text', 'Launch '+ btn_value[-1])                    
        return


    def makoRealtimeStim(self, btn_value, node):
        murfNode = bt.sib_node(node['id'], self.json, 0)
        stimLog = bt.nameLogfile(node, self.subject, murfNode)
        self.run = murfNode['run']   ## in case of accidental logout
        self.flotJavascript()
        # based on group, use proper stimulus file
        group = lib.get_node(self.json, j.GROUP)
        if group == "high":
            psychofile = j.HIFILE
        elif group == "low":
            psychofile = j.LOFILE
        lib.set_here(node, 'file', psychofile)  # record which stimulus file was used
        # ready to launch!
        self.stimProc, h = lib.doStim(self.subject, self.TabID, self.run, stimLog, psychofile,self.json["study_info"]["group"])
        lib.set_here(node,'disabled', True)  # this button only launches. 'End Murfi' cleans up
        return


    def makoDoServ(self,btn_value,node):
        murfNode = bt.sib_node(node['id'], self.json, 0)
        servLog = bt.nameLogfile(node, self.subject, murfNode)
        self.run = murfNode['run']  # in case of accidental logout
        self.servProc, self.servOUT, h = lib.doServ(self.subject, self.TabID, self.run, servLog)
        lib.set_here(node,'disabled', True)
        return


    def makoCheckboxHandler(self,node):
        lib.set_here(node, 'checked', True)
        lib.set_here(node, 'disabled', True)
        self.updateProgress(node['id'])
        return


    @cherrypy.expose
    def subjectMoved(self, reason, moved="false"):
        print self.TabID, reason, moved
        ## timestamp and store comment
        infoNode = lib.get_node(self.json, ['protocol',self.TabID,'visit_info'])
        bt.timeStamp(infoNode)
        infoNode['comments'].append(reason)
        ## determine which steps need to be redone
        if moved == "true":
            ## QUESTION: should we be on an active visit only?
            ## enable & clear printed timestamp on localizers & test equipment
            bt.movementRedo(self.json, self.TabID)
            ## REMINDER: on functional runs, they should get to hit "end" (minor bug)
        elif moved == "false":
            pass  ## just adding the comment to visit_info
        else:
            raise Exception("Invalid value for 'moved' from radio button!")
        return self.renderAndSave()


    def completionChecks(self):
        tab = self.TabID
        vComplete = lib.get_node(self.json,self.vNodePath + j.VCOMPLETE)
        print "complete:", vComplete,
        if vComplete:
            return
        progress = lib.get_node(self.json, self.vNodePath + j.VPROGRESS)
        print "... progress:",progress, "tab:",tab
        if progress == "":    ## activate first step, deactivate all else
            if (tab == 0):
                [bt.enableOnly(self.json, t, None) for t in range(1,len(j.VISIT_LIST))]
                bt.enableOnly(self.json, tab, 'first')
            else:
                prevVNodePath = self.vNodePath[:-2] + str(tab-1) + ":"
                lastVComplete = lib.get_node(self.json, prevVNodePath + j.VCOMPLETE)
                if lastVComplete:
                    bt.enableOnly(self.json, tab, 'first')
                else:
                    bt.enableOnly(self.json, tab, None)
        else:
            activeVisit = bt.enableNext(progress,self.json)
            if not activeVisit == tab:
                bt.enableOnly(self.json, tab, None)
                bt.enableOnly(self.json, activeVisit, 'first')
        return


    def flotJavascript(self):
        self.json['flotscript'] = """
"""
        if self.json['saved_flotscript'] == "":        
            flotcalls = j.flotSetup(self.subject)
            self.json['saved_flotscript'] = '\n'.join(flotcalls)
        self.json['flotscript'] += self.json['saved_flotscript']
        # for visit in range(1, 6):
        #     for run in range(1, 7):
        #         active_url = 'subjects/%s/session%s/data/run%03d_active.json' % \
        #                      (self.subject, visit, run)
        #         reference_url = 'subjects/%s/session%s/data/run%03d_reference.json' %\
        #                      (self.subject, visit, run)
        #         placeholder = '$("#rtgraph%d_%d")' % (visit, run)
        #         flotcalls.append('flotplot("%s", "%s", %s);' % (active_url,
        #                                                           reference_url,
        #                                                           placeholder))
        # self.json['flotscript'] += '\n'.join(flotcalls)
        return


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
    cherrypy.config.update({'log.access_file':'realtime_app_access.log',
                            'log.error_file':'realtime_app_error.log'})
    config = {'/': {'tools.staticdir.on': True,
                   'tools.staticdir.dir': os.getcwd(),
                   'tools.sessions.on' : True,
                   'tools.sessions.storage_type' : "file",
                   'tools.sessions.storage_path': lib.SUBJS,
                   'tools.sessions.timeout' : 120},
              '/css': {'tools.staticdir.on': True,
                       'tools.staticdir.dir': os.path.abspath('css/')},
              '/js': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('js/')},
              '/img': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('img/')},
              '/flot': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('flot/')},
              '/subjects': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath(lib.SUBJS)}
              }
    cherrypy.tree.mount(AppRoot(), '/', config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
