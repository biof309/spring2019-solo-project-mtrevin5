from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

listOrder=[
    '                                        I agree to participate',
    '                                        I do not agree to participate',
    '1) Participant Number',
    '2) Date',
    '3) What is your age?',
    '4) What is your gender?',
    '5) Do you have normal or corrected-to-normal vision?'
    ]
listOrder2=['Radiologist', 'Radiation Oncologist', 'Trainee, Fellow, Resident','Non-Radiologist']

listOrder3=['                                                                         ']

listOrder4=['Abdominal', 'Breast', 'Chest', 'Musculoskeletal', 'Neuro', 'Nuclear', 'General Radiology', 'Pediatric Radiology', 'Prostate MR','Other','Not Applicable']
listOrder5=[
    '1) What is the cancer detection rate at your practice?',
    '2) What is your average recall rate from screening?',
    '3) Were you intially trained in digital or screen film radiography'
]
listOrder6=[
    '1) How long have you been reading prostate MR in years? (exclude residency and fellowship training)',
    '2) Approximately how many prostate cases do you read each week?',
    '3) Approximately what percentage of your clinical time do you spend in prostate imaging?',
    '4) While searching through an image, do you...'
]
#parameters/info about exp





info = {                                          #putting it all into dictionary
    listOrder[0]:False,                           #detects that it's a boolean value. So this is tick box now!
    listOrder[1]:False, 
    listOrder[2]:'',   
    listOrder[3]:data.getDateStr(),
    listOrder[4]:'',
    listOrder[5]:['Male', 'Female', 'Other'],
    listOrder[6]:['Yes', 'No']
    }
info2={
    listOrder2[0]:False,
    listOrder2[1]:False,
    listOrder2[2]:False,
    listOrder2[3]:False
    }
info3={
    listOrder3[0]:''
    }
info4={
    listOrder4[0]: False,
    listOrder4[1]: False,
    listOrder4[2]: False,
    listOrder4[3]: False,
    listOrder4[4]: False,
    listOrder4[5]: False,
    listOrder4[6]: False,
    listOrder4[7]: False,
    listOrder4[8]: False,
    listOrder4[9]: False,
    listOrder4[10]: False
    }
info5={
    listOrder5[0]:'',
    listOrder5[1]:'',
    listOrder5[2]:['Digital', 'Film', 'Not Applicable']
   }
info6={
    listOrder6[0]:'',
    listOrder6[1]:'',
    listOrder6[2]:'',
    listOrder6[3]:['Drill (restrict eye movements to a small region of the image while quickly scrolling through slices)', 'Scan (search over large areas at a given depth before moving on to the next slice)', 'Both']
}


#present dialogue to participant
dlg1 = gui.DlgFromDict(info, title = 'Survey Questions', fixed=[listOrder[3]],order=listOrder) #generating a dialog and presenting it to the participant. Class.
if not dlg1.OK or not info[listOrder[0]]: #can also write if dlg.OK == False:
    core.quit()

filename = "data/%s_%s"%(info[listOrder[2]], info[listOrder[3]]) #creating file
#dataFile = open(filename+'.csv', 'a')  # a simple text file with 'comma-separated-values'
#dataFile.write(info[listOrder[2]])
#dataFile.write(info[listOrder[3]]+) 
#dataFile.write(info[listOrder[4]])
#dataFile.write(info[listOrder[5]]) 
#dataFile.write(info[listOrder[6]))

#if "Non-Radiologist" in info[listOrder[6]]:
#    listOrder.insert(7,"You have selected Non-Radiologist, Enter Profession Role")
#    info["You have selected Non-Radiologist, Enter Profession Role"]=""
dlg2 = gui.DlgFromDict(info2, title = '6) What is your professional role?', order=listOrder2)
if info2['Non-Radiologist']:
    listOrder2.append("Please specify if Non-Radiologist")
    info2[listOrder2[len(listOrder2)-1]]=''
    dlg2 = gui.DlgFromDict(info2, title = '6) What is your professional role?', order=listOrder2)
if info2['Radiologist']:
    listOrder2.append(" 6 a) How many years have you been a practicing radiologist?")
    info2[listOrder2[len(listOrder2)-1]]=''
    dlg2 = gui.DlgFromDict(info2, title = '6) What is your professional role?', order=listOrder2)
if not dlg2.OK: #can also write if dlg.OK == False:
    core.quit()
#elif "You have selected Non-Radiologist, Enter Profession Role" in listOrder:
#    listOrder.pop(7)
    
dlg3 = gui.DlgFromDict(info3, title = '7) On average, how many cases do you read a year? (across all types of imaging)', order=listOrder3)
if not dlg3.OK: #can also write if dlg.OK == False:
    core.quit()

