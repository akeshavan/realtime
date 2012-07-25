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

### global vars ... should probably be options?
############## condition file globals!
fileName_base = "../conditions/autoRTconditions"
header_row_titles = ["arrow","image","q_or_r"]
up_arrow_img_filename = "images/up.jpg"
down_arrow_img_filename = "images/down.jpg"
qtext = ["Rate your ability to control your brain activation at this time.","Rate your ability to concentrate at this time.","Rate how much you relied on your strategy during this trial.","Rest."]
###############  XML file globals!
xmlDir = "../murfi/fakedata/scripts/"
softwareDir = "~/software/murfi/"   ## murfi location
xmlInputName = xmlDir + "run1.xml"
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

### now permute the stimulus rows (and corresponding question rows)
sq_zip = zip(stimuli,questions)
random.shuffle(sq_zip)
[stimPerm,questPerm] = zip(*sq_zip)
stimuli = list(stimPerm)
questions = list(questPerm)
### this is for checking question counterbalancing!
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
for elem in inElement.findall("processor/module[@name='mask-load']"):
    mask = subjectsDir + '/mask/'+ elem.find("option[@name='filename']").text.strip() + '.nii'
    if os.path.isfile(mask):   ## verify that the file exists
        mask_dtype = nib.Nifti1Image.load(mask).get_data_dtype()
        if  mask_dtype == "int16":   ## murfi needs the short datatype, AKA int16
            print "Found valid int16 nifti mask:" + mask
        else:
            print "ERROR in cond_and_XML_gen.py: mask data type is " + mask_dtype + ", should be int16!"
            exit(1)
    else:
        print "ERROR in cond_and_XML_gen.py: could not find mask file " + mask
        exit(1)

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
    with open(fileName_base+'%d.csv'%runNum, 'wb') as csv_fileh:
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
    ## </with>    ################### end Step 2

    ############## Step 3: Generate output XML files
    outXMLfile = xmlName_base + '%d_auto.xml'%r
    outElem = ET.ElementTree(inElement)
    ## do processing here!
    outElem.write(outXMLfile)
    ## need to remove root elements!!!!

## print sq
## </for r> 




