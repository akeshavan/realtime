import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os
import time
from library import makeSession, SUBJS

json = {"subject_id":"",
        "time":time.ctime(),
        "Protocol":[{"name":"Localizer",
                     "Steps":[{"name":"Test Sounds","type":"button","value":"TestSound"},
                              {"name":"Test Display","type":"button","value":"TestDisplay"},
                              {"name":"Run localizer32", "type":"checkbox"},
                              {"name":"Run AAScout", "type":"checkbox"},
                              {"name":"Run MPRAGE", "type":"checkbox"},
                              {"name":"Start 1-back localizer","type":"button","value":"1back"},
                              {"name":"Start 2-back localizer","type":"button","value":"2back"}],
                     "active":True},
                    {"name":"Visit 1",
                     "Steps":[{"name":"Test Display","type":"button","value":"TestSound"},
                              {"name":"Run localizer32", "type":"checkbox"},
                              {"name":"Run AAScout", "type":"checkbox"}], 
                     "active":False},
                    {"name":"Visit 2",
                     "Steps":[{"name":"Test Display","type":"button","value":"TestSound"},
                              {"name":"Run localizer32", "type":"checkbox"},
                              {"name":"Run AAScout", "type":"checkbox"}],
                     "active":False} ] }
  

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
        self.activateVisit(int(visit),json)
        json['subject_id'] = subject 
        ### if no sessiondir exists, create it 
        if not os.path.exists(os.path.join(SUBJS,"%s/session%s/"%(subject,visit))):
            history = makeSession(subject,visit)   # returns history
            self.history = history + self.history
        try:
            subregTmpl = lookup.get_template("subreg.html")
            return subregTmpl.render(**json)
        except:
            return exceptions.html_error_template().render()
    doMakoLogin.exposed = True

    def activateVisit(self,visit,json):
        if visit > len(json['Protocol']):  ## visit must be defined in Protocol
            visit = 0
        for (i,v) in enumerate(json['Protocol']):
            if i==visit:
                v['active'] = True
            else:
                v['active'] = False
        return
    activateVisit.exposed = True

    def formHandler(self,button):
        subreg = lookup.get_template("subreg.html")
        return subreg.render(**json)
    formHandler.exposed=True

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