dlg4 = gui.DlgFromDict(info4, title = '8) Which types of imaging do you perform? (select all that apply)', order=listOrder4)
if info4['Other']:
    listOrder4.append("8 a) Please specify if Other")
    info4[listOrder4[len(listOrder4)-1]]=''
    dlg4 = gui.DlgFromDict(info4, title = ' 8) Which types of imaging do you perform?', order=listOrder4)
if not dlg4.OK: #can also write if dlg.OK == False:
    core.quit()
if info4['Breast']:
    dlg5=gui.DlgFromDict(info5, title = 'Breast Questions', order=listOrder5)
    if not dlg5.OK: #can also write if dlg.OK == False:
        core.quit()
if info4['Prostate MR']:
    dlg6=gui.DlgFromDict(info6, title = 'Prostate MR Questions', order=listOrder6)
    if not dlg6.OK: #can also write if dlg.OK == False:
        core.quit()

### Initialization


#Timing of Fixation and Prostate image
fixationSeconds = 0.5
stimulusSeconds = 0.5
#filename = "data/test.csv"
#create needed objects 
display_resolution=1366,768

# Create Window

win=visual.Window(display_resolution,
                        units='norm',
                        color=(-1,-1,-1),
                        fullscr=False, allowGUI=True,
                        screen=0
                        )
respClock = core.Clock()

#frames for fixation and prostate image
fps = win.getActualFrameRate()
print(fps)
fixationFrames = int(fps*fixationSeconds)
print(fixationFrames)
stimulusFrames = int(fps*stimulusSeconds)
print(stimulusFrames)


