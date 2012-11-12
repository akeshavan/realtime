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
from copy import deepcopy

lookup = TemplateLookup(directories=['.','../cherrypy'],filesystem_checks=True,encoding_errors='replace',strict_undefined=True)

class MakoRoot:
    def __init__(self):
        self.history = "<ul><li>logged in</li></ul>"
        self.json = deepcopy(j.info)
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
        self.setTab(visit)          # activates the tab
        # handle subject's group assignment and create visit/session dir based on group, if needed.
        group = lib.get_node(self.json, j.GROUP)
        if not group == "":
            self.visitDir = j.checkVisitDir(subject,visit,group, self.json) ### create & populate session dir        
            return self.renderAndSave()   # saves the json, and renders the page
        else:
            return self.modalthing()  # render modal to assign group -> call setgroup() -> save json & render normally

    doMakoLogin.exposed = True
    def LogOut(self):
        print "LOGGING OUT!!!!"
        self.mySubjectDir=None
        self.jsonpath=None
        self.visitDir = None
        self.history = "<ul><li>logged in</li></ul>"
        self.json = deepcopy(j.info)
        self.subject = ""
        self.TabID = 99
        self.run = 99
        self.jsonpath = ""
        return self.index()
    LogOut.exposed = True

    def modalthing(self):
        try:
            subregTmpl = lookup.get_template("group_modal.html")
            return subregTmpl.render(cache_enabled=False, **self.json)
        except:
            return exceptions.html_error_template().render()
    modalthing.exposed=True

    def setgroup(self, group=None):
        ## Responds to result of modalthing's form submission. 
        ## Uses group value to create session dir.
        ## Note: group might not be assigned if "Cancel" is pressed
        if group:
            lib.set_node(self.json, group, j.GROUP)
            self.visitDir = j.checkVisitDir(self.subject, self.TabID, group, self.json) ### create & populate session dir
        return self.renderAndSave()
    setgroup.exposed=True

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
        ## NB: Clicking on a tab in the web-interface updates the json properly, but
        ##     the mako template (subreg.html) is not re-rendered, so "what you get" is NOT
        ##     "what you see". You must either cause the form to be submitted (click a button)
        ##     or logout and login again for the website to catch up to the json's reality.
        self.TabID = int(tab)
        self.visitDir = os.path.join(self.mySubjectDir, "session%d"%self.TabID)
        self.vNodePath = j.FULLSTUDY + ":%d:"%self.TabID
        lib.set_node(self.json,self.TabID,j.TAB)
        return self.renderAndSave()
    setTab.exposed=True

    def formHandler(self,button):
        print "received",button
        button_value = str(button).split(' ')
        btn_id = button_value[0]
        bNode = bt.btn_node(btn_id, self.json)
        bt.timeStamp(bNode)
        # remove the flotUpdate part of flotsript
        self.json["flotscript"] = self.json['flotscript'].split('flotUpdate();')[0] 
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
        """
        Don't do this until we're done with this action!
        TODO: figure out when RT runs and psychopy stuff is done
        """
        print "new progress will be",bid
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
            lib.set_here(bt.sib_node(node['id'], self.json, 1), "disabled", False)  ## activate psychopy
            lib.set_here(bt.sib_node(node['id'], self.json, 2), "disabled", False)  ## activate servenii
            lib.writeFlots(self.subject, self.TabID, node['run'])  ## update jquery for murfi plots
            print "attempting to change flotmurfi.js to use " + str(node['run']) +"!\n\n"
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
            print "mako_cherry: Can't handle this murfi button value:",btn_value
        return


    def makoDoStim(self,btn_value,node):
        print btn_value
        if ('RT' in btn_value):
            return self.makoRealtimeStim(btn_value,node)
        else:
            if ('Launch' in btn_value) or ('Test' in btn_value):
                psyFile = os.path.join(lib.RTDIR,node['file'])
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


    def makoRealtimeStim(self,btn_value,node):
        murfNode = bt.sib_node(node['id'], self.json, 0)
        stimLog = bt.nameLogfile(node, self.subject, murfNode)
        self.run = murfNode['run']   ## in case of accidental logout
        self.flotJavascript(self.TabID, self.run)
        # based on group, use proper stimulus file
        group = lib.get_node(self.json, j.GROUP)
        if group == "high":
            psychofile = j.HIFILE
        elif group == "low":
            psychofile = j.LOFILE
        lib.set_here(node, 'file', psychofile)  # record which stimulus file was used
        # ready to launch!
        self.stimProc, h = lib.doStim(self.subject, self.TabID, self.run, stimLog, psychofile)
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
        node['checked'] = not node['checked']  # toggle state
        self.updateProgress(node['id'])
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
        return
    completionChecks.exposed=True
        

    def flotJavascript(self, visit, run):
        self.json['flotscript'] = """
$(function () {
    """
        for i in range(1,int(run)):
            self.json['flotscript'] += """
    var data%d = [];
    var placeholder%d = $('#rtgraph%d');
    
    // fetch one series, adding to what we got
    
    function onDataReceived%d(series) {
	    
	data%d.push(series);
        $.plot(placeholder%d, data%d);
        };

    """%(i,i,i,i,i,i,i)
            self.json['flotscript'] += """$.ajax({
	    url: "subjects/%s/session%s/data/run%03d_active.json",
	    method: 'GET',
	    dataType: 'json',
	    success: onDataReceived%d
        });
        $.ajax({
	    url: "subjects/%s/session%s/data/run%03d_reference.json",
	    method: 'GET',
	    dataType: 'json',
	    success: onDataReceived%d
        });"""%(self.subject,visit,i,i,self.subject,visit,i,i)

        self.json['flotscript'] += """});
    function flotUpdate() {   
    $('#modalflot').modal('show')

    var data = [];
    var placeholder = $('#rtmodal');
    
    $.plot(placeholder, data);

    // fetch one series, adding to what we got
    var alreadyFetched = {};

    var iteration = 0;
    function fetchData() {
        ++iteration;
        data = []
        function onDataReceived(series) {
	    
	    data.push(series);
	
	    $.plot(placeholder, data);
        }

        $.ajax({
	    url: "subjects/%s/session%s/data/run%03d_active.json",
	    method: 'GET',
	    dataType: 'json',
	    success: onDataReceived
        });

        $.ajax({
	    url: "subjects/%s/session%s/data/run%03d_reference.json",
	    method: 'GET',
	    dataType: 'json',
	    success: onDataReceived
        });
        
        if (iteration < 63)
	    setTimeout(fetchData, 5000);
        else {
	    data = [];
	    alreadyFetched = {};
        }
    };

    setTimeout(fetchData, 1000);

fetchData()        
};
flotUpdate();
"""%(self.subject,visit,run,self.subject,visit,run) 
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
                      'tools.staticdir.dir':os.path.abspath('../flot/')},
              '/subjects': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath(lib.SUBJS)},
              }
    cherrypy.tree.mount(MakoRoot(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
