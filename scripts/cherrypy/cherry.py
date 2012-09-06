import cherrypy
import subprocess
import os
from library import doMurfi, endMurfi, doServ, endServ, doStim, makeSession, HOME, SUBJS,makeFakeData,createSubDir,testDisplay, testTrigger,testButton,testBirdSounds,testLetterSounds, testInfoClient_Start
import getpass
from psychopy import data
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
        date = data.getDateStr()[:-5]
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
       <div style="padding: 10px 10px 10px 10px"><input type="submit" name="button" value="End InfoClient"></div>
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

<div id="placeholder" style="width:600px;height:300px;"></div>

<p>
      <input class="dataUpdate" type="button" value="Poll for data">
    </p>
<script type="text/javascript">
$(function () {
    var options = {
        lines: { show: true },
        points: { show: true },
        xaxis: { tickDecimals: 0, tickSize: 1 }
    };
    var data = [];
    var placeholder = $("#placeholder");
    
    $.plot(placeholder, data, options);

    
    // fetch one series, adding to what we got
    var alreadyFetched = {};
    
    $("input.fetchSeries").click(function () {
        var button = $(this);
        
        // find the URL in the link right next to us 
        var dataurl = button.siblings('a').attr('href');

        // then fetch the data with jQuery
        function onDataReceived(series) {
            // extract the first coordinate pair so you can see that
            // data is now an ordinary Javascript object
            var firstcoordinate = '(' + series.data[0][0] + ', ' + series.data[0][1] + ')';
            button.siblings('span').text('Fetched ' + series.label + ', first point: ' + firstcoordinate);

            // let's add it to our current data
            if (!alreadyFetched[series.label]) {
                alreadyFetched[series.label] = true;
                data.push(series);
            }
            
            // and plot all we got
            $.plot(placeholder, data, options);
         }
        
        $.ajax({
            url: dataurl,
            method: 'GET',
            dataType: 'json',
            success: onDataReceived
        });
    });


    // initiate a recurring data update
    $("input.dataUpdate").click(function () {
        // reset data
        data = [];
        alreadyFetched = {};
        
        $.plot(placeholder, data, options);

        var iteration = 0;
        
        function fetchData() {
            ++iteration;
            data = []
            function onDataReceived(series) {
                // we get all the data in one go, if we only got partial
                // data, we could merge it with what we already got
                
                //if (!alreadyFetched[series.label]) {
                //alreadyFetched[series.label] = true;
                //data.push(series);
                //}
                data.push(series);
                
                $.plot($("#placeholder"), data, options);
            }
        
            $.ajax({
                // usually, we'll just call the same URL, a script
                // connected to a database, but in this case we only
                // have static example files so we need to modify the
                // URL
                url: "subjects/%s/session%s/data/%s_%s_run_%03d_active.json",
                method: 'GET',
                dataType: 'json',
                success: onDataReceived
            });

            $.ajax({
                // usually, we'll just call the same URL, a script
                // connected to a database, but in this case we only
                // have static example files so we need to modify the
                // URL
                url: "subjects/%s/session%s/data/%s_%s_run_%03d_reference.json",
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
        }

        setTimeout(fetchData, 1000);
    });
});
</script>



""" % (subject, visit, self.run,subject,visit,subject,date,int(self.run),subject,visit,subject,date,int(self.run))
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
            self.rt = testInfoClient_Start()
            return self.doLogin(self.subject,self.visit)            
        if button=="Check InfoClient":
           log = open("/home/%s/Desktop/infoClientTest.txt"%getpass.getuser(),'w') 
           self.rt.check()
           log.write(str(self.rt.xml))
           log.close()
           self.history = "<ul><li> checked infoclient </li></ul>" + self.history
           return self.doLogin(self.subject,self.visit)
        if button=="End InfoClient":
           self.rt.close()
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
              '/flot': {'tools.staticdir.on': True,
                         'tools.staticdir.dir': os.path.abspath('../flot')},
              '/subjects': {'tools.staticdir.on': True,
                         'tools.staticdir.dir': '/home/%s/subjects'%getpass.getuser()},
              }
    cherrypy.tree.mount(HelloWorld(),'/',config=config)
    cherrypy.engine.start()
    cherrypy.engine.block()
#cherrypy.quickstart(HelloWorld())
