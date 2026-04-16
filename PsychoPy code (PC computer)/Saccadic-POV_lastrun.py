#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.1.2),
    on Thu Apr 16 06:48:16 2026
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.1.2'
expName = 'Saccadic-POV'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/w00085722/Documents/Saccadic-POV/PsychoPy code (PC computer)/Saccadic-POV_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Setup" ---
    text_instr_1 = visual.TextStim(win=win, name='text_instr_1',
        text='Welcome!  A series of images will be presented on the \nlight bar in front of you.  You will be asked to identify either the \nSMALL letters that make up the image, or the LARGE letter \nbuilt from the small ones.',
        font='Arial',
        pos=(0, 0.4), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_begin = keyboard.Keyboard(deviceName='defaultKeyboard')
    text_example = visual.TextStim(win=win, name='text_example',
        text='L L L L L\n    L     \n    L     \n    L     \n    L     \n',
        font='Courier New',
        pos=(0.35, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    # Run 'Begin Experiment' code from code_example
    text_example.setAlignText('left')
    
    text_instr_3 = visual.TextStim(win=win, name='text_instr_3',
        text="In the example above, the LARGE letter is a T, \n and the SMALL letters are L's",
        font='Arial',
        pos=(0, -0.3), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    continue_instr_1 = visual.TextStim(win=win, name='continue_instr_1',
        text='Press any key to continue.',
        font='Arial',
        pos=(0, -0.45), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    
    # --- Initialize components for Routine "Display_Experiment_Type" ---
    text_exp_type = visual.TextStim(win=win, name='text_exp_type',
        text='',
        font='Arial',
        pos=(0, 0.15), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_exp_type = keyboard.Keyboard(deviceName='defaultKeyboard')
    continue_instr_2 = visual.TextStim(win=win, name='continue_instr_2',
        text='Press any key to continue.',
        font='Arial',
        pos=(0, -0.45), draggable=False, height=0.03, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    
    # --- Initialize components for Routine "blank" ---
    text = visual.TextStim(win=win, name='text',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "Trial" ---
    trial_inprogress = visual.TextStim(win=win, name='trial_inprogress',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    trial_servostatus = visual.TextStim(win=win, name='trial_servostatus',
        text=None,
        font='Arial',
        pos=(0, -0.2), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_input = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "Get_Trial_Response" ---
    text_trial_getresponse = visual.TextStim(win=win, name='text_trial_getresponse',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_whatletter = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "End" ---
    text_instr = visual.TextStim(win=win, name='text_instr',
        text='All done.  Thank you!',
        font='Arial',
        pos=(-0.3, 0.25), draggable=False, height=0.04, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_end = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Setup" ---
    # create an object to store info about Routine Setup
    Setup = data.Routine(
        name='Setup',
        components=[text_instr_1, key_begin, text_example, text_instr_3, continue_instr_1],
    )
    Setup.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_begin
    key_begin.keys = []
    key_begin.rt = []
    _key_begin_allKeys = []
    # store start times for Setup
    Setup.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Setup.tStart = globalClock.getTime(format='float')
    Setup.status = STARTED
    thisExp.addData('Setup.started', Setup.tStart)
    Setup.maxDuration = None
    # keep track of which components have finished
    SetupComponents = Setup.components
    for thisComponent in Setup.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Setup" ---
    thisExp.currentRoutine = Setup
    Setup.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_instr_1* updates
        
        # if text_instr_1 is starting this frame...
        if text_instr_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_instr_1.frameNStart = frameN  # exact frame index
            text_instr_1.tStart = t  # local t and not account for scr refresh
            text_instr_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_instr_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_instr_1.status = STARTED
            text_instr_1.setAutoDraw(True)
        
        # if text_instr_1 is active this frame...
        if text_instr_1.status == STARTED:
            # update params
            pass
        
        # *key_begin* updates
        
        # if key_begin is starting this frame...
        if key_begin.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_begin.frameNStart = frameN  # exact frame index
            key_begin.tStart = t  # local t and not account for scr refresh
            key_begin.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_begin, 'tStartRefresh')  # time at next scr refresh
            # update status
            key_begin.status = STARTED
            # keyboard checking is just starting
            key_begin.clock.reset()  # now t=0
            key_begin.clearEvents(eventType='keyboard')
        if key_begin.status == STARTED:
            theseKeys = key_begin.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
            _key_begin_allKeys.extend(theseKeys)
            if len(_key_begin_allKeys):
                key_begin.keys = _key_begin_allKeys[-1].name  # just the last key pressed
                key_begin.rt = _key_begin_allKeys[-1].rt
                key_begin.duration = _key_begin_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *text_example* updates
        
        # if text_example is starting this frame...
        if text_example.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_example.frameNStart = frameN  # exact frame index
            text_example.tStart = t  # local t and not account for scr refresh
            text_example.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_example, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_example.status = STARTED
            text_example.setAutoDraw(True)
        
        # if text_example is active this frame...
        if text_example.status == STARTED:
            # update params
            pass
        
        # *text_instr_3* updates
        
        # if text_instr_3 is starting this frame...
        if text_instr_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_instr_3.frameNStart = frameN  # exact frame index
            text_instr_3.tStart = t  # local t and not account for scr refresh
            text_instr_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_instr_3, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_instr_3.status = STARTED
            text_instr_3.setAutoDraw(True)
        
        # if text_instr_3 is active this frame...
        if text_instr_3.status == STARTED:
            # update params
            pass
        
        # *continue_instr_1* updates
        
        # if continue_instr_1 is starting this frame...
        if continue_instr_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            continue_instr_1.frameNStart = frameN  # exact frame index
            continue_instr_1.tStart = t  # local t and not account for scr refresh
            continue_instr_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(continue_instr_1, 'tStartRefresh')  # time at next scr refresh
            # update status
            continue_instr_1.status = STARTED
            continue_instr_1.setAutoDraw(True)
        
        # if continue_instr_1 is active this frame...
        if continue_instr_1.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Setup,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Setup.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Setup.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Setup.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Setup" ---
    for thisComponent in Setup.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Setup
    Setup.tStop = globalClock.getTime(format='float')
    Setup.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Setup.stopped', Setup.tStop)
    thisExp.nextEntry()
    # the Routine "Setup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    exp_type = data.TrialHandler2(
        name='exp_type',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('setup_data/exp_type.xlsx'), 
        seed=None, 
        isTrials=False, 
    )
    thisExp.addLoop(exp_type)  # add the loop to the experiment
    thisExp_type = exp_type.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisExp_type.rgb)
    if thisExp_type != None:
        for paramName in thisExp_type:
            globals()[paramName] = thisExp_type[paramName]
    
    for thisExp_type in exp_type:
        exp_type.status = STARTED
        if hasattr(thisExp_type, 'status'):
            thisExp_type.status = STARTED
        currentLoop = exp_type
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # abbreviate parameter names if possible (e.g. rgb = thisExp_type.rgb)
        if thisExp_type != None:
            for paramName in thisExp_type:
                globals()[paramName] = thisExp_type[paramName]
        
        # --- Prepare to start Routine "Display_Experiment_Type" ---
        # create an object to store info about Routine Display_Experiment_Type
        Display_Experiment_Type = data.Routine(
            name='Display_Experiment_Type',
            components=[text_exp_type, key_exp_type, continue_instr_2],
        )
        Display_Experiment_Type.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        text_exp_type.setText(str(saccade_description) +'\n\n\n'+str(forest_trees_description))
        # create starting attributes for key_exp_type
        key_exp_type.keys = []
        key_exp_type.rt = []
        _key_exp_type_allKeys = []
        # store start times for Display_Experiment_Type
        Display_Experiment_Type.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Display_Experiment_Type.tStart = globalClock.getTime(format='float')
        Display_Experiment_Type.status = STARTED
        Display_Experiment_Type.maxDuration = None
        # keep track of which components have finished
        Display_Experiment_TypeComponents = Display_Experiment_Type.components
        for thisComponent in Display_Experiment_Type.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Display_Experiment_Type" ---
        thisExp.currentRoutine = Display_Experiment_Type
        Display_Experiment_Type.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisExp_type, 'status') and thisExp_type.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_exp_type* updates
            
            # if text_exp_type is starting this frame...
            if text_exp_type.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text_exp_type.frameNStart = frameN  # exact frame index
                text_exp_type.tStart = t  # local t and not account for scr refresh
                text_exp_type.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_exp_type, 'tStartRefresh')  # time at next scr refresh
                # update status
                text_exp_type.status = STARTED
                text_exp_type.setAutoDraw(True)
            
            # if text_exp_type is active this frame...
            if text_exp_type.status == STARTED:
                # update params
                pass
            
            # *key_exp_type* updates
            
            # if key_exp_type is starting this frame...
            if key_exp_type.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_exp_type.frameNStart = frameN  # exact frame index
                key_exp_type.tStart = t  # local t and not account for scr refresh
                key_exp_type.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_exp_type, 'tStartRefresh')  # time at next scr refresh
                # update status
                key_exp_type.status = STARTED
                # keyboard checking is just starting
                key_exp_type.clock.reset()  # now t=0
                key_exp_type.clearEvents(eventType='keyboard')
            if key_exp_type.status == STARTED:
                theseKeys = key_exp_type.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
                _key_exp_type_allKeys.extend(theseKeys)
                if len(_key_exp_type_allKeys):
                    key_exp_type.keys = _key_exp_type_allKeys[-1].name  # just the last key pressed
                    key_exp_type.rt = _key_exp_type_allKeys[-1].rt
                    key_exp_type.duration = _key_exp_type_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *continue_instr_2* updates
            
            # if continue_instr_2 is starting this frame...
            if continue_instr_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                continue_instr_2.frameNStart = frameN  # exact frame index
                continue_instr_2.tStart = t  # local t and not account for scr refresh
                continue_instr_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(continue_instr_2, 'tStartRefresh')  # time at next scr refresh
                # update status
                continue_instr_2.status = STARTED
                continue_instr_2.setAutoDraw(True)
            
            # if continue_instr_2 is active this frame...
            if continue_instr_2.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=Display_Experiment_Type,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                Display_Experiment_Type.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if Display_Experiment_Type.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in Display_Experiment_Type.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Display_Experiment_Type" ---
        for thisComponent in Display_Experiment_Type.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Display_Experiment_Type
        Display_Experiment_Type.tStop = globalClock.getTime(format='float')
        Display_Experiment_Type.tStopRefresh = tThisFlipGlobal
        # the Routine "Display_Experiment_Type" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler2(
            name='trials',
            nReps=1, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions('setup_data/trials.xlsx'), 
            seed=None, 
            isTrials=True, 
        )
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTrial in trials:
            trials.status = STARTED
            if hasattr(thisTrial, 'status'):
                thisTrial.status = STARTED
            currentLoop = trials
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    globals()[paramName] = thisTrial[paramName]
            
            # --- Prepare to start Routine "blank" ---
            # create an object to store info about Routine blank
            blank = data.Routine(
                name='blank',
                components=[text],
            )
            blank.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # store start times for blank
            blank.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            blank.tStart = globalClock.getTime(format='float')
            blank.status = STARTED
            blank.maxDuration = 2
            # keep track of which components have finished
            blankComponents = blank.components
            for thisComponent in blank.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "blank" ---
            thisExp.currentRoutine = blank
            blank.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 2.0:
                # if trial has changed, end Routine now
                if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # is it time to end the Routine? (based on local clock)
                if tThisFlip > blank.maxDuration-frameTolerance:
                    blank.maxDurationReached = True
                    continueRoutine = False
                
                # *text* updates
                
                # if text is starting this frame...
                if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text.frameNStart = frameN  # exact frame index
                    text.tStart = t  # local t and not account for scr refresh
                    text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    text.status = STARTED
                    text.setAutoDraw(True)
                
                # if text is active this frame...
                if text.status == STARTED:
                    # update params
                    pass
                
                # if text is stopping this frame...
                if text.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > text.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        text.tStop = t  # not accounting for scr refresh
                        text.tStopRefresh = tThisFlipGlobal  # on global time
                        text.frameNStop = frameN  # exact frame index
                        # update status
                        text.status = FINISHED
                        text.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=blank,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    blank.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if blank.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in blank.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "blank" ---
            for thisComponent in blank.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for blank
            blank.tStop = globalClock.getTime(format='float')
            blank.tStopRefresh = tThisFlipGlobal
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if blank.maxDurationReached:
                routineTimer.addTime(-blank.maxDuration)
            elif blank.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-2.000000)
            
            # --- Prepare to start Routine "Trial" ---
            # create an object to store info about Routine Trial
            Trial = data.Routine(
                name='Trial',
                components=[trial_inprogress, trial_servostatus, key_input],
            )
            Trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            trial_inprogress.setColor('white', colorSpace='rgb')
            trial_inprogress.setText("(The POV display is now showing image number "+str(image_number)+", a "+str(forest_letter)+" made of "+str(tree_letter)+"'s.\n\n")
            trial_servostatus.setColor('white', colorSpace='rgb')
            trial_servostatus.setText('')
            # create starting attributes for key_input
            key_input.keys = []
            key_input.rt = []
            _key_input_allKeys = []
            # Run 'Begin Routine' code from run_trial_code
            key_input.clearEvents()
            # store start times for Trial
            Trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Trial.tStart = globalClock.getTime(format='float')
            Trial.status = STARTED
            thisExp.addData('Trial.started', Trial.tStart)
            Trial.maxDuration = None
            # keep track of which components have finished
            TrialComponents = Trial.components
            for thisComponent in Trial.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Trial" ---
            thisExp.currentRoutine = Trial
            Trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *trial_inprogress* updates
                
                # if trial_inprogress is starting this frame...
                if trial_inprogress.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    trial_inprogress.frameNStart = frameN  # exact frame index
                    trial_inprogress.tStart = t  # local t and not account for scr refresh
                    trial_inprogress.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(trial_inprogress, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'trial_inprogress.started')
                    # update status
                    trial_inprogress.status = STARTED
                    trial_inprogress.setAutoDraw(True)
                
                # if trial_inprogress is active this frame...
                if trial_inprogress.status == STARTED:
                    # update params
                    pass
                
                # *trial_servostatus* updates
                
                # if trial_servostatus is starting this frame...
                if trial_servostatus.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    trial_servostatus.frameNStart = frameN  # exact frame index
                    trial_servostatus.tStart = t  # local t and not account for scr refresh
                    trial_servostatus.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(trial_servostatus, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    trial_servostatus.status = STARTED
                    trial_servostatus.setAutoDraw(True)
                
                # if trial_servostatus is active this frame...
                if trial_servostatus.status == STARTED:
                    # update params
                    pass
                
                # *key_input* updates
                waitOnFlip = False
                
                # if key_input is starting this frame...
                if key_input.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                    # keep track of start time/frame for later
                    key_input.frameNStart = frameN  # exact frame index
                    key_input.tStart = t  # local t and not account for scr refresh
                    key_input.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_input, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'key_input.started')
                    # update status
                    key_input.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_input.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_input.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_input.status == STARTED and not waitOnFlip:
                    theseKeys = key_input.getKeys(keyList=['enter','space'], ignoreKeys=["escape"], waitRelease=False)
                    _key_input_allKeys.extend(theseKeys)
                    if len(_key_input_allKeys):
                        key_input.keys = _key_input_allKeys[-1].name  # just the last key pressed
                        key_input.rt = _key_input_allKeys[-1].rt
                        key_input.duration = _key_input_allKeys[-1].duration
                # Run 'Each Frame' code from run_trial_code
                keys = key_input.getKeys()
                if keys:
                    print(keys)
                if 'space' in keys:
                    if saccade_type == 'servo':
                        trial_servostatus.setText('Slewing servo')
                    else:
                        trial_servostatus.setText('No servo allowed')
                else:
                    trial_servostatus.setText('')
                if 'return' in keys:
                    continueRoutine = False
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Trial,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Trial.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Trial.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Trial" ---
            for thisComponent in Trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Trial
            Trial.tStop = globalClock.getTime(format='float')
            Trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Trial.stopped', Trial.tStop)
            # check responses
            if key_input.keys in ['', [], None]:  # No response was made
                key_input.keys = None
            trials.addData('key_input.keys',key_input.keys)
            if key_input.keys != None:  # we had a response
                trials.addData('key_input.rt', key_input.rt)
                trials.addData('key_input.duration', key_input.duration)
            # the Routine "Trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "Get_Trial_Response" ---
            # create an object to store info about Routine Get_Trial_Response
            Get_Trial_Response = data.Routine(
                name='Get_Trial_Response',
                components=[text_trial_getresponse, key_resp_whatletter],
            )
            Get_Trial_Response.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            text_trial_getresponse.setColor('white', colorSpace='rgb')
            text_trial_getresponse.setText("Type the "+("SMALL" if forest_trees=="trees" else "LARGE")+" letter you saw.")
            # create starting attributes for key_resp_whatletter
            key_resp_whatletter.keys = []
            key_resp_whatletter.rt = []
            _key_resp_whatletter_allKeys = []
            # store start times for Get_Trial_Response
            Get_Trial_Response.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Get_Trial_Response.tStart = globalClock.getTime(format='float')
            Get_Trial_Response.status = STARTED
            thisExp.addData('Get_Trial_Response.started', Get_Trial_Response.tStart)
            Get_Trial_Response.maxDuration = None
            # keep track of which components have finished
            Get_Trial_ResponseComponents = Get_Trial_Response.components
            for thisComponent in Get_Trial_Response.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Get_Trial_Response" ---
            thisExp.currentRoutine = Get_Trial_Response
            Get_Trial_Response.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # if trial has changed, end Routine now
                if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_trial_getresponse* updates
                
                # if text_trial_getresponse is starting this frame...
                if text_trial_getresponse.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    text_trial_getresponse.frameNStart = frameN  # exact frame index
                    text_trial_getresponse.tStart = t  # local t and not account for scr refresh
                    text_trial_getresponse.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(text_trial_getresponse, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text_trial_getresponse.started')
                    # update status
                    text_trial_getresponse.status = STARTED
                    text_trial_getresponse.setAutoDraw(True)
                
                # if text_trial_getresponse is active this frame...
                if text_trial_getresponse.status == STARTED:
                    # update params
                    pass
                
                # *key_resp_whatletter* updates
                waitOnFlip = False
                
                # if key_resp_whatletter is starting this frame...
                if key_resp_whatletter.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    key_resp_whatletter.frameNStart = frameN  # exact frame index
                    key_resp_whatletter.tStart = t  # local t and not account for scr refresh
                    key_resp_whatletter.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(key_resp_whatletter, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    key_resp_whatletter.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(key_resp_whatletter.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(key_resp_whatletter.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if key_resp_whatletter.status == STARTED and not waitOnFlip:
                    theseKeys = key_resp_whatletter.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
                    _key_resp_whatletter_allKeys.extend(theseKeys)
                    if len(_key_resp_whatletter_allKeys):
                        key_resp_whatletter.keys = _key_resp_whatletter_allKeys[-1].name  # just the last key pressed
                        key_resp_whatletter.rt = _key_resp_whatletter_allKeys[-1].rt
                        key_resp_whatletter.duration = _key_resp_whatletter_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer, globalClock], 
                        currentRoutine=Get_Trial_Response,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    Get_Trial_Response.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if Get_Trial_Response.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in Get_Trial_Response.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Get_Trial_Response" ---
            for thisComponent in Get_Trial_Response.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Get_Trial_Response
            Get_Trial_Response.tStop = globalClock.getTime(format='float')
            Get_Trial_Response.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Get_Trial_Response.stopped', Get_Trial_Response.tStop)
            # check responses
            if key_resp_whatletter.keys in ['', [], None]:  # No response was made
                key_resp_whatletter.keys = None
            trials.addData('key_resp_whatletter.keys',key_resp_whatletter.keys)
            if key_resp_whatletter.keys != None:  # we had a response
                trials.addData('key_resp_whatletter.rt', key_resp_whatletter.rt)
                trials.addData('key_resp_whatletter.duration', key_resp_whatletter.duration)
            # the Routine "Get_Trial_Response" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            # mark thisTrial as finished
            if hasattr(thisTrial, 'status'):
                thisTrial.status = FINISHED
            # if awaiting a pause, pause now
            if trials.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                trials.status = STARTED
            thisExp.nextEntry()
            
        # completed 1 repeats of 'trials'
        trials.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisExp_type as finished
        if hasattr(thisExp_type, 'status'):
            thisExp_type.status = FINISHED
        # if awaiting a pause, pause now
        if exp_type.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            exp_type.status = STARTED
    # completed 1 repeats of 'exp_type'
    exp_type.status = FINISHED
    
    
    # --- Prepare to start Routine "End" ---
    # create an object to store info about Routine End
    End = data.Routine(
        name='End',
        components=[text_instr, key_end],
    )
    End.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_end
    key_end.keys = []
    key_end.rt = []
    _key_end_allKeys = []
    # store start times for End
    End.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    End.tStart = globalClock.getTime(format='float')
    End.status = STARTED
    thisExp.addData('End.started', End.tStart)
    End.maxDuration = None
    # keep track of which components have finished
    EndComponents = End.components
    for thisComponent in End.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "End" ---
    thisExp.currentRoutine = End
    End.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_instr* updates
        
        # if text_instr is starting this frame...
        if text_instr.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_instr.frameNStart = frameN  # exact frame index
            text_instr.tStart = t  # local t and not account for scr refresh
            text_instr.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_instr, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_instr.status = STARTED
            text_instr.setAutoDraw(True)
        
        # if text_instr is active this frame...
        if text_instr.status == STARTED:
            # update params
            pass
        
        # *key_end* updates
        
        # if key_end is starting this frame...
        if key_end.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_end.frameNStart = frameN  # exact frame index
            key_end.tStart = t  # local t and not account for scr refresh
            key_end.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_end, 'tStartRefresh')  # time at next scr refresh
            # update status
            key_end.status = STARTED
            # keyboard checking is just starting
            key_end.clock.reset()  # now t=0
            key_end.clearEvents(eventType='keyboard')
        if key_end.status == STARTED:
            theseKeys = key_end.getKeys(keyList=None, ignoreKeys=["escape"], waitRelease=False)
            _key_end_allKeys.extend(theseKeys)
            if len(_key_end_allKeys):
                key_end.keys = _key_end_allKeys[-1].name  # just the last key pressed
                key_end.rt = _key_end_allKeys[-1].rt
                key_end.duration = _key_end_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=End,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            End.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if End.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in End.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "End" ---
    for thisComponent in End.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for End
    End.tStop = globalClock.getTime(format='float')
    End.tStopRefresh = tThisFlipGlobal
    thisExp.addData('End.stopped', End.tStop)
    thisExp.nextEntry()
    # the Routine "End" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
