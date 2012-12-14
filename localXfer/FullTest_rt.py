#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.73.06), October 04, 2012, at 11:14
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui, sound
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
import sys

#store info about the experiment session
if len(sys.argv) != 4:
    raise Exception("USAGE: python FullTest_rt.py <SubjectID> <Visit#> <Timestamp>")
else:
    expName='FullTest_rt'#from the Builder filename that created this script
    expInfo={'participant':sys.argv[1], 'session':sys.argv[2]}
    expInfo['date']=sys.argv[3]
    expInfo['expName']=expName

#setup files for saving
base_directory = os.path.join(os.path.expanduser('~/subjects/'),expInfo['participant'],'session%s'%expInfo['session'],'ltTaskData',expName)

if not os.path.isdir(base_directory):
    os.makedirs(base_directory)
filename = os.path.join(base_directory,expName+expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#setup the Window
win = visual.Window(size=(1280, 1024), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:start
startClock=core.Clock()
text_2=visual.TextStim(win=win, ori=0, name='text_2',
    text=u'Press a button to start setup',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:trigger
triggerClock=core.Clock()
text_3=visual.TextStim(win=win, ori=0, name='text_3',
    text=u'Testing scanner trigger...',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:ready
readyClock=core.Clock()
text_4=visual.TextStim(win=win, ori=0, name='text_4',
    text=u'Setup is complete!',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Start of routine start
t=0; startClock.reset()
frameN=-1

#update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse() #create an object of type KeyResponse
key_resp_2.status=NOT_STARTED
#keep track of which have finished
startComponents=[]#to keep track of which have finished
startComponents.append(text_2)
startComponents.append(key_resp_2)
for thisComponent in startComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=startClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*text_2* updates
    if t>=0.0 and text_2.status==NOT_STARTED:
        #keep track of start time/frame for later
        text_2.tStart=t#underestimates by a little under one frame
        text_2.frameNStart=frameN#exact frame index
        text_2.setAutoDraw(True)
    
    #*key_resp_2* updates
    if t>=0.0 and key_resp_2.status==NOT_STARTED:
        #keep track of start time/frame for later
        key_resp_2.tStart=t#underestimates by a little under one frame
        key_resp_2.frameNStart=frameN#exact frame index
        key_resp_2.status=STARTED
        #keyboard checking is just starting
        key_resp_2.clock.reset() # now t=0
        event.clearEvents()
    if key_resp_2.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys(keyList=['1', '2'])
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_2.keys=theseKeys[-1]#just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in startComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine start
for thisComponent in startComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#set up handler to look after randomisation of conditions etc
#Start of routine trigger
t=0; triggerClock.reset()
frameN=-1

#update component parameters for each repeat
key_resp_3 = event.BuilderKeyResponse() #create an object of type KeyResponse
key_resp_3.status=NOT_STARTED
#keep track of which have finished
triggerComponents=[]#to keep track of which have finished
triggerComponents.append(text_3)
triggerComponents.append(key_resp_3)
for thisComponent in triggerComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=triggerClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*text_3* updates
    if t>=0.0 and text_3.status==NOT_STARTED:
        #keep track of start time/frame for later
        text_3.tStart=t#underestimates by a little under one frame
        text_3.frameNStart=frameN#exact frame index
        text_3.setAutoDraw(True)
    
    #*key_resp_3* updates
    if t>=0.0 and key_resp_3.status==NOT_STARTED:
        #keep track of start time/frame for later
        key_resp_3.tStart=t#underestimates by a little under one frame
        key_resp_3.frameNStart=frameN#exact frame index
        key_resp_3.status=STARTED
        #keyboard checking is just starting
        key_resp_3.clock.reset() # now t=0
        event.clearEvents()
    if key_resp_3.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys(keyList=['plus', '+', 'num_add', '5', '6'])
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_3.keys=theseKeys[-1]#just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in triggerComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine trigger
for thisComponent in triggerComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Start of routine ready
t=0; readyClock.reset()
frameN=-1

#update component parameters for each repeat
#keep track of which have finished
readyComponents=[]#to keep track of which have finished
readyComponents.append(text_4)
for thisComponent in readyComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=readyClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*text_4* updates
    if t>=0.0 and text_4.status==NOT_STARTED:
        #keep track of start time/frame for later
        text_4.tStart=t#underestimates by a little under one frame
        text_4.frameNStart=frameN#exact frame index
        text_4.setAutoDraw(True)
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in readyComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine ready
for thisComponent in readyComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Shutting down:
win.close()
core.quit()