fixation = visual.TextStim(win=win, name='Fixation',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

ProstateImageId = visual.ImageStim(
    win, image=None, 
    pos=(0, 0))

print(ProstateImageId.size)
scale= (2*.56, 2)
ProstateImageId.size = scale  # scale the image relative to initial size
print(ProstateImageId.size)

SectorMap = visual.ImageStim(
    win, image=None, 
    pos=(0, 0))
    

LocalizePrompt1 = visual.TextStim(win, 
    text='                                   Please localize the lesion on the sector map.\r\n\r\nEven if you think there was not a lesion indicate the most likely location of the lesion.', 
    pos = (0, .88), 
    color = 'green', height=0.07, wrapWidth =800.0, alignVert='center',
    bold = True)

LocalizePrompt2 = visual.TextStim(win, 
    text='Is this where you want it? (Y/N)', 
    pos = (0, .88), 
    color = 'red', height=0.065,
    bold = True)
    
LocalizePrompt3 = visual.TextStim(win, 
    text='Do you have another place? (Y/N)', 
    pos = (0, .85), 
    color = 'red', 
    bold = True)
Theend = visual.ImageStim(
    win, image='The end.jpg', 
    pos=(0, 0))
Ready = visual.ImageStim(
    win, image='Ready.jpg', 
    pos=(0, 0))


#Rating Scale
ratingScale = visual.RatingScale(win=win, low=0, high=100, name='rating', marker='triangle', noMouse=False, textColor= u'white', markerColor='red',stretch=2, markerStart=5, size=1.2, labels=[''], scale='No Lesion                                                                       Certain Lesion')
txt="                              Was there a lesion?\r\n\r\nRate how likely there was a lesion on a scale from 0 to 100.\r\n\r\n0 denotes there was not a lesion.\r\n\r\n100 denotes there was a lesion."
item = visual.TextStim(win=win, text=txt,
    font='Arial',
    pos=[0, 0.40], height=0.07, ori=0, wrapWidth =800.0,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-1.0)
    
    
button_x1=0.3616
button_y1=-0.4525
button_x2=0.5
button_y2=-0.5225

thisExp = data.ExperimentHandler(
        name='Prostate', version='1.0', #not needed, just handy
        extraInfo=info, runtimeInfo=None,
        savePickle=True,saveWideText=True,
        dataFileName = filename, # using our string with data/name_date
        )

conditions = data.importConditions('trialList.xlsx')

trials = data.TrialHandler(trialList=conditions, nReps=1,method='random',extraInfo=info)

mouseText=visual.TextBox(window=win, 
                         text="x",
                         bold=False,
                         italic=False,
                         font_size=21,
                         font_color=[-1,-1,1], 
                         size=(0.1,.1),
                         pos=(0.0,0.5), 
                         units='norm',
                         grid_horz_justification='center',
                         grid_vert_justification='center',
                         )

thisExp.addLoop(trials) #what does this do?
#Start Running trials

#LocalizePrompt1 = visual.TextStim(win, 
#    text='                                   Please localize the lesion on the sector map.\r\n\r\nEven if you think there was not a lesion indicate the most likely location of the lesion.', 
#    pos = (0, .88), 
#    color = 'red', height=0.07, wrapWidth =800.0, alignVert='center',
#    bold = True)

checkBoxes={}

Ready.draw()
win.flip()
keyPressed=event.waitKeys()
    
for thisTrial in trials:
    #update stim for this trial
    img=thisTrial['ProstateImageId']
    ProstateImageId.setImage(thisTrial['ProstateImageId'])
    SectorMap.setImage(thisTrial['SectorMap'])
    checkBoxes[img]={}
    for i in range(1,13):
        cName="chk"+str(i)
        if thisTrial[cName] is not None:
            checkBoxes[img][thisTrial[cName]]={"selected":False, "box":visual.TextBox(window=win, 
                         text="x",
                         bold=False,
                         italic=False,
                         font_size=21,
                         font_color=[-1,-1,1], 
                         size=(0.1,.1),
                         pos=(0.0,0.5), 
                         units='norm',
                         grid_horz_justification='center',
                         grid_vert_justification='center',
                         )}
    if thisTrial['chk1'] is not None:
        chk1_x=float(thisTrial['chk1'].split()[0])
        chk1_y=float(thisTrial['chk1'].split()[1])
    else:
        chk1_x=-1
        chk1_y=-1
    #present fix, stim... 
    for r in range(fixationFrames):
        fixation.draw()
        win.flip()
    
    for f in range(stimulusFrames):
        ProstateImageId.draw()
        win.flip()
        print(stimulusFrames)
        lMouse=event.Mouse(visible=True)

    keyPressed=['']
    mouseDisplayIndex=[False]*13

    win.flip()
    quitNow=False
    kount=0
    checkBoxKey=""
    while True:
        b1,b2,b3=lMouse.getPressed()
        SectorMap.draw()
        LocalizePrompt1.draw()
#        for i in range(kount):
#            if mouseDisplayIndex[i]:
#                mousePositions[i].draw()

        for i in checkBoxes[img]:
            if checkBoxes[img][i]['selected']:
                checkBoxes[img][i]['box'].draw()
        if (b1):
            SectorMap.draw()
            keyPressed=['']
            x=lMouse.getPos()[0]
            y=lMouse.getPos()[1]
            validCoordinates=False

            if len(checkBoxes[img])>0:
                for k in checkBoxes[img]:
                    chk1_x=float(k.split()[0])
                    chk1_y=float(k.split()[1])
                    if x>=chk1_x-0.1 and x<=chk1_x+0.1 and y>=chk1_y-0.1 and y<=chk1_y+0.1:
                       # print("Update")
                        x=chk1_x
                        y=chk1_y
                        validCoordinates=True
                        checkBoxKey=k
                        break
            else:
                validCoordinates=True
       #     print(x,y,checkBoxKey)
            if not validCoordinates:
                print("Invalid Selection")
                continue
            if not (x >=0.3616 and x<=0.5 and y>=-0.5225 and y<=-0.4525):
                while keyPressed[0] not in ['y', 'Y', 'n', 'N']:
                    win.flip()
                    SectorMap.draw()
                    deselectItem=False
                    iIndex=-1
                    checkBoxes[img][checkBoxKey]['box'].setPosition((x,y))
                    checkBoxes[img][checkBoxKey]['selected']=not checkBoxes[img][checkBoxKey]['selected']
                    for i in checkBoxes[img]:
                        if checkBoxes[img][i]['selected']:
                            checkBoxes[img][i]['box'].draw()
                    LocalizePrompt3.draw()
                    win.flip()
                    keyPressed=event.waitKeys()
            else:
                break
            if keyPressed[0] in ['n', 'N']:
                break
            kount=kount+1
            if kount > 13:
                print("Too many selections")
                break
            lMouse.clickReset(buttons=[0,1,2])
            event.clearEvents()
        else:
            win.flip()
    for i in checkBoxes[img]:
        thisExp.addData("CHK_"+str(kount),i+"("+str(checkBoxes[img][i]['selected'])+")")
        thisExp.nextEntry()
    event.clearEvents()
            
    ratingScale.reset()
    while ratingScale.noResponse:
        item.draw()
        ratingScale.draw()
        win.flip()
        rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
        thisExp.addData('rating', ratingScale.getRating())  
        thisExp.addData('RatingRT', ratingScale.getRT())
        thisExp.addData('ChoiceHistory',ratingScale.getHistory())
        thisExp.addData('Q6',info2)
        thisExp.addData('Q7',info3)
        thisExp.addData('Q8',info4)
        thisExp.addData('Breast',info5)
        thisExp.addData('Prostate',info6)
        thisExp.nextEntry()
    #event.clearEvents()
    #thisExp.addData("Participant Number",info['1) Participant Number'])
#    kount=1
#    for i in checkBoxes[img]:
#       thisExp.addData("CHK_"+str(kount),i+"("+str(checkBoxes[img][i]['selected'])+")")
#        kount+=1
Theend.draw()
win.flip()
keyPressed=event.waitKeys()
#thisExp.saveAsText("data/test.csv")
