import cherrypy
import subprocess
import os
from library import doMurfi, endMurfi, doServ, endServ, doStim, makeSession, HOME, SUBJS,makeFakeData,createSubDir,testDisplay, testTrigger,testButton,testBirdSounds,testLetterSounds, testInfoClient_Start
import getpass

class HelloWorld:
    def __init__(self):
        self.run = '1'
        self.history = "<ul><li>logged in</li></ul>"
    
    def index(self):
        with open(os.path.join(HOME,'index.html')) as fp:
            msg = fp.readlines()
        login = """<!--#include virtual="index.html" -->
<div style="background-color: white; text-align: left; padding: 0px 10px 200px 10px">
<form action="doLogin" method="post">

    <p><div style="padding: 50px 10px 10px 10px">Subject:
    <input type="text" name="subject" value=""
        size="10" maxlength="40"/></div></p>
    <p><div style="padding: 10px 10px 10px 10px">Visit #:
    <input type="text" name="visit" value=""
        size="10" maxlength="40"/></div></p>
    <p><div style="padding: 10px 10px 10px 75px"><input type="submit" value="Login"/>
    <input type="reset" value="Clear"/></div></p>
</form>
</div>
"""
        msg+= login
        with open(os.path.join(HOME,'footer.html')) as fp:
            foot = fp.readlines()
        return msg+foot       ###end: def index()
    index.exposed = True

    def doLogin(self,subject=None,visit=None):
        self.subject = subject
        self.visit = visit
        with open(os.path.join(HOME,'index.html')) as fp:
            msg = fp.readlines()
        with open(os.path.join(HOME,'historybar.html')) as fp:
            hist = fp.readlines()
        msg += hist 
        ## if no subject/sessiondir exists, create it - also if the mask and study ref exist lets make fakedata
        if not os.path.exists(os.path.join(SUBJS,subject)):
            self.history = createSubDir(subject) + self.history
        if os.path.exists(os.path.join(SUBJS,subject,'mask','%s_roi.nii'%subject)) \
            and os.path.exists(os.path.join(SUBJS,subject,'xfm','%s_study_ref.nii'%subject))\
            and not os.path.exists(os.path.join(SUBJS,subject,'run1.nii')):
            pass
            #self.history = makeFakeData(subject) +self.history
        if not os.path.exists(os.path.join(SUBJS,"%s/session%s/"%(subject,visit))):
            history = makeSession(subject,visit)   # returns history
            self.history = history + self.history
        msg += self.history
        msg += """</div></div>"""
        subject_info = """
<div style="background-color: white; text-align: left; padding: 0px 10px 10px 10px">
<p>
 <br><b>Subject:</b> %s 
 <br><b>Visit #:</b> %s 
</p>
<p>

<form method="post" action="formHandler">

    <p><div style="padding: 10px 10px 10px 10px">Run #:
    <input type="text" name="run" value=%s
        size="10" maxlength="40"/></div></p>
    <p><b>Tests:</b>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Test Display"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Test Buttons"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Test Scanner Trigger"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Test Letter Sounds"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Test Bird Sounds"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Start InfoClient Test"></div>
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Check InfoClient"></div>
    </p>
    <p><b>Murfi:</b>
    <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Start Murfi"></div>
    <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="End Murfi"></div></p>
    <p><b>Fake Data:</b>
    <br><div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Serve"></div>
    <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="End Serve"></div></p>
    <p><b>Stimulus:</b>
    <br><div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="Stimulus"></p>
</form>
</p>
""" % (subject, visit, self.run)
        msg += subject_info
        with open(os.path.join(HOME,'footer.html')) as fp:
            foot = fp.readlines()
        return msg+foot     ### end: def doLogin()

    doLogin.exposed=True

    def formHandler(self,run=None,button=None):
        self.run = run   # run number
        if button=="Start Murfi":
            return self.doMurfi(run)
        if button=="End Murfi":
            return self.endMurfi(run)
        if button=="Serve":
            return self.doServ(run)
        if button=="End Serve":
            return self.endServ(run)
        if button=="Stimulus":
            return self.doStim(run)
        if button=="Test Display":
            history = testDisplay()
            self.history = history + self.history
            return self.doLogin(self.subject,self.visit)
        if button=="Test Buttons":
            history = testButton()
            self.history = history + self.history
            return self.doLogin(self.subject,self.visit)
        if button=="Test Bird Sounds":
            history = testBirdSounds()
            self.history = history + self.history
            return self.doLogin(self.subject,self.visit)
        if button=="Test Letter Sounds":
            history = testLetterSounds()
            self.history = history + self.history
            return self.doLogin(self.subject,self.visit)
        if button=="Test Scanner Trigger":
            history = testTrigger()
            self.history = history + self.history
            return self.doLogin(self.subject,self.visit)
        if button=="Start InfoClient Test":
            history = "<ul><li> Started info client, please serve fakedata </li></ul>"
            self.history = history + self.history
            self.ic = testInfoClient_Start()
            return self.doLogin(self.subject,self.visit)            
        if button=="Check InfoClient":
           log = open("/home/%s/Desktop/infoClientTest.txt"%getpass.getuser(),'w') 
           log.write(str(self.ic.check()))
           log.close()
           self.history = "<ul><li> checked infoclient </li></ul>" + self.history
           self.ic.stop()
           return self.doLogin(self.subject,self.visit)
            
        ### end: def formHandler()

    formHandler.exposed=True

    def doMurfi(self,run=None):
        proc, history = doMurfi(self.subject,self.visit,run)
        self.murfi_subprocess = proc
        self.history = history + self.history
        return self.doLogin(self.subject,self.visit)
        
    doMurfi.exposed=True

    def endMurfi(self,run=None):
        history = endMurfi(self.murfi_subprocess,self.subject,self.visit,run)
        self.history = history + self.history
        return self.doLogin(self.subject,self.visit)

    endMurfi.exposed=True

    def doServ(self,run=None):
        proc, history = doServ(self.subject,self.visit,run)
        self.serv_subprocess = proc
        self.history = history + self.history 
        return self.doLogin(self.subject,self.visit)

    doServ.exposed=True 
    
    def endServ(self,run=None):
        history = endServ(self.serv_subprocess,self.subject,self.visit,run)
        self.history = history + self.history
        return self.doLogin(self.subject,self.visit)

    endServ.exposed=True

    def doStim(self,run=None):
        proc, history = doStim(self.subject,self.visit,run)
        self.history = history + self.history 
        return self.doLogin(self.subject,self.visit)
    
    doStim.exposed=True

if __name__ == "__main__":
    config = {'/': {'tools.staticdir.on': True,
                    'tools.staticdir.dir': os.getcwd()},
              '/css': {'tools.staticdir.on': True,
                       'tools.staticdir.dir': os.path.abspath('css/')},
              }
    cherrypy.tree.mount(HelloWorld(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
#cherrypy.quickstart(HelloWorld())
