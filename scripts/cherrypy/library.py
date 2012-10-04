import os, re
import getpass
import subprocess
from glob import glob 
import json
import sys
from infoclientLib import InfoClient
sys.path.append(os.path.abspath('../'))

HOME = os.path.abspath('.')
RTDIR = os.path.abspath('../../')
SUBJS = os.path.abspath("/home/%s/subjects/"%getpass.getuser())

def doMurfi(subject,visit,run):
    print "starting murfi ......................."
    os.chdir("/home/%s/subjects/%s/session%s"%(getpass.getuser(),subject,visit))
    foo = subprocess.Popen(["murfi","-f","scripts/run%s.xml"%run])
    history = "<ul><li> Started Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return foo, history

    
def endMurfi(proc,subject,visit,run):
    proc.kill()
    history = "<ul><li> Ended Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return history


def doServ(subject,visit,run):
    os.chdir("/home/%s/subjects/%s"%(getpass.getuser(),subject))
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
    return foo, history


def endServ(proc,subject,visit,run):
    proc.kill()
    history = "<ul><li> Stopped Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return history


def doStim(subject,visit,run):
    os.chdir(RTDIR)
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(run) > 1:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
    else:
        debug = '0'
    runNum = run[-1]  # will produce the number either way
    proc = ["python", "mTBI_rt.py", subject, visit, '00%s'%runNum, debug]
    print ' '.join(proc)
    foo = subprocess.Popen(["python", "mTBI_rt.py", subject, visit, '00%s'%runNum, debug])    
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
    spval = subprocess.Popen(["python", "createRtSession.py", subject, visit, 'none'])
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
    from xmlparse import RT
    """
    ic = None
    xml = []

    localPort = 15002  # default
    remotePort = 15003  # default
    if os.environ.has_key('ICLOCALPORT'):
        localPort = int(os.environ['ICLOCALPORT'])
    if os.environ.has_key('ICREMOTEPORT'):
        remotePort = int(os.environ['ICREMOTEPORT'])       	
    ic = InfoClient('localhost', localPort, 'localhost', remotePort)
    ic.add('roi-weightedave', 'active')
    ic.add('roi-weightedave','reference')
    ic.start()
    print "initialized new RT"
    return ic"""
    a = RT()
    return a


