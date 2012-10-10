#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.73.06), August 23, 2012, at 09:57
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division #so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import * #things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
"""
#store info about the experiment session
expName='ButtonTest'#from the Builder filename that created this script
expInfo={'participant':'', 'session':'001'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file
"""
#setup the Window
win = visual.Window(size=(1280, 1024), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:trial
trialClock=core.Clock()
text=visual.TextStim(win=win, ori=0, name='text',
    text=u'Press 1 key',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:next_key
next_keyClock=core.Clock()
text_2=visual.TextStim(win=win, ori=0, name='text_2',
    text=u'Press 2 key',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:thanks
thanksClock=core.Clock()
text_3=visual.TextStim(win=win, ori=0, name='text_3',
    text=u'Button box works!',
    font=u'Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)

#Start of routine trial
t=0; trialClock.reset()
frameN=-1

#update component parameters for each repeat
key_resp = event.BuilderKeyResponse() #create an object of type KeyResponse
key_resp.status=NOT_STARTED
#keep track of which have finished
trialComponents=[]#to keep track of which have finished
trialComponents.append(text)
trialComponents.append(key_resp)
for thisComponent in trialComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=trialClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*text* updates
    if t>=0.0 and text.status==NOT_STARTED:
        #keep track of start time/frame for later
        text.tStart=t#underestimates by a little under one frame
        text.frameNStart=frameN#exact frame index
        text.setAutoDraw(True)
    
    #*key_resp* updates
    if t>=0.0 and key_resp.status==NOT_STARTED:
        #keep track of start time/frame for later
        key_resp.tStart=t#underestimates by a little under one frame
        key_resp.frameNStart=frameN#exact frame index
        key_resp.status=STARTED
        #keyboard checking is just starting
        key_resp.clock.reset() # now t=0
        event.clearEvents()
    if key_resp.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys(keyList=['1'])
        if len(theseKeys)>0:#at least one key was pressed
            key_resp.keys=theseKeys[-1]#just the last key pressed
            key_resp.rt = key_resp.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in trialComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine trial
for thisComponent in trialComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Start of routine next_key
t=0; next_keyClock.reset()
frameN=-1

#update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse() #create an object of type KeyResponse
key_resp_2.status=NOT_STARTED
#keep track of which have finished
next_keyComponents=[]#to keep track of which have finished
next_keyComponents.append(text_2)
next_keyComponents.append(key_resp_2)
for thisComponent in next_keyComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=next_keyClock.getTime()
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
        theseKeys = event.getKeys(keyList=['2'])
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_2.keys=theseKeys[-1]#just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in next_keyComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine next_key
for thisComponent in next_keyComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Start of routine thanks
t=0; thanksClock.reset()
frameN=-1

#update component parameters for each repeat
key_resp_3 = event.BuilderKeyResponse() #create an object of type KeyResponse
key_resp_3.status=NOT_STARTED
#keep track of which have finished
thanksComponents=[]#to keep track of which have finished
thanksComponents.append(text_3)
thanksComponents.append(key_resp_3)
for thisComponent in thanksComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=thanksClock.getTime()
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
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_3.keys=theseKeys[-1]#just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine thanks
for thisComponent in thanksComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Shutting down:
win.close()
core.quit()
