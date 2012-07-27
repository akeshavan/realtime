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
import xml.etree.ElementTree as ET
import csv
import os.path
import nibabel.nifti1 as nib
import random
import re

### global vars ... should probably be options?
# randomStimOrder = True  
randomStimOrder = False  ## fixed stimulus order, good for testing
############## condition file globals!
fileName_base = "../conditions/mTBIconditions"
header_row_titles = ["arrow","image","q_or_r"]
up_arrow_img_filename = "images/up.jpg"
down_arrow_img_filename = "images/down.jpg"
qtext = ["Rate your ability to control your brain activation at this time.","Rate your ability to concentrate at this time.","Rate how much you relied on your strategy during this trial.","Rest."]
###############  XML file globals!
xmlDir = "./" ### "../murfi/fakedata/scripts/"
softwareDir = "/local/murfi/"   ###"~/software/murfi/"   ## murfi location
xmlInputName = xmlDir + "template.xml"  ## xmlDir + "run1.xml"
xmlName_base = xmlDir + "run"

## the 4 possible stimuli for this experiment.
## -- 1=up, 0=down
## -- the order will be permuted
## -- all 4 get used for FB. rows 1&2 are also noFB, runs 1&6 respectively
## -- question vectors are associated with stimulus vectors. 
stimuli = [[1,1,0,1,0,0],
           [0,1,1,0,0,1],
           [0,0,1,0,1,1],
           [1,0,0,1,1,0]]
questions = [[1,3,2,4,1,3],   # see question text above
             [2,1,3,4,2,4],
             [1,3,2,4,1,3],
             [2,1,3,4,2,4]]

########################## NO MORE USER-EDITABLE STUFF BELOW THIS POINT

########### DEFINE FUNCTIONS 
def matrixMaker(fb_run,stimulusVec,questionVec):
    # TRs= "        1 2 3 4 5 6 7 8 9101112131415161718192021222324"
    data = "        1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0"
    null = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    q123 = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0"
    #feedback runs (1 in varname means FB)
    fbk1 = "        0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0"
    # no feedback runs (0 in varname means noFB)
    fbk0 = "        0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    # rests for trials with questions
    rst1 = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1"
    rst0 = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1"
    # rests for trials where q4 = rest (_ in varname means q4=rest)
    rs_1 = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 1 1 1 1 1 1"
    rs_0 = "        0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1"

    if fb_run:
        feedback = [fbk1,fbk1,fbk1,fbk1,fbk1,fbk1]
    else:  ## not a feedback run
        feedback = [fbk0,fbk0,fbk0,fbk0,fbk0,fbk0]

    dataup = []
    datadown = []
    rest = []
    q1 = []
    q2 = []
    q3 = []
    for (s,q) in zip(stimulusVec,questionVec):
        if s:
            dataup.append(data)
            datadown.append(null)
        else:
            dataup.append(null)
            datadown.append(data)

        if q == 4:
            q1.append(null)
            q2.append(null)
            q3.append(null)
            if fb_run:
                rest.append(rs_1)
            else:
                rest.append(rs_0)
        else:
            if fb_run:
                rest.append(rst1)
            else:
                rest.append(rst0)
                
            if q == 1:
                q1.append(q123)
                q2.append(null)
                q3.append(null)
            elif q == 2:
                q1.append(null)
                q2.append(q123)
                q3.append(null)
            elif q == 3:
                q1.append(null)
                q2.append(null)
                q3.append(q123)

    #### this dict depends on the condition names!!!
    dictofMats = {'data-up': "\n"+"\n".join(dataup)+"\n      ",
                  'data-down':"\n"+"\n".join(datadown)+"\n      ",
                  'q1': "\n"+"\n".join(q1)+"\n      ",
                  'q2': "\n"+"\n".join(q2)+"\n      ",
                  'q3': "\n"+"\n".join(q3)+"\n      ",
                  'feedback': "\n"+"\n".join(feedback)+"\n      ",
                  'rest': "\n"+"\n".join(rest)+"\n      "}
    return dictofMats


################## DONE WITH FUNCTIONS, MAIN BODY FOLLOWS


### now permute the stimulus rows (and corresponding question rows)
if randomStimOrder:
    sq_zip = zip(stimuli,questions)
    random.shuffle(sq_zip)
    [stimPerm,questPerm] = zip(*sq_zip)
    stimuli = list(stimPerm)
    questions = list(questPerm)

### DEBUG: this is for checking question counterbalancing!
## sq = np.zeros([4,2])  

################### Step 1: Parse input murfi config XML file

## Step 1.1: open input file, add XML root, parse XML into etree
## i. currently cribbing off rtsmoking & the murfi example XML files.
## -- may eventually use a different input file
## ii. need root element because murfi doesn't like valid xml
## -- otherwise, we could've just use ET.parse(xmlInputName) !
## -- must strip root off during XML output creation 

