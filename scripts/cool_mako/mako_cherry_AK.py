import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import subprocess
import os
import time
from library import makeSession, SUBJS, load_json, save_json, createSubDir
import library as lib
from json_template import json
import numpy as np
lookup = TemplateLookup(directories=['.','../cherrypy'],filesystem_checks=True,encoding_errors='replace',strict_undefined=True)

class MakoRoot:
    def __init__(self):
        self.history = "<ul><li>logged in</li></ul>"
        self.json = json
        self.TabID = 99
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
        self.jsonpath = os.path.join(SUBJS,subject,"%s_experiment_info.json"%subject)
        if os.path.exists(self.jsonpath):
            self.json = load_json(self.jsonpath)
        else:
            self.json = json
            self.json['subject_id'] = subject 
        self.json['time'] = time.ctime() ## record new login time
        visit = [v['active'] for v in self.json['Protocol']].index(True)  # auto-get last open tab
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
        #self.completionChecks()   # activates the next relevant button
        save_json(self.jsonpath,self.json)
        try:
            subregTmpl = lookup.get_template("subreg.html")
            print "Rendering"
            return subregTmpl.render(**self.json)
        except:
            return exceptions.html_error_template().render()
    renderAndSave.exposed=True


    def formHandler(self,button):
        Dict = self.locate(button)
        if Dict["ui"]=="button":
            exec(Dict["action"])
        if Dict["ui"]=="checkbox":
            Dict["checked"] = not Dict["checked"]
        Dict["clicked"] = True
        self.eval_click(Dict)
        self.set_all_dicts(self.json["Protocol"])
        return self.renderAndSave()

    formHandler.exposed=True

    def eval_click(self,Dict):
        lists = Dict["on_click"].split(",,")
        print lists
        for dicts in lists:
            key, item = dicts.split(" = ")
            Dict[key] = eval(item)

    def setdict(self,Dict):
        if not Dict["ui"] == "loop":
            if not Dict["enabled_when"] == None:
                print Dict["text"]
                Dict["disabled"] = not self.eval_bool(Dict["enabled_when"])
        else:
            self.set_all_dicts(Dict["Steps"])

    def set_all_dicts(self,Dict):
        for D in Dict:
            self.setdict(D)

    def eval_bool(self,phrase):
        c = []
        coords = phrase.replace("and","")
        coords = coords.replace("or","")
        coords = coords.replace("(","")
        coords = coords.replace(")","")
        coords = coords.replace("not","")
        coords = coords.replace("!","").replace("  ", " ").replace("  "," ")
        c = coords.split(" ")
        for loc in c:
            print loc
            D = self.locate(loc)
            phrase = phrase.replace(loc,str(D["clicked"]))
        print "phrase = ", phrase
        return eval(phrase)    

    def locate(self,coord):
        coords = coord.split('.')
        coords = np.asarray(coords).astype(int).tolist()
        x = lambda P, l: P[l]
        step = lambda P: P["Steps"]
        Protocol = self.json["Protocol"]
        P = Protocol
        for i,c in enumerate(coords):
            P = x(P,c)
            if i == len(coords)-1:
                return P
            else:
                P = step(P)
    
    def setTab(self,tab):
        self.TabID = int(tab)
        if self.TabID > len(self.json['Protocol']):  ## visit must be defined in Protocol
            self.TabID = 0
        for (i,v) in enumerate(self.json['Protocol']):
            if i==self.TabID:
                v['active'] = True
            else:
                v['active'] = False
        print "Did set tab!"
        return self.renderAndSave()
    setTab.exposed=True



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
              '/flot': {'tools.staticdir.on': True,
                        'tools.staticdir.dir': os.path.abspath('../flot')},
              '/img': {'tools.staticdir.on': True, 
                      'tools.staticdir.dir':os.path.abspath('img/')}
              }
    cherrypy.tree.mount(MakoRoot(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
