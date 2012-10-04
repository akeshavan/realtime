import os, re
import getpass
import subprocess
from glob import glob 
from copy import deepcopy
import json
import sys
from infoclientLib import InfoClient
from psychopy import __version__
from linecache import getline

HOME = os.path.abspath('.')
RTDIR = os.path.abspath('../../')
RTSCRIPTSDIR = os.path.abspath('../')
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
    psychoFile = "mTBI_rt.py"
    os.chdir(RTDIR)
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(run) > 1:   # run = 'Debug1' for 'runDebug1.xml'
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

def glob_nodes(hierarchy,path):
   if not path.count('*') == 1:
       print path
       raise LookupError("glob_nodes: supports exactly one * index!")
   star = path.index('*')
   preStar = path[:star]
   postStar = ":".join(path[star+1:])  # pass as string to force path slice to be copied over during each call to get_node()
   preNode = get_node(hierarchy,preStar)
   if isinstance(preNode,list):
       return [get_node(i,postStar) for i in preNode]
   else:
       print preNode
       raise LookupError("glob_nodes: cannot use '*' with a %s"%type(preNode))


def get_node(hierarchy, path=[], delimiter=":"):
    """ 
    Given a multi-layer object 'hierarchy' (with nested dicts and
    lists), return whatever's at a certain node, as addressed by
    'path', which may be a string (colon-separated by default,
    override using 'delimiter') or a list.

    Path may contain a single wildcard ('*') instead of a
    list-index. In this case, return a list of nodes, with all
    elements of that list substituted into path. Note: '*' may not be
    used as a delimiter!

    eg: btn = get_node(myJson, 'Protocol:0:Steps:0:text') 
    eg: btn = get_node(myJson, 'Protocol/0/Steps/0/text','/') 
    eg: btn = get_node(myJson, ['Protocol',0,'Steps',0,'text'])
    eg: allSteps = get_node(myJson, 'Protocol:0:Steps:*:text')
    """

    if isinstance(path,str):
        path = path.split(delimiter)   ## else, path is already a list
    if '*' in path:   ## handle globbing separately
        return glob_nodes(hierarchy,path)

    # Base case of recursion is when path is empty
    if not path:
        return hierarchy    
    branch = path.pop(0)
    # recurse into hierarchy using branch.
    # but check that branch is a valid index first!
    # at this point, hierarchy can only be a list or dict 
    if isinstance(hierarchy,list):
        try:
            target = hierarchy[int(branch)]
        except:
            raise IndexError("get_node: tried index %s on a list of length %d."%(str(branch),len(hierarchy)))
    elif isinstance(hierarchy,dict):
        try:
            target = hierarchy[str(branch)]  # should this be hierarchy[branch]?
        except:
            print hierarchy
            raise KeyError("get_node: failed to find key %s."%str(branch))
    else: 
        print hierarchy
        print "get_node: tried to use",str(branch), "to index into", type(hierarchy)
        raise TypeError
    return get_node(target,path)

def set_node(hierarchy, value, path=[], delimiter=":"):
    if isinstance(path,str):
        path = path.split(delimiter)   ## else, path is already a list
    mypath = deepcopy(path)  ## to avoid modifying original
    leaf = mypath.pop()
    set_here(get_node(hierarchy,mypath),leaf,value)
    return

def set_here(node, leaf, value):
    """
    Set node[leaf] to value.
    Only leaves (nodes with no children) are settable
    node = a list or dict
    leaf = str or int that indexes into node
    Thus node[leaf] = str, bool, numeric, etc. 

    eg: set_here(myJson,"subject_id","pilot42")
    eg: set_here(get_node(myJson,"Protocol:0"),"complete",True)
    """
    if isinstance(node, list):
        try:
            leaf = int(leaf)
            oldval = node[leaf]
        except TypeError:
            raise TypeError("set_here: %s cannot be used to index a list."%leaf)
        except IndexError:
            raise IndexError("set_here: tried index %d on list of length %d"%(leaf,len(node)))
    elif isinstance(node,dict):
        try:
            oldval = node[str(leaf)]
        except KeyError:
            raise KeyError("set_here: failed to find key %s."%str(leaf))
    else:
        print node
        raise TypeError("set_here: Requires a list or dict, not a %s."%type(node))

    # Ensure node[leaf] has no children, then set it to value
    if isinstance(oldval, (list,dict)):
        print oldval
        raise TypeError("Cannot set this node because it is a list or dict.")
    else:
        node[leaf] = value  
    return
