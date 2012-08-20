import os, re
import getpass
import subprocess
from glob import glob 

HOME = os.path.abspath('.')
RTDIR = os.path.abspath('../../')
SUBJS = os.path.abspath("/home/%s/subjects/"%getpass.getuser())

def doMurfi(subject,visit,run,murfOUT):
    print "starting murfi ......................."
    os.chdir("/home/%s/subjects/%s/session%s"%(getpass.getuser(),subject,visit))
    foo = subprocess.Popen(["murfi","-f","scripts/run%s.xml"%run],stdout=murfOUT,stderr=subprocess.STDOUT)
    history = "<ul><li> Started Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return foo, history

    
def endMurfi(proc,subject,visit,run,murfOUT):
    proc.kill()
    murfOUT.close()
    history = "<ul><li> Ended Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return history


def doServ(subject,visit,run,servOUT):
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
    foo = subprocess.Popen(["servenii4d","run%s.nii"%runNum,"localhost",scannerport,tr],stdout=servOUT,stderr=subprocess.STDOUT)
    history = "<ul><li> Served Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)  
    return foo, history


def endServ(proc,subject,visit,run,servOUT):
    proc.kill()
    servOUT.close()
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
