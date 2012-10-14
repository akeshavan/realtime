#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.73.06), August 10, 2012, at 20:43
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
import sys
import getpass
#inputs: subject, visit#, session#

if len(sys.argv) != 5:

    raise Exception("USAGE: python mTBI_rt.py <Subject ID> <Visit #> <Session/Run#> <DEBUG: 1 for debug 0 otherwise>")

else:
    #store info about the experiment session
    print "In placebo mode!!!!!!!"
    expName='None'#from the Builder filename that created this script
    expInfo={'participant':sys.argv[1], 'session':sys.argv[3], "visit":sys.argv[2]}
    #dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
    #if dlg.OK==False: core.quit() #user pressed cancel
 
    debug = int(sys.argv[-1])

    expInfo['date']=data.getDateStr()#add a simple timestamp
    expInfo['expName']=expName

    base_directory = os.path.join('/home/%s/subjects/'%getpass.getuser(),expInfo['participant'],'session%s'%expInfo["visit"])
    if not os.path.exists(base_directory):
        raise Exception("Have you created the murfi directory?")

    #setup files for saving
    if not os.path.isdir(os.path.join(base_directory,'data')):
        os.makedirs(os.path.join(base_directory,'data')) #if this fails (e.g. permissions) we will get error
    filename=os.path.join(base_directory,'data') + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
    logFile=logging.LogFile(filename+'.log', level=logging.DEBUG)
    logging.console.setLevel(logging.WARNING)#this outputs to the screen, not a file

    #setup the Window and timings - depending on debug mode
    timings = {}

    if debug:
        print "IN DEBUG MODE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        win = visual.Window(size=[640, 512], fullscr=False, screen=0, allowGUI=True, allowStencil=False,
        monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb')
        timings["baseline"] = 30/2*0.5
        timings["stimulus"] = 14/2*0.5
        timings["question"] = 4/2*0.5
        timings["rest"] = 12/2*0.5
        timings["smileyface"] = 2/2*0.5
        timings["feedback"] = 2/2*0.5

    else:

        win = visual.Window(size=(1280, 1024), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                            monitor='testMonitor', color=[0,0,0], colorSpace='rgb')
        timings["baseline"] = 30
        timings["stimulus"] = 14
        timings["question"] = 4
        timings["rest"] = 12
        timings["smileyface"] = 2
        timings["feedback"] = 2 



    #Initialise components for routine:trigger
    triggerClock=core.Clock()
    text=visual.TextStim(win=win, ori=0, name='text',
        text='Waiting for scanner trigger ...',
        font='Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    condition_file = os.path.join(base_directory,'conditions/mTBIconditions%s.csv'%expInfo['session'][-1])

    #Initialise components for routine:baseline
    baselineClock=core.Clock()
    text_3=visual.TextStim(win=win, ori=0, name='text_3',
        text='Rest',
        font='Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    
    from scripts.graph_base import GraphBase
    from scripts.feedback import ThermBase, get_target, get_feedback
    from scripts.xmlparse import RT
    import numpy as np
    try:
        rt = RT(filename[:-5]+'_run_%s'%expInfo['session']+'.json')
    except:
        raise Exception("Have you started MURFI yet??")
    
    run_num = 1

    #Initialise components for routine:stimulus
    stimulusClock=core.Clock()
    patch=visual.PatchStim(win=win, name='patch',
        tex='sin', mask=None,
        ori=0, pos=[0, 0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1,
        texRes=128, interpolate=False, depth=0.0)
    text_5_fake=visual.TextStim(win=win, ori=0, name='text_5_fake',
        text='nonsense',
        font='Arial',
        pos=[0, 1], height=0.0,wrapWidth=None,
        color='grey', colorSpace='rgb', opacity=0,
        depth=-1.0)


    #Initialise components for routine:feedback
    feedbackClock=core.Clock()
    patch_2=visual.PatchStim(win=win, name='patch_2',
        tex='sin', mask=None,
        ori=0, pos=[0, 0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1.0,
        texRes=128, interpolate=False, depth=0.0)
    
    def extract(rt,dr,mask='active'):
        trials = np.asarray(rt.trial_type[mask])
        data = np.asarray(rt.data[mask])
        if (trials==dr).any():
            return data[trials==dr].tolist()
        else:
            return []


    #Initialise components for routine:stimulus
    stimulusClock=core.Clock()
    patch=visual.PatchStim(win=win, name='patch',
        tex='sin', mask=None,
        ori=0, pos=[0, 0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1,
        texRes=128, interpolate=False, depth=0.0)
    text_5_fake=visual.TextStim(win=win, ori=0, name='text_5_fake',
        text='nonsense',
        font='Arial',
        pos=[0, 1], height=0.0,wrapWidth=None,
        color='grey', colorSpace='rgb', opacity=0,
        depth=-1.0)


    #Initialise components for routine:question_maybe
    question_maybeClock=core.Clock()
    text_4=visual.TextStim(win=win, ori=0, name='text_4',
        text='nonsense',
        font='Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    rating=visual.RatingScale(win=win, name='rating', escapeKeys=['escape'], displaySizeFactor=1.00,
        pos=[0.0, -0.4], markerStart=False, leftKeys='1', rightKeys='2', scale=' ',acceptPreText='')

    #Initialise components for routine:smileyface
    smileyfaceClock=core.Clock()
    patch_5=visual.PatchStim(win=win, name='patch_5',
        tex='sin', mask=None,
        ori=0, pos=[0, 0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace='rgb', opacity=1.0,
        texRes=128, interpolate=False, depth=0.0)
    patch_3=visual.PatchStim(win=win, name='patch_3',
        tex=u'images/smiley_face.jpg', mask=None,
        ori=0, pos=[0, -0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        texRes=128, interpolate=False, depth=0.0)

    patch_4=visual.PatchStim(win=win, name='patch_4',
        tex=u'images/flat_face.jpg', mask=None,
        ori=0, pos=[0, -0.75], size=[0.25, 0.25], sf=None, phase=0.0,
        color=[1,1,1], colorSpace=u'rgb', opacity=1,
        texRes=128, interpolate=False, depth=0.0)

    text_5=visual.TextStim(win=win, ori=0, name='text_5',
        text=u'Rest',
        font=u'Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color=u'white', colorSpace=u'rgb', opacity=1.0,
        depth=-2.0)


    #Initialise components for routine:rest
    restClock=core.Clock()
    text_2=visual.TextStim(win=win, ori=0, name='text_2',
        text='nonsense',
        font='Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)


    #Initialise components for routine:end
    endClock=core.Clock()
    text_5_end=visual.TextStim(win=win, ori=0, name='text_5_end',
        text='Good Job!',
        font='Arial',
        pos=[0, 0.75], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=0.0)
    text_6=visual.TextStim(win=win, ori=0, name='text_6',
        text='nonsense',
        font='Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color='white', colorSpace='rgb', opacity=1,
        depth=-2.0)


    #Start of routine trigger
    t=0; triggerClock.reset()
    frameN=-1

    #update component parameters for each repeat
    key_resp_2 = event.BuilderKeyResponse() #create an object of type KeyResponse
    key_resp_2.status=NOT_STARTED

    #keep track of which have finished
    triggerComponents=[]#to keep track of which have finished
    triggerComponents.append(text)
    triggerComponents.append(key_resp_2)
    for thisComponent in triggerComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=triggerClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        
        #*text* updates
        if t>=0.0 and text.status==NOT_STARTED:
            #keep track of start time/frame for later
            text.tStart=t#underestimates by a little under one frame
            text.frameNStart=frameN#exact frame index
            text.setAutoDraw(True)
        
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
            theseKeys = event.getKeys(keyList=['plus', 'num_add'])
            if len(theseKeys)>0:#at least one key was pressed
                key_resp_2.keys=theseKeys[-1]#just the last key pressed
                key_resp_2.rt = key_resp_2.clock.getTime()
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


    #Start of routine baseline
    t=0; baselineClock.reset()
    frameN=-1

    #update component parameters for each repeat
    Feedbacks = {'up':[],'down':[]}
    Targets = {'up':[],'down':[]}
    Success = {'up':[],'down':[]}
    if expInfo['session']=='001':
        th = 0
        FB=0
    else:
        FB = 0
        run_num = int(expInfo['session'])
        foo = np.load(filename[:-5]+'_run_%03d'%(run_num-1)+'.npz')
        Feedbacks = foo["Feedbacks"].tolist()
        Targets = foo["Targets"].tolist()
        Success = foo["Success"].tolist()
    if expInfo['session'] == '006':
        FB = 0
    _window = (-4,-1)
    _target_window = -4
    FB=bool(FB)

    #keep track of which have finished
    baselineComponents=[]#to keep track of which have finished
    baselineComponents.append(text_3)
    for thisComponent in baselineComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=baselineClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        
        #*text_3* updates
        if t>=0.0 and text_3.status==NOT_STARTED:
            #keep track of start time/frame for later
            text_3.tStart=t#underestimates by a little under one frame
            text_3.frameNStart=frameN#exact frame index
            text_3.setAutoDraw(True)
        elif text_3.status==STARTED and t>=(0.0+timings["baseline"]):
            text_3.setAutoDraw(False)
        
        
        #check if all components have finished
        if not continueRoutine:
            break # lets a component forceEndRoutine
        continueRoutine=False#will revert to True if at least one component still running
        for thisComponent in baselineComponents:
            if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                continueRoutine=True; break#at least one component has not yet finished
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #end of routine baseline
    for thisComponent in baselineComponents:
        if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
    rt.check('baseline')

    #set up handler to look after randomisation of conditions etc
    trials=data.TrialHandler(nReps=1, method=u'sequential', 
        extraInfo=expInfo, originPath=None,
        trialList=data.importConditions(condition_file),
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
        
        #set up handler to look after randomisation of conditions etc
        trials_2=data.TrialHandler(nReps=1, method='random', 
            extraInfo=expInfo, originPath=None,
            trialList=[None],
            seed=None)
        thisTrial_2=trials_2.trialList[0]#so we can initialise stimuli with some values
        #abbreviate parameter names if possible (e.g. rgb=thisTrial_2.rgb)
        if thisTrial_2!=None:
            for paramName in thisTrial_2.keys():
                exec(paramName+'=thisTrial_2.'+paramName)
        
        for thisTrial_2 in trials_2:
            currentLoop = trials_2
            #abbrieviate parameter names if possible (e.g. rgb=thisTrial_2.rgb)
            if thisTrial_2!=None:
                for paramName in thisTrial_2.keys():
                    exec(paramName+'=thisTrial_2.'+paramName)
            
            #Start of routine stimulus
            t=0; stimulusClock.reset()
            frameN=-1
            
            #update component parameters for each repeat
            patch.setTex(image)
            text_5_fake.setText(arrow)
            
            #keep track of which have finished
            stimulusComponents=[]#to keep track of which have finished
            stimulusComponents.append(patch)
            stimulusComponents.append(text_5_fake)
            for thisComponent in stimulusComponents:
                if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
            #start the Routine
            continueRoutine=True
            while continueRoutine:
                #get current time
                t=stimulusClock.getTime()
                frameN=frameN+1#number of completed frames (so 0 in first frame)
                #update/draw components on each frame
                
                #*patch* updates
                if t>=0.0 and patch.status==NOT_STARTED:
                    #keep track of start time/frame for later
                    patch.tStart=t#underestimates by a little under one frame
                    patch.frameNStart=frameN#exact frame index
                    patch.setAutoDraw(True)
                elif patch.status==STARTED and t>=(0.0+timings["stimulus"]):
                    patch.setAutoDraw(False)
                
                #*text_5_fake* updates
                
                if t>=0.0 and text_5_fake.status==NOT_STARTED:
                    #keep track of start time/frame for later
                    text_5_fake.tStart=t#underestimates by a little under one frame
                    text_5_fake.frameNStart=frameN#exact frame index
                    text_5_fake.setAutoDraw(True)
                elif text_5_fake.status==STARTED and t>=(0.0+0.0):
                    text_5_fake.setAutoDraw(False)
                
                
                #check if all components have finished
                if not continueRoutine:
                    break # lets a component forceEndRoutine
                continueRoutine=False#will revert to True if at least one component still running
                for thisComponent in stimulusComponents:
                    if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                        continueRoutine=True; break#at least one component has not yet finished
                
                #check for quit (the [Esc] key)
                if event.getKeys(["escape"]): core.quit()
                #refresh the screen
                if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #end of routine stimulus
            for thisComponent in stimulusComponents:
                if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
            rt.check(arrow)
            
            #Start of routine feedback
	    print "======================STARTING ROUTINE FEEDBACK======================="
            t=0; feedbackClock.reset()
            frameN=-1
            
            #update component parameters for each repeat
            patch_2.setOpacity(1)
            patch_2.setTex(image)
            rtdata = rt.check(arrow)[0]
            fb = get_feedback(rt,arrow,7)
            Feedbacks[arrow].append(fb)
            
            if not expInfo['session']=='001':
                th = get_target(Feedbacks,arrow)
            Targets[arrow].append(th)    
            #keep track of which have finished
            feedbackComponents=[]#to keep track of which have finished
            feedbackComponents.append(patch_2)
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
            #start the Routine
            continueRoutine=True
            while continueRoutine:
                #get current time
                t=feedbackClock.getTime()
                frameN=frameN+1#number of completed frames (so 0 in first frame)
                #update/draw components on each frame
                
                #*patch_2* updates
                if t>=0.0 and patch_2.status==NOT_STARTED:
                    #keep track of start time/frame for later
                    patch_2.tStart=t#underestimates by a little under one frame
                    patch_2.frameNStart=frameN#exact frame index
                    patch_2.setAutoDraw(True)
                elif patch_2.status==STARTED and t>=(0.0+2.0):
                    patch_2.setAutoDraw(False)
                t = ThermBase(win, [0.25,1],[-0.125,-0.5])
                if FB:
                    t.plot(fb,th,arrow,frameN)
                t.draw()
                
                #check if all components have finished
                if not continueRoutine:
                    break # lets a component forceEndRoutine
                continueRoutine=False#will revert to True if at least one component still running
                for thisComponent in feedbackComponents:
                    if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                        continueRoutine=True; break#at least one component has not yet finished
                
                #check for quit (the [Esc] key)
                if event.getKeys(["escape"]): core.quit()
                #refresh the screen
                if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #end of routine feedback
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
            rt.check(arrow+'_fb')
        
        #completed 1 repeats of 'trials_2'
        
        #get names of stimulus parameters
        if trials_2.trialList in ([], [None], None):  params=[]
        else:  params = trials_2.trialList[0].keys()
        #save data for this loop
        trials_2.saveAsPickle(filename+'trials_2')
        trials_2.saveAsExcel(filename+'.xlsx', sheetName='trials_2',
            stimOut=params,
            dataOut=['n','all_mean','all_std', 'all_raw'])
        
        #Start of routine stimulus
        t=0; stimulusClock.reset()
        frameN=-1
        
        #update component parameters for each repeat
        patch.setTex(image)
        text_5_fake.setText(arrow)
        
        #keep track of which have finished
        stimulusComponents=[]#to keep track of which have finished
        stimulusComponents.append(patch)
        stimulusComponents.append(text_5_fake)
        for thisComponent in stimulusComponents:
            if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
        #start the Routine
        continueRoutine=True
        while continueRoutine:
            #get current time
            t=stimulusClock.getTime()
            frameN=frameN+1#number of completed frames (so 0 in first frame)
            #update/draw components on each frame
            
            #*patch* updates
            if t>=0.0 and patch.status==NOT_STARTED:
                #keep track of start time/frame for later
                patch.tStart=t#underestimates by a little under one frame
                patch.frameNStart=frameN#exact frame index
                patch.setAutoDraw(True)
            elif patch.status==STARTED and t>=(0.0+timings["stimulus"]):
                patch.setAutoDraw(False)
            
            #*text_5_fake* updates
            
            if t>=0.0 and text_5_fake.status==NOT_STARTED:
                #keep track of start time/frame for later
                text_5_fake.tStart=t#underestimates by a little under one frame
                text_5_fake.frameNStart=frameN#exact frame index
                text_5_fake.setAutoDraw(True)
            elif text_5_fake.status==STARTED and t>=(0.0+0.0):
                text_5_fake.setAutoDraw(False)
            
            
            #check if all components have finished
            if not continueRoutine:
                break # lets a component forceEndRoutine
            continueRoutine=False#will revert to True if at least one component still running
            for thisComponent in stimulusComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            
            #check for quit (the [Esc] key)
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #end of routine stimulus
        for thisComponent in stimulusComponents:
            if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
        rt.check(arrow)
        
        #Start of routine question_maybe
        t=0; question_maybeClock.reset()
        frameN=-1
        
        #update component parameters for each repeat
        text_4.setText(q_or_r)
        rating.reset()
        rating.status = NOT_STARTED
        keys_ever_pressed = False
        #keep track of which have finished
        question_maybeComponents=[]#to keep track of which have finished
        question_maybeComponents.append(text_4)
        for thisComponent in question_maybeComponents:
            if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
        #start the Routine
        continueRoutine=True
        while continueRoutine:
            #get current time
            t=question_maybeClock.getTime()
            frameN=frameN+1#number of completed frames (so 0 in first frame)
            #update/draw components on each frame
            
            #*text_4* updates
            if t>=0.0 and text_4.status==NOT_STARTED:
                #keep track of start time/frame for later
                text_4.tStart=t#underestimates by a little under one frame
                text_4.frameNStart=frameN#exact frame index
                text_4.setAutoDraw(True)
            elif text_4.status==STARTED and t>=(0.0+timings["question"]):
                text_4.setAutoDraw(False)
            if not q_or_r =='Rest':
                if not keys_ever_pressed:
                    keys = event.getKeys()
                    if len(keys)>0:
                        rating.setMarkerPos(3)
                        keys_ever_pressed=True
                rating.draw()
                if rating.noResponse == False:
                    rating.status = FINISHED
                    rating.response = rating.getRating()
                    rating.rt = rating.getRT()
            
            #check if all components have finished
            if not continueRoutine:
                break # lets a component forceEndRoutine
            continueRoutine=False#will revert to True if at least one component still running
            for thisComponent in question_maybeComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            
            #check for quit (the [Esc] key)
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #end of routine question_maybe
        for thisComponent in question_maybeComponents:
            if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
        if q_or_r=='Rest':
            rt.check('rest')
        else:
            rt.check(q_or_r)
        trials.addData('rating.rt', rating.markerPlacedAt)

        #Start of routine smileyface
        t=0; smileyfaceClock.reset()
        frameN=-1
        
        #update component parameters for each repeat
        patch_5.setOpacity(FB)
        patch_5.setTex(image)
        rtdata = rt.check(arrow)[0]
        fb = get_feedback(rt,arrow,14)
        Feedbacks[arrow].append(fb)
        Targets[arrow].append(th)
        if (arrow=="down" and fb < th) or (arrow=="up" and fb > th): 
            Success[arrow].append(1)
        else:
            Success[arrow].append(0)
        #keep track of which have finished
        smileyfaceComponents=[]#to keep track of which have finished
        smileyfaceComponents.append(patch_5)
        for thisComponent in smileyfaceComponents:
            if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
        #start the Routine
        continueRoutine=True
        while continueRoutine:
            #get current time
            t=smileyfaceClock.getTime()
            frameN=frameN+1#number of completed frames (so 0 in first frame)
            #update/draw components on each frame
            
            #*patch_5* updates
            if t>=0.0 and patch_5.status==NOT_STARTED:
                #keep track of start time/frame for later
                patch_5.tStart=t#underestimates by a little under one frame
                patch_5.frameNStart=frameN#exact frame index
                patch_5.setAutoDraw(True)
            elif patch_5.status==STARTED and t>=(0.0+timings["smileyface"]):
                patch_5.setAutoDraw(False)
            #if (fb>th and arrow=='up' and FB) or (fb<th and arrow == 'down' and FB):
            #    patch_3.draw()
                
            #elif (fb<th and arrow=='up' and FB) or (fb>th and arrow=='down' and FB):
            #    patch_4.draw()
            
            t = ThermBase(win, [0.25,1],[-0.125,-0.5])
            if FB:
                pass
                #t.plot(fb,th,arrow,frameN)
                #t.draw()
            else:
                text_5.draw()
            
            #check if all components have finished
            if not continueRoutine:
                break # lets a component forceEndRoutine
            continueRoutine=False#will revert to True if at least one component still running
            for thisComponent in smileyfaceComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            
            #check for quit (the [Esc] key)
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #end of routine smileyface
        for thisComponent in smileyfaceComponents:
            if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
        rt.check(arrow+'_smile_fb')
        
        #Start of routine rest
        t=0; restClock.reset()
        frameN=-1
        
        #update component parameters for each repeat
        text_2.setText('Rest')
        
        #keep track of which have finished
        restComponents=[]#to keep track of which have finished
        restComponents.append(text_2)
        for thisComponent in restComponents:
            if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
        #start the Routine
        continueRoutine=True
        while continueRoutine:
            #get current time
            t=restClock.getTime()
            frameN=frameN+1#number of completed frames (so 0 in first frame)
            #update/draw components on each frame
            
            #*text_2* updates
            if t>=0.0 and text_2.status==NOT_STARTED:
                #keep track of start time/frame for later
                text_2.tStart=t#underestimates by a little under one frame
                text_2.frameNStart=frameN#exact frame index
                text_2.setAutoDraw(True)
            elif text_2.status==STARTED and t>=(0.0+timings["rest"]):
                text_2.setAutoDraw(False)
            
            
            #check if all components have finished
            if not continueRoutine:
                break # lets a component forceEndRoutine
            continueRoutine=False#will revert to True if at least one component still running
            for thisComponent in restComponents:
                if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                    continueRoutine=True; break#at least one component has not yet finished
            
            #check for quit (the [Esc] key)
            if event.getKeys(["escape"]): core.quit()
            #refresh the screen
            if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #end of routine rest
        for thisComponent in restComponents:
            if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
        rt.check('rest')

    #completed 1 repeats of 'trials'

    #get names of stimulus parameters
    if trials.trialList in ([], [None], None):  params=[]
    else:  params = trials.trialList[0].keys()
    #save data for this loop
    trials.saveAsPickle(filename+'trials')
    trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])

    #Start of routine end
    t=0; endClock.reset()
    frameN=-1

    #update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse() #create an object of type KeyResponse
    key_resp_3.status=NOT_STARTED
    text_6.setText(run_num)
    rt.save(filename[:-5]+'_run_%s'%expInfo['session']+'.npz',Feedbacks,Targets,Success)
    rt.close()

    def get_bars(arrow):
        S = Success[arrow]
        v = []
        for i in xrange(int(len(S)/3)):
            v.append(sum(S[3*i:3*i+3]))
        print v
        return v
    
    downgraph = GraphBase(win,size=[0.75,0.5], pos=[0.2, 0],maxrange=[0,3])
    upgraph = GraphBase(win,size=[0.75,0.5], pos=[-0.8,0],maxrange=[0,3])
    upgraph.bar(get_bars('up'),abs_minmax=[0,100])
    downgraph.bar(get_bars('down'),abs_minmax=[0,100])
    upgraph.add_title('Successful Ups',0.075)
    downgraph.add_title('Successful Downs',0.075)

    #keep track of which have finished
    endComponents=[]#to keep track of which have finished
    endComponents.append(text_5_end)
    endComponents.append(key_resp_3)
    endComponents.append(text_6)
    for thisComponent in endComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=endClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        #*text_5_end* updates
        if not expInfo["session"] == '001': 
            upgraph.draw()
            downgraph.draw()
        if t>=0.0 and text_5_end.status==NOT_STARTED:
            #keep track of start time/frame for later
            text_5_end.tStart=t#underestimates by a little under one frame
            text_5_end.frameNStart=frameN#exact frame index
            text_5_end.setAutoDraw(True)
        
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
            theseKeys = event.getKeys(keyList=['y', 'n', 'left', 'right', 'space'])
            if len(theseKeys)>0:#at least one key was pressed
                key_resp_3.keys=theseKeys[-1]#just the last key pressed
                key_resp_3.rt = key_resp_3.clock.getTime()
                #abort routine on response
                continueRoutine=False
        
        #*text_6* updates 
        
        if t>=0.0 and text_6.status==NOT_STARTED:
            #keep track of start time/frame for later
            text_6.tStart=t#underestimates by a little under one frame
            text_6.frameNStart=frameN#exact frame index
            text_6.setAutoDraw(True)
        elif text_6.status==STARTED and t>=(0.0+1.0):
            text_6.setAutoDraw(False)
        
        
        #check if all components have finished
        if not continueRoutine:
            break # lets a component forceEndRoutine
        continueRoutine=False#will revert to True if at least one component still running
        for thisComponent in endComponents:
            if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                continueRoutine=True; break#at least one component has not yet finished
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #end of routine end
    for thisComponent in endComponents:
        if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)







    




    #Shutting down:
    win.close()
    core.quit()
