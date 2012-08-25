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
        save_json(self.jsonpath,self.json)
        #print self.json
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(**self.json)
        except:
            return exceptions.html_error_template().render()
    renderAndSave.exposed=True

    def formHandler(self,button):
        if button == "Test Sounds -":
            pass
        if button == "Test Display -":
            pass
        if button == "Start 1-back localizer":
            pass
        if button == "Start 1-back transfer":
            pass
        if button == "Start 2-back transfer":
            pass
        else:            
            [act,program,runNum] = button.split(' ')
#            self.setRun(runNum)
            self.buttonReuse(button)
            # if act == "Start":
            #     newText = "End %s"%program
            #     if program == "Murfi":
            #         btnNum = 0

            # if program =="Murfi":
            #     if runNum == '1':
            #         print "pressed start murfi 1"
            #     if act == "Start":
            #         findInJson = ["Protocol",self.TabID,"Steps",3,"Steps",0]
            #         self.buttonReuse("End Murfi",findInJson)
        return self.renderAndSave()

    formHandler.exposed=True
    
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
            self.setRun(1)
            print "\nTabID is %d\n"%self.TabID
        return self.renderAndSave()
    setTab.exposed=True

    def setRun(self,run):
        self.json["Protocol"][self.TabID]["activeRunNum"] = int(run)
        return
    setTab.exposed=True

    def buttonReuse(self,button):
        ## When a button has been pressed, (say to start something),
        ## rename it to the opposite function (say, to end the thing)
        [act,prog,runNum] = button.split(' ')
        if (act == "Start") or (act == "Restart"):
            newText = "End %s"%prog
        elif act == "End":
            newText = "Restart %s"%prog
        else:    ## not startable/endable  (or disable here?)
            return
        ## end if (act...
        if prog == "Murfi":
            btnNum = 0
        elif prog == "Serve":
            btnNum = 1
        else:   # disable is going to suck here
            return 
        ## end if prog...
        self.json['Protocol'][self.TabID]['Steps'][3]['Steps'][btnNum]["text"] = newText
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
