import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os
import time
from library import makeSession, SUBJS, load_json, save_json
from json_template import json

lookup = TemplateLookup(directories=['.','../cherrypy'],filesystem_checks=True,encoding_errors='replace')

class MakoRoot:
    def __init__(self):
        self.history = "<ul><li>logged in</li></ul>"
        self.json = json
        self.run = '1'

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
        self.activateVisit(int(visit))
        jsonpath = os.path.join(SUBJS,subject,"%s_experiment_info.json"%subject)
        if os.path.exists(jsonpath):
            self.json = load_json(jsonpath)
        else:
            self.json = json
            self.json['subject_id'] = subject 
            save_json(jsonpath,self.json)
        ### if no sessiondir exists, create it 
        if not os.path.exists(os.path.join(SUBJS,"%s/session%s/"%(subject,visit))):
            history = makeSession(subject,visit)   # returns history
            self.history = history + self.history
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(**self.json)
        except:
            return exceptions.html_error_template().render()
    doMakoLogin.exposed = True

    def activateVisit(self,visit):
        if visit > len(self.json['Protocol']):  ## visit must be defined in Protocol
            visit = 0
        for (i,v) in enumerate(self.json['Protocol']):
            if i==visit:
                v['active'] = True
            else:
                v['active'] = False
        return
    activateVisit.exposed = True

    def formHandler(self,button):
        if button == "TestSound":
            pass
        if button == "TestDisplay":
            pass
        if button == "1backbird":
            pass
        if button == "2backbird":
            pass
        if button == "1backtransfer":
            pass
        if button == "2backtransfer":
            pass
        if button =="Start Murfi":
            pass
        if button == "End Murfi":
            pass
        if button == "Start Serve":
            pass
        if button == "End Serve":
            pass
        if button == "RT Stimulus":
            pass
        subreg = lookup.get_template("subreg.html")
        return subreg.render(**self.json)
    formHandler.exposed=True
    
    def setTab(self,tab):
        subreg = lookup.get_template("subreg.html")
        self.TabID = int(tab)
        self.activateVisit(self.TabID) 
        return subreg.render(**self.json)
    setTab.exposed=True

    def setRun(self,run):
        subreg = lookup.get_template("subreg.html")
        self.Run = int(run)
        #self.json["Protocol"][self.TabID]["Steps"][3]["RT Session"][]
        #self.activateVisit(self.TabID) 
        return subreg.render(**self.json)
    setTab.exposed=True


if __name__ == "__main__":
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
#cherrypy.quickstart(HelloWorld())
