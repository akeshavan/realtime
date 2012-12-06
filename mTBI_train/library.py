import os, re
import getpass
import subprocess
from glob import glob 
import json
import sys
from psychopy import __version__
from linecache import getline

HOME = os.path.abspath('.')
RTDIR = os.path.abspath('../localXfer')
RTSCRIPTSDIR = os.path.abspath('../')
SUBJS = os.path.abspath("/home/%s/subjects/"%getpass.getuser())

def localizer():
    os.chdir(RTDIR)
    a = ["python", "Practice_Bird1back.py"]
    print a
    foo = subprocess.Popen(a)
    os.chdir(HOME)

def transfer1():
    os.chdir(RTDIR)
    a = ["python", "Practice_Letter1back.py"]
    print a
    foo = subprocess.Popen(a)
    os.chdir(HOME)

def transfer2():
    os.chdir(RTDIR)
    a = ["python", "Practice_Letter2back.py"]
    print a
    foo = subprocess.Popen(a)
    os.chdir(HOME)

def rtActive():
    #os.chdir('..')
    a = ["python", "mTBI_rt_train.py"]
    print a
    foo = subprocess.Popen(a)
    #os.chdir(HOME)

def rtPassive():
    #os.chdir('..')
    a = ["python", "mTBI_rt_train_placebo.py"]
    print a
    foo = subprocess.Popen(a)
    #os.chdir(HOME)

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

def completeVisit(self,coord):
    loc = int(coord.split('.')[0])
    visit = self.json["Protocol"][loc]
    visit["complete"] = True



