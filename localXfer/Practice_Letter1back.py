#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.73.06), August 10, 2012, at 13:12
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
#if len(sys.argv) != 4:
#    raise Exception("USAGE: python Letter_1back.py <SubjectID> <Visit#> <Timestamp>")
#else:
expName='PracticeLetter1back'
expInfo={'expName':expName, 'subjID':'train', 'visit':0, 'date':''}

#setup files for saving
base_directory = os.path.join(os.path.expanduser('~/subjects/'),expInfo['subjID'],'session%s'%expInfo['visit'],'ltTaskData',expName)

if not os.path.isdir(base_directory):
    os.makedirs(base_directory)
filename = os.path.join(base_directory,expName+expInfo['date'])
logFile=logging.LogFile(filename+'.log', level=logging.INFO)
logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

#setup the Window
win = visual.Window(size=(640, 480), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=u'black', colorSpace=u'rgb')

#Initialise components for routine:hello1
hello1Clock=core.Clock()
hello_hello=visual.TextStim(win=win, ori=0, name='hello_hello',
    text='Please press the button when you are ready.',
    font='Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
instruction1=visual.TextStim(win=win, ori=0, name='instruction1',
    text=u'You will be presented with a sequence of letter sounds over headphones and with a sequence of geometric pictures on the screen.\n\nYou either focus on the screen, the sound, or on both at the same time. Whether you have to focus on the sound, the screen or on both is indicated by icons on the screen:',
    font=u'Arial',
    pos=[0, 0.5], height=0.06,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=0.0)
instruction2=visual.TextStim(win=win, ori=0, name='instruction2',
    text=u'Compare the current sound/picture to one presented prior to the current one in the sequence. If the current and the previous sound/picture are identical you press the left button with your index finger as quickly as possible. \n\nExample:',
    font=u'Arial',
    pos=[0, -0.25], height=0.06,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=-1.0)
earpic=visual.PatchStim(win=win, name='earpic',
    tex=u'Stimuli/ear_def.bmp', mask=None,
    ori=0, pos=[-0.15, 0.14], size=[0.12, 0.15], sf=None, phase=0.0,
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    texRes=128, interpolate=False, depth=-2.0)
eyepic=visual.PatchStim(win=win, name='eyepic',
    tex=u'Stimuli/eye_def.bmp', mask=None,
    ori=0, pos=[0.15, .15], size=[0.2, 0.15], sf=None, phase=0.0,
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    texRes=128, interpolate=False, depth=-3.0)
birdspic=visual.PatchStim(win=win, name='birdspic',
    tex=u'Stimuli/task1_transfer.png', mask=None,
    ori=0, pos=[0, -0.5], size=[0.4, 0.1], sf=None, phase=0.0,
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    texRes=128, interpolate=False, depth=-4.0)
instruction3=visual.TextStim(win=win, ori=0, name='instruction3',
    text=u'Press the button after the fourth picture',
    font=u'Arial',
    pos=[0, -0.65], height=0.05,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=-5.0)
instruction4=visual.TextStim(win=win, ori=0, name='instruction4',
    text=u'Please press the button when you are ready',
    font=u'Arial',
    pos=[0, -0.8], height=0.06,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=-6.0)


#Initialise components for routine:hello
helloClock=core.Clock()
get_ready=visual.TextStim(win=win, ori=0, name='get_ready',
    text='Get ready to begin!',
    font='Arial',
    pos=[0, 0], height=0.15,wrapWidth=None,
    color=[0.5,0.5,0.5], colorSpace='rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:trial
trialClock=core.Clock()

task=visual.PatchStim(win=win, name='task',
    tex='sin', mask=None,
    ori=0, pos=[0, 0.75], size=[0.5, 0.5], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    texRes=128, interpolate=False, depth=-1.0)

show_visual=visual.PatchStim(win=win, name='show_visual',units='pix', 
    tex='sin', mask=None,
    ori=0, pos=[0, 0], size=[600, 440], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    texRes=128, interpolate=False, depth=-1.0)

background=visual.PatchStim(win=win, name='background',units='pix', 
    tex=os.path.abspath('./Stimuli/spa/background.bmp'), mask=None,
    ori=0, pos=[0, 0], size=[600, 440], sf=None, phase=0.0,
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    texRes=128, interpolate=False, depth=-1.0)

rest1=visual.TextStim(win=win, ori=0, name='Rest',
    text=u'Rest',
    font=u'Arial',
    pos=[0, 0.75], height=0.1,wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=-6.0)

    
play_sound=sound.Sound('A',)
play_sound.setVolume(1.0)

#Initialise components for routine:goodbye
goodbyeClock=core.Clock()
text_2=visual.TextStim(win=win, ori=0, name='text_2',
    text='Good job!',
    font='Arial',
    pos=[0, 0], height=0.15,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

#Start of routine hello1
t=0; hello1Clock.reset()
frameN=-1

#update component parameters for each repeat
proceed_key = event.BuilderKeyResponse() #create an object of type KeyResponse
proceed_key.status=NOT_STARTED
#keep track of which have finished
hello1Components=[]#to keep track of which have finished
hello1Components.append(instruction1)
hello1Components.append(instruction2)
hello1Components.append(instruction3)
hello1Components.append(instruction4)
hello1Components.append(eyepic)
hello1Components.append(earpic)
hello1Components.append(birdspic)
hello1Components.append(proceed_key)
for thisComponent in hello1Components:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=hello1Clock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    if t>=0.0 and instruction1.status==NOT_STARTED:
        #keep track of start time/frame for later
        instruction1.tStart=t#underestimates by a little under one frame
        instruction1.frameNStart=frameN#exact frame index
        instruction1.setAutoDraw(True)
   
    if t>=0.0 and instruction2.status==NOT_STARTED:
        #keep track of start time/frame for later
        instruction2.tStart=t#underestimates by a little under one frame
        instruction2.frameNStart=frameN#exact frame index
        instruction2.setAutoDraw(True)
        
    if t>=0.0 and instruction3.status==NOT_STARTED:
        #keep track of start time/frame for later
        instruction3.tStart=t#underestimates by a little under one frame
        instruction3.frameNStart=frameN#exact frame index
        instruction3.setAutoDraw(True)
        
    if t>=0.0 and instruction4.status==NOT_STARTED:
        #keep track of start time/frame for later
        instruction4.tStart=t#underestimates by a little under one frame
        instruction4.frameNStart=frameN#exact frame index
        instruction4.setAutoDraw(True)
        
    if t>=0.0 and eyepic.status==NOT_STARTED:
        #keep track of start time/frame for later
        eyepic.tStart=t#underestimates by a little under one frame
        eyepic.frameNStart=frameN#exact frame index
        eyepic.setAutoDraw(True)
        
    if t>=0.0 and earpic.status==NOT_STARTED:
        #keep track of start time/frame for later
        earpic.tStart=t#underestimates by a little under one frame
        earpic.frameNStart=frameN#exact frame index
        earpic.setAutoDraw(True)
        
    if t>=0.0 and birdspic.status==NOT_STARTED:
        #keep track of start time/frame for later
        birdspic.tStart=t#underestimates by a little under one frame
        birdspic.frameNStart=frameN#exact frame index
        birdspic.setAutoDraw(True)
   
    #*proceed_key* updates
    if t>=0.0 and proceed_key.status==NOT_STARTED:
        #keep track of start time/frame for later
        proceed_key.tStart=t#underestimates by a little under one frame
        proceed_key.frameNStart=frameN#exact frame index
        proceed_key.status=STARTED
        #keyboard checking is just starting
        proceed_key.clock.reset() # now t=0
        event.clearEvents()
    if proceed_key.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys(keyList=['b', '1'])
        if len(theseKeys)>0:#at least one key was pressed
            proceed_key.keys=theseKeys[-1]#just the last key pressed
            proceed_key.rt = proceed_key.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in hello1Components:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine hello1
for thisComponent in hello1Components:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Start of routine hello
t=0; helloClock.reset()
frameN=-1

#update component parameters for each repeat
start_expt = event.BuilderKeyResponse() #create an object of type KeyResponse
start_expt.status=NOT_STARTED
#keep track of which have finished
helloComponents=[]#to keep track of which have finished
helloComponents.append(get_ready)
helloComponents.append(start_expt)
for thisComponent in helloComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=helloClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*get_ready* updates
    if t>=0.0 and get_ready.status==NOT_STARTED:
        #keep track of start time/frame for later
        get_ready.tStart=t#underestimates by a little under one frame
        get_ready.frameNStart=frameN#exact frame index
        get_ready.setAutoDraw(True)
    
    #*start_expt* updates
    if t>=0.0 and start_expt.status==NOT_STARTED:
        #keep track of start time/frame for later
        start_expt.tStart=t#underestimates by a little under one frame
        start_expt.frameNStart=frameN#exact frame index
        start_expt.status=STARTED
        #keyboard checking is just starting
        start_expt.clock.reset() # now t=0
    if start_expt.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys(keyList=['t', '+', 'plus', 'num_add','5', '6'])
        if len(theseKeys)>0:#at least one key was pressed
            start_expt.keys.extend(theseKeys)#storing all keys
            start_expt.rt.append(start_expt.clock.getTime())
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in helloComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine hello
for thisComponent in helloComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#set up handler to look after randomisation of conditions etc
trials=data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions('Run-Designs/practice_new_letter_nback1.xlsx'),
    seed=None)
thisTrial=trials.trialList[0]#so we can initialise stimuli with some values
#abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial!=None:
    for paramName in thisTrial.keys():
        exec(paramName+'=thisTrial.'+paramName)

for thisTrial in trials:
    currentLoop = trials
    #abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial!=None:
        for paramName in thisTrial.keys():
            exec(paramName+'=thisTrial.'+paramName)
    
    #Start of routine trial
    t=0; trialClock.reset()
    frameN=-1
    
    #update component parameters for each repeat
    task.setOpacity(1)
    if condition == 'AUDIO':
        task.setTex(os.path.abspath("./Stimuli/ear_def.bmp"))
    elif condition == 'VISUAL':
        task.setTex(os.path.abspath("./Stimuli/eye_def.bmp"))
    elif condition == "AUDIO-VISUAL":
        task.setTex(os.path.abspath("./Stimuli/ear_eye.bmp"))
    elif condition == 'REST':
        task.setOpacity(0)

    show_visual.setOpacity(showprompt)
    show_visual.setTex(os.path.abspath("./Stimuli/spa/%s.bmp"%(visuall)))
    play_sound.setSound(os.path.abspath("./Stimuli/%s/normalized/letter%s.wav"%(sounddir,audioo)))
    play_sound.setVolume(showprompt)
    trial_resp = event.BuilderKeyResponse() #create an object of type KeyResponse
    trial_resp.status=NOT_STARTED
    #keep track of which have finished
    trialComponents=[]#to keep track of which have finished
    trialComponents.append(task)
    trialComponents.append(show_visual)
    trialComponents.append(play_sound)
    trialComponents.append(trial_resp)
    for thisComponent in trialComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=trialClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        if not condition == "REST":
            background.draw() 
        else:
            rest1.draw()
        #*task* updates
        if t>=0.0 and task.status==NOT_STARTED:
            #keep track of start time/frame for later
            task.tStart=t#underestimates by a little under one frame
            task.frameNStart=frameN#exact frame index
            task.setAutoDraw(True)
        elif task.status==STARTED and t>=(0.0+1.4):
            task.setAutoDraw(False)
        
        #*show_visual* updates
        if t>=0.0 and show_visual.status==NOT_STARTED:
            #keep track of start time/frame for later
            show_visual.tStart=t#underestimates by a little under one frame
            show_visual.frameNStart=frameN#exact frame index
            show_visual.setAutoDraw(True)
        elif show_visual.status==STARTED and t>=(0.0+1.2):
            show_visual.setAutoDraw(False)
        #start/stop play_sound
        if t>=0 and play_sound.status==NOT_STARTED:
            #keep track of start time/frame for later
            play_sound.tStart=t#underestimates by a little under one frame
            play_sound.frameNStart=frameN#exact frame index
            play_sound.play()#start the sound (it finishes automatically)
        elif play_sound.status==STARTED and t>=(0+1.4):
            play_sound.stop()#stop the sound (if longer than duration)
        
        #*trial_resp* updates
        if t>=0.0 and trial_resp.status==NOT_STARTED:
            #keep track of start time/frame for later
            trial_resp.tStart=t#underestimates by a little under one frame
            trial_resp.frameNStart=frameN#exact frame index
            trial_resp.status=STARTED
            #keyboard checking is just starting
            trial_resp.clock.reset() # now t=0
        elif trial_resp.status==STARTED and t>=1.4:
            trial_resp.status=STOPPED
        if trial_resp.status==STARTED:#only update if being drawn
            theseKeys = event.getKeys(keyList=['b', '1'])
            if len(theseKeys)>0:#at least one key was pressed
                if trial_resp.keys==[]:#then this was the first keypress
                    trial_resp.keys=theseKeys[0]#just the first key pressed
                    trial_resp.rt = trial_resp.clock.getTime()
        
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
    #check responses
    if len(trial_resp.keys)==0: #No response was made
       trial_resp.keys=None
    #store data for trials (TrialHandler)
    trials.addData('trial_resp.keys',trial_resp.keys)
    if trial_resp.keys != None:#we had a response
        trials.addData('trial_resp.rt',trial_resp.rt)

#completed 1 repeats of 'trials'

#get names of stimulus parameters
if trials.trialList in ([], [None], None):  params=[]
else:  params = trials.trialList[0].keys()
#save data for this loop
trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
trials.saveAsText(filename+'trials.csv', delim=',',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

#Start of routine goodbye
t=0; goodbyeClock.reset()
frameN=-1

#update component parameters for each repeat
#keep track of which have finished
goodbyeComponents=[]#to keep track of which have finished
goodbyeComponents.append(text_2)
for thisComponent in goodbyeComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=goodbyeClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*text_2* updates
    if t>=0.0 and text_2.status==NOT_STARTED:
        #keep track of start time/frame for later
        text_2.tStart=t#underestimates by a little under one frame
        text_2.frameNStart=frameN#exact frame index
        text_2.setAutoDraw(True)
    elif text_2.status==STARTED and t>=(0.0+2.0):
        text_2.setAutoDraw(False)
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in goodbyeComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine goodbye
for thisComponent in goodbyeComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#Shutting down:
win.close()
core.quit()
