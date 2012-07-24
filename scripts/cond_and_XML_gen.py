##############################################
### cond_and_XML_gen.py
### sasen@mit.edu   (created 2012-07-23)
###
### Workflow: Before using psychopy or murfi, run this script to
### auto-generate condition_files (for psychopy) and XML run config
### files (for murfi).
###
### Currently set up for audio attention control neurofeedback
### experiments.

import numpy as np
import csv

### global vars ... should probably be options?
fileName_base = "../conditions/autoRTconditions"
header_row_titles = ["arrow","image","q_or_r"]
up_arrow_img_filename = "images/up.jpg"
down_arrow_img_filename = "images/down.jpg"
qtext = ["Rate your ability to control your brain activation at this time.","Rate your ability to concentrate at this time.","Rate how much you relied on your strategy during this trial.","Rest."]

## the 4 possible stimuli for this experiment.
## -- 1=up, 0=down
## -- all 4 used for FB. rows 1&2 are also noFB, runs 1&6 respectively
## -- question vectors are associated with stimulus vectors. 
stimuli = [[1,1,0,1,0,0],
           [0,1,1,0,0,1],
           [0,0,1,0,1,1],
           [1,0,0,1,1,0]]
questions = [[1,3,2,4,1,3],   # see question text above
             [2,1,3,4,2,4],
             [1,3,2,4,1,3],
             [2,1,3,4,2,4]]
### this is for checking question counterbalancing!
## sq = np.zeros([4,2])  

numRuns=6
for r in range(0,numRuns):
    ## check for feedback
    if r in [0,numRuns-1]:
        fb_run = 0   ## first or last is NOT a feedback run
    else:
        fb_run = 1   ## feedback run
    ###  runNum = r  # zero-indexed
    runNum = r+1   # one-indexed
    # row lookup is (r mod 4) because rows 1 & 2 are repeated in runs 5 & 6
    # ERRR all my comments have one-indexed row #s. sorry.
    stimulusVec = stimuli[r%4]
    questionVec = questions[r%4]

    with open(fileName_base+'%d.csv'%runNum, 'wb') as csv_fileh:
        csvFileWriter = csv.writer(csv_fileh)
        csvFileWriter.writerow(header_row_titles)
        
        for i in range(len(stimulusVec)):
            if stimulusVec[i]:
                dirtext = 'up'
                img = up_arrow_img_filename
##                if fb_run:
##                    sq[questionVec[i]-1][1] += 1
            else:
                dirtext = 'down'
                img = down_arrow_img_filename
##                if fb_run:
##                    sq[questionVec[i]-1][0] += 1
        ## </for>
            csvFileWriter.writerow([dirtext, img, qtext[questionVec[i]-1]]) 
        csv_fileh.close()
        ## </with>

## </for> outmost!


   
### condition_file = 'conditions/mTBIconditions%s.xlsx'%expInfo['session'][-1]

#set up handler to look after randomisation of conditions etc               
# trials=data.TrialHandler(nReps=1, method='sequential',
#     extraInfo=expInfo, originPath=None,
#     trialList=data.importConditions(condition_file),
#     seed=None)


#### I SUGGEST WE MAKE ANOTHER TRIAL LOOP for feedback vs. no feedback. Then we can let method='random' permute the run order for us. Well... or something.

