import os, re
from shutil import copy
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

def doMurfi(subject,visit,run,murfLog):
    """
    Starts murfi, creating logfiles for murfi stdout/stderr
    In: subject (str), visit (int), run (int), murfLog (str -- desired logfile name)
    Out: murfProc (process handle), murfOUT (filehandle), history (str -- for cherrypy)
    """
    print "starting murfi ......................."
    murfOUT = open(murfLog, 'w')  # stdout/stderr go to this file
    myDIR = os.path.abspath(os.getcwd())
    os.chdir(os.path.join(SUBJS,subject,"session%s"%visit))  ## maybe use subprocess.Popen(cwd=thisthing)
    murfProc = subprocess.Popen(["murfi","-f","scripts/run%s.xml"%run],stdout=murfOUT,stderr=subprocess.STDOUT)
    os.chdir(myDIR)
    history = "<ul><li> Started Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return murfProc, murfOUT, history

    
def endMurfi(proc,subject,visit,run,murfOUT):
    print "ending murfi ..  ..  ..  ..  ..  ..  .."
    proc.kill()
    murfOUT.close()
    history = "<ul><li> Ended Murfi for %s, visit %s, run %s</li></ul>"%(subject, visit,run)
    return history


def doServ(subject,visit,run,servLog):
    """
    Starts servenii4d, creating logfiles for its stdout/stderr
    In: subject (str), visit (int), run (int), servLog (str -- desired logfile name)
    Out: servProc (process handle), servOUT (filehandle), history (str -- for cherrypy)
    """
    ####  ASSUMES RUN < 10 (SINGLE DIGIT)!!!
    if len(str(run)) > 1:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
        tr = '0.5'
    else:
        debug = '0'
        tr = '2'
    runNum = str(run)[-1]  # will produce the number either way
    if os.environ.has_key("SCANNERPORT"):
        scannerport = os.environ["SCANNERPORT"]
    else:  # use default SCANNERPORT
        scannerport = str(15000)
    fakedata = (os.path.join(SUBJS,subject,"run%s.nii"%runNum))
    servCommand = map(str,["servenii4d",fakedata,"localhost",scannerport,tr])
    print ' '.join(servCommand)
    print "starting servenii4d - - - - - - - - - - - - - - -"
    servOUT = open(servLog, 'w')  # stdout/stderr go to this file
    servProc = subprocess.Popen(servCommand, stdout=servOUT, stderr=subprocess.STDOUT)
    history = "<ul><li> Served Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)  
    return servProc, servOUT, history


def endServ(proc,subject,visit,run,servOUT):
    print "ending servenii4d .-.  .-.  .-.  .-.  .-."
    proc.kill()
    servOUT.close()
    history = "<ul><li> Stopped Fake Data for %s, visit %s, run %s</li></ul>"%(subject,visit,run)
    return history


def startPsycho(psyFile, psyArgs, log):
    """
    Starts psychopy, creating logfiles for its stdout/stderr
    In: psyFile (str): fullpath + name of psychopy coder mode file
        psyArgs (list of str): command-line arguments to psyFile 
        log (str): fullpath + name of desired logfile
    Out: psyProc (process handle), history (str -- for cherrypy)
    """
    if not os.path.exists(psyFile):
        raise OSError('startPsycho: Psychopy file not found! %s'%psyFile)
    psyDir = os.path.abspath(os.path.dirname(psyFile))
    psyCommand = ["python", psyFile] + (map(str,psyArgs))
    print ' '.join(psyCommand)
    if checkPsychopyVersion(psyFile) == 'match':
        print "starting stimulus -*-  -*-  -*-  -*-  -*- -*-"
        with open(log, 'w') as psyOUT:  # stdout/stderr abspath
            psyProc = subprocess.Popen(psyCommand, stdout=psyOUT, stderr=subprocess.STDOUT, cwd=psyDir)
            history = "<ul><li> Started Psychopy: %s; Logged at: %s</li></ul>"%(psyFile,log)
    else:
        psyProc = None
        history = "<ul><li>Error: Psychopy version mismatch: %s</li></ul>"%psyFile
    return psyProc, history


