import cherrypy
import subprocess
import os
from mako.template import Template
import time

json = {"subject_id":"pilot17",
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
                              {"name":"Run AAScout", "type":"checkbox"}]}],
                     "active":False}
foo = Template(filename='subreg.html',encoding_errors='replace')

class HelloWorld:
    run = '1'
    history = "<ul><li>logged in</li></ul>"
    json = json
    def index(self):
        return foo.render(**json)
    index.exposed = True

    def formHandler(self,button):
        return foo.render(**json)
    
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
    cherrypy.tree.mount(HelloWorld(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
#cherrypy.quickstart(HelloWorld())