inXMLfile = open(xmlInputName,'rb')
xmlStrings = inXMLfile.readlines()
inXMLfile.close()
xmlStrings.insert(1,'<root>\n')
xmlStrings.append('</root>\n')
inElement = ET.fromstringlist(xmlStrings)  # Element object
inET = ET.ElementTree(inElement)   # ElementTree object

## Step 1.2: Fix murfi softwareDir
## -- unnecessary once all users have the same directory structure
## -- or if we use environment vars in the input XML file.
inElement.find("study/option[@name='softwareDir']").text = softwareDir

## Step 1.3: verify roi and background/reference maskfiles
## -- could do some more error checking here
## -- could also take their names/locations as inputs

subjectsDir = xmlDir + inElement.find("study/option[@name='subjectsDir']").text.strip()
## ensure that subjectsDir matches the subject name
############# FINISHME

# for elem in inElement.findall("processor/module[@name='mask-load']"):
#     mask = subjectsDir + '/mask/'+ elem.find("option[@name='filename']").text.strip() + '.nii'
#     if os.path.isfile(mask):   ## verify that the file exists
#         mask_dtype = nib.Nifti1Image.load(mask).get_data_dtype()
#         if  mask_dtype == "int16":   ## murfi needs the short datatype, AKA int16
#             print "Found valid int16 nifti mask:" + mask
#         else:
#             print "ERROR in cond_and_XML_gen.py: mask data type is " + mask_dtype + ", should be int16!"
#             exit(1)
#     else:
#         print "ERROR in cond_and_XML_gen.py: could not find mask file " + mask
#         exit(1)

## Step 1.4: make sure all conditions have been created 
## -- i know, this should have better logic
## -- also, condition creation should be a function. but not today.
designNode = inElement.find("processor/module/design")  # this is the parent element
if not designNode.find("option[@conditionName='q2']"):
    q1Elem = designNode.find("option[@conditionName='q1']")
    q2Elem = ET.Element.copy(q1Elem)
    q2Elem.set('conditionName','q2')
    designNode.append(q2Elem)
if not designNode.find("option[@conditionName='q3']"):
    q1Elem = designNode.find("option[@conditionName='q1']")
    q3Elem = ET.Element.copy(q1Elem)
    q3Elem.set('conditionName','q3')
    designNode.append(q3Elem)

condNames = [c.get('conditionName') for c in designNode.findall("option[@conditionName]")]   # complete list of condition name keys

## Step 1.??? TODO
## i. let scanner/option->name=port be settable
## ii. let scanner/option->name=tr be settable
## iii.  ... and name=measurements (# seconds)
## iv.  ... and all the resolution & voxel dimensions 
## v. maybe set infoclient port/host parameters too?

#################### end Step 1


numRuns=6
for r in range(0,numRuns):    # r is a run
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

    ############## Step 2: Generate psychopy CSV condition files
    csvOutfile = fileName_base + '%d.csv'%runNum
    with open(csvOutfile, 'wb') as csv_fileh:
        csvFileWriter = csv.writer(csv_fileh)
        csvFileWriter.writerow(header_row_titles)
        
        for i in range(len(stimulusVec)):   # i is an up/down trial
            if stimulusVec[i]:
                dirtext = 'up'
                img = up_arrow_img_filename
                # if fb_run:
                #     sq[questionVec[i]-1][1] += 1
            else:
                dirtext = 'down'
                img = down_arrow_img_filename
                # if fb_run:
                #     sq[questionVec[i]-1][0] += 1
            ## </if stimulusVec>
            csvFileWriter.writerow([dirtext, img, qtext[questionVec[i]-1]]) 
        ## </for>
        csv_fileh.close()  
        print "wrote out " + csvOutfile
    ## </with>    ################### end Step 2

    ############## Step 3: Generate output XML files
    ## do processing here!
    
    matrixDict = matrixMaker(fb_run,stimulusVec,questionVec)

    ## Step 3.2: put output matrices into inElement's condition nodes
    for cond in designNode.findall("option[@conditionName]"):
        cond.text = matrixDict[cond.get('conditionName')]
    
    ## Step 3.3: Writing the output
    ## -- ok, inElement now contains the right stuff for this run.
    ## -- but wait, we need to remove root elements!!!!
    outXMLstr = ET.tostring(inElement)
    (outStr,num) = re.subn("</?root>","",outXMLstr)
    ## finally, dump that string to the output file
    outXMLfile = xmlName_base + '%d.xml'%(r+1)
    with open(outXMLfile,'wb') as out_fileh:
        out_fileh.write(outStr)
        out_fileh.close()
        print "wrote out " + outXMLfile
    ################### end Step 3
## print sq
## </for r> 