def doStim(subject,visit,run,stimLog,group):
    """
    Wraps startPsycho() for realtime stimulus. 
    ### NOTDONE group support!
    In: subject (str), visit (int), run (int/str), stimLog (str -- desired logfile name)
    Out: stimProc (process handle), history (str -- for cherrypy)
    """
    if group == "high":
        psychoFile = "mTBI_rt.py" ## modify based on group
    elif group == "low":
        psychoFile = "mTBI_rt_placebo.py"
    if len(str(run)) > 2:   # run = 'Debug1' for 'runDebug1.xml'
        debug = '1'
    else:
        debug = '0'
    runNum = str(run)[-1]  # will produce the number either way

    stimArgs = [subject, str(visit), '00%s'%runNum, debug]
    return startPsycho(os.path.join(RTDIR, psychoFile), stimArgs, stimLog)


def checkPsychopyVersion(coderfile):
    """
    Explicitly check that a psychopy Coder mode stimulus program was
    generated from Builder mode using the same version of psychopy
    that is currently installed. 
    (1) We suggest that hand-generated Coder mode files include the
    psychopy version number on the proper line number in a comment.
    (2) Please update the line # here if Builder->Coder conversion changes.

    In: coderfile (str)
    Out: 'match' or 'mismatch' (str)
    """
    verline = getline(coderfile,4)  ## linecache.getline gets the line by number
    ver = re.search("v(\d+\.\d+\.\d+)",verline).group(1) ## grab the version number
    if ver != __version__:
        print "Psychopy version (%s) doesn't match the experiment (%s)!"%(__version__,ver)
        return 'mismatch'
    else:
        return 'match'
    

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


def writeFlots(subj, tab, run, timepoints=170, tr=2):
    ## NOTDONE tr and timepoints support
    ## NOTDONE empty file if not a realtime run
    ## NOTDONE numRtRuns should be a variable

    # prepare all lines to be written
    basedir = os.path.join('subjects', subj, 'session%s'%str(tab), 'data')
    updateAct = os.path.join(basedir, 'run00%s_active.json'%str(run))
    updateRef = os.path.join(basedir, 'run00%s_reference.json'%str(run))
    copy('template_active.json',os.path.join(os.path.expanduser('~/'),updateAct))
    copy('template_reference.json',os.path.join(os.path.expanduser('~/'),updateRef))

    RtRuns = 6
    fnName = 'onDataReceived'
    graphList = []
    for i in range(1, RtRuns+1):
        actFile = os.path.join(basedir, 'run00%s_active.json'%str(i))
        refFile = os.path.join(basedir, 'run00%s_reference.json'%str(i))
        fn = fnName + str(i)    
        if not i == int(run):
            graphList.append("    $.getJSON('" + actFile + "',{}, " + fn + ");\n")
            graphList.append("    $.getJSON('" + refFile + "',{}, " + fn + ");\n")
        
    # assemble outdata
    outdata = []
    outdata.append("                $('#rtcaption" + str(run) + "').text(jlen + ' TRs.');\n")
    ##outdata.append("                }\n")
    outdata.append("                $.plot($('#rtgraph" + str(run) + "'), [latest['active'], latest['reference']], options);\n")
    outdata.append("            }\n")
    outdata.append("            $.plot($('#rtgraph" + str(run) + "'), data, options); \n")
    outdata.append("            $.getJSON('" + updateAct + "',{}, " + fnName + ");\n")
    outdata.append("            $.getJSON('" + updateRef + "',{}, " + fnName + ");\n")
    outdata.append("            if (iteration < 70)\n")
    outdata.append("                setTimeout(fetchData, 5000);\n")
    outdata.append("            else {\n")
    outdata.append("                data = [];\n")
    outdata.append("            }\n")
    outdata.append("        }\n")
    outdata.append("        setTimeout(fetchData, 1000);\n")
    outdata.append("    });\n")
    outdata.extend(graphList)
    outdata.append("});\n")
    
    # write it all out!
    # copy contents of infile to outfile, then tack on what we just constructed
    with open('top_half_of_flot.txt','r') as infile:
        indata = infile.read()
    with open('flotmurfi.js','w') as outfile:
        outfile.write(indata)
        outfile.writelines(outdata)
        print "writeFlots: I THINK I WROTE A THING\n\n"
    return 


def glob_nodes(hierarchy,path):
   if not path.count('*') == 1:
       print path
       raise LookupError("glob_nodes: supports exactly one * index!")
   star = path.index('*')
   preStar = path[:star]
   postStar = ":".join(path[star+1:])  # pass as string to force path slice to be copied over during each call to get_node()
   preNode = get_node(hierarchy,preStar)
   if isinstance(preNode,list):
       if len(path) == star+1:
           return [i for i in preNode]
       else:
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
