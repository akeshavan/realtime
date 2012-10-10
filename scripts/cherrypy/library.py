import os, re
import getpass
import subprocess
from glob import glob 
import json
import sys
from infoclientLib import InfoClient
from psychopy import __version__
from linecache import getline

HOME = os.path.abspath('.')
RTDIR = os.path.abspath('../../')
RTSCRIPTSDIR = os.path.abspath('../')
SUBJS = os.path.abspath("/home/%s/subjects/"%getpass.getuser())

def doMurfi(subject,visit,run,self,loc):
    print "starting murfi ......................."
    os.chdir("/home/%s/subjects/%s/session%s"%(getpass.getuser(),subject,visit))
    foo = subprocess.Popen(["murfi","-f","scripts/run%s.xml"%run])
    history = "<ul><li> Started Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    foo1, hist1 = doStim(subject,visit,run,self.json["placebo"])
    print "Is placebo???", self.json["placebo"]
    os.chdir(HOME)
    if not loc == None:
        endMurfiButton(self,loc)
    return [foo,foo1], history+hist1

    
def endMurfi(proc,subject,visit,run,murfOUT=None):
    for p in proc:
        p.kill()
    #murfOUT.close()
    history = "<ul><li> Ended Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return history


def doServ(subject,visit,run,self,servOUT=None,loc=None):
    os.chdir("/home/%s/subjects/%s"%(getpass.getuser(),subject))
    visit = str(visit)
    run = str(run)
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(run) > 1:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
        tr = '0.5'
    else:
        debug = '0'
        tr = '2'
    runNum = run[-1]  # will produce the number either way
    if os.environ.has_key("SCANNERPORT"):
        scannerport = os.environ["SCANNERPORT"]
    else:  # use default SCANNERPORT
        scannerport = str(15000)
    foo = subprocess.Popen(["servenii4d","run%s.nii"%runNum,"localhost",scannerport,tr])
    history = "<ul><li> Served Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)  
    os.chdir(HOME)
    if not loc == None:
        endServeButton(self,loc)
    return foo, history


def endServ(proc,subject,visit,run,servOUT=None):
    proc.kill()
    #servOUT.close()
    history = "<ul><li> Stopped Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return history


def doStim(subject,visit,run,placebo=False):
    if placebo:
        psychoFile = "mTBI_rt_placebo.py"
    else:
        psychoFile = "mTBI_rt.py"
    os.chdir(RTDIR)
    run = str(run)
    visit = str(visit)
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(str(run)) > 1:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
    else:
        debug = '0'
    runNum = run[-1]  # will produce the number either way
    proc = ["python", psychoFile, subject, visit, '00%s'%runNum, debug]
    ## verify that our current psychopy version matches experiment creation version
    verline = getline(os.path.join(RTDIR,psychoFile),4)  ## linecache.getline gets the line by number
    ver = re.search("v(\d+\.\d+\.\d+)",verline).group(1) ## grab the version number
    if ver != __version__:
        print "Psychopy version (%s) doesn't match the experiment (%s)!"%(__version__,ver)
        sys.exit(1)
    print ' '.join(proc)
    foo = subprocess.Popen(["python", psychoFile, subject, visit, '00%s'%runNum, debug])    
    history = "<ul><li> Started Simulus for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return foo, history
    
def doStimPlacebo(subject,visit,run):
    os.chdir(RTDIR)
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(run) > 1:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
    else:
        debug = '0'
    runNum = run[-1]  # will produce the number either way
    proc = ["python", "mTBI_rt_placebo.py", subject, visit, '00%s'%runNum, debug]
    print ' '.join(proc)
    foo = subprocess.Popen(["python", "mTBI_rt_placebo.py", subject, visit, '00%s'%runNum, debug])    
    history = "<ul><li> Started Placebo Simulus for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return foo, history
 
def makeSession(subject,visit):
    whereami = os.path.abspath('.')
    os.chdir(RTDIR+'/scripts/')
    spval = subprocess.Popen(["python", "createRtSession.py", str(subject), str(visit), 'none'])
    history = "<ul><li>Created new session for %s: session%s</li></ul>"%(subject,visit)
    os.chdir(whereami)
    return history

def makeFakeData(subject):
    print os.getcwd()
    os.chdir(RTDIR)
    print os.getcwd()
    print glob("*.py")
    a = ["python","make_fakedata.py",subject]
    foo = subprocess.Popen(a)
    history = "<ul><li>Generated FakeData for %s </ul></li>"%subject
    return history

def createSubDir(subject):
    os.mkdir(os.path.join(SUBJS,subject))
    history = "<ul><li> Created directory for %s </li></ul>"%subject
    os.mkdir(os.path.join(SUBJS,subject,'session0'))   ## visit=0, initial localizer
    os.mkdir(os.path.join(SUBJS,subject,'session5'))     ## visit=5, final localizer
    return history


def testDisplay():
    os.chdir(RTDIR)
    a = ["python", "DisplayTest.py"]
    foo = subprocess.Popen(a)
    return "<ul><li> Tested Display </li></ul>"

def testTrigger():
    os.chdir(RTDIR)
    a = ["python", "TriggerTest.py"]
    foo = subprocess.Popen(a)
    return "<ul><li> Tested Trigger </li></ul>"

def testButton():
    os.chdir(RTDIR)
    a = ["python", "ButtonTest.py"]
    foo = subprocess.Popen(a)
    return "<ul><li> Tested Buttons </li></ul>"


def testBirdSounds():
    os.chdir(os.path.join(RTDIR,"localXfer"))
    a = ["python", "SoundTest_Bird.py"]
    foo = subprocess.Popen(a)
    return "<ul><li> Tested Bird Sounds </li></ul>"

def testFull():
    os.chdir(os.path.join(RTDIR,"localXfer"))
    a = ["python", "FullTest.py"]
    foo = subprocess.Popen(a)
    os.chdir(HOME)
    return "<ul><li> Tested Setup </li></ul>"

def testLetterSounds():
    os.chdir(os.path.join(RTDIR,"localXfer"))
    a = ["python", "SoundTest_Letter.py"]
    foo = subprocess.Popen(a)
    return "<ul><li> Tested Letter Sounds </li></ul>"


def save_json(filename, data):
    """Save data to a json file

Parameters
----------
filename : str
Filename to save data in.
data : dict
Dictionary to save in json file.

"""

    fp = file(filename, 'w')
    json.dump(data, fp, sort_keys=True, indent=4)
    fp.close()


def load_json(filename):
    """Load data from a json file

Parameters
----------
filename : str
Filename to load data from.

Returns
-------
data : dict

"""

    fp = file(filename, 'r')
    data = json.load(fp)
    fp.close()
    return data

def testInfoClient_Start():
    sys.path.append(RTSCRIPTSDIR)
    from xmlparse import RT
    a = RT()
    return a

def redoRun(self,murfiloc,serveloc=None):
    Dict = self.locate(murfiloc)
    print Dict["text"]
    Dict["text"] = "Start Murfi"
    Dict["clicked"] = False
    Dict["action"] = "self.murfiproc,_ = lib.doMurfi(\"%s\",%s,%d,self,loc=\'%s\')"%(self.json["subject_id"],
                                                                   Dict["value"].split('.')[0],
                                                                   int(Dict["value"].split('.')[2])+1,murfiloc)
    Dict["disabled"] = False
    print Dict["action"]
    if not serveloc == None:
        print Dict
        Dict = self.locate(serveloc)
        Dict["text"] = "Start Serve"
        Dict["clicked"] = False
        Dict["action"] = "self.serveproc,_ = lib.doServ(\"%s\",%s,%d,self,loc=\'%s\')"%(self.json["subject_id"],
                                                                   Dict["value"].split('.')[0],
                                                                   int(Dict["value"].split('.')[2])+1,serveloc)
        Dict["disabled"] = False

def endMurfiButton(self,loc):
    Dict = self.locate(loc)
    visit, run = loc.split('.')[0], loc.split('.')[2]
    Dict['disabled'] = False
    Dict['text'] = 'End Murfi'
    Dict['action'] = "lib.endMurfi(self.murfiproc,\'%s\',%s,%s)"%(self.json["subject_id"],visit,run)
    Dict['clicked'] = True
    Dict['on_click'] = None

def endServeButton(self,loc):
    Dict = self.locate(loc)
    visit, run = loc.split('.')[0], loc.split('.')[2]
    Dict['disabled'] = False
    Dict['text'] = 'End Serve'
    Dict['action'] = "lib.endServ(self.serveproc,\'%s\',%s,%s)"%(self.json["subject_id"],visit,run)
    Dict['clicked'] = False
    Dict['on_click'] = None

def completeVisit(self,coord):
    loc = int(coord.split('.')[0])
    visit = self.json["Protocol"][loc]
    visit["complete"] = True
