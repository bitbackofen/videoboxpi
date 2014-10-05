#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import signal
import ConfigParser
from pyomxplayer import OMXPlayer
from logbook import Logger
from logbook import SyslogHandler

log = Logger('Door Logger')
error_handler = SyslogHandler('videodoor', level='DEBUG')

with error_handler.applicationbound():

    Config = ConfigParser.ConfigParser()
    Config.read('/etc/videodoor/videodoor.ini')
    SensorPin = Config.getint('hardware','SensorPin')
    log.debug('setting up GPIO pin %i...' % SensorPin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SensorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    log.debug('done.')

    log.debug('Setting up the omxplayer instance...')
    File = Config.get('video','File')
    Options = Config.get('video','Options')
    omx_status = False
    log.info('initializing videoplayer with file %s and options %s' % (File, Options))
    omx = OMXPlayer(File, Options)
    log.debug('done.')

    def start_video():
        global omx, omx_status
        if(omx_status):
    	    log.warn('video already running')
        else:
        	omx.toggle_pause()
        	omx_status = True
        	log.info('door opened')

    def stop_video():
        global omx, omx_status
        if(omx_status):
        	omx.toggle_pause()
        	omx.previous_chapter()
        	omx_status = False
        	log.info('door closed')
        else:
    	    log.warn('video not running')

    def my_callback2(channel):
        global Config
        inverse = Config.getboolean('hardware','Inverse')
        if GPIO.input(channel) > 0:
            if(inverse):
    	        stop_video()
            else:
                start_video()
        else:
    	    if(inverse):
                start_video()
            else:
                stop_video()

    GPIO.add_event_detect(23, GPIO.BOTH, callback=my_callback2, bouncetime=100)

    try:
        log.info('Pausing and waiting for interrupt...')
        signal.pause()
        log.debug('Something went wrong...')

    except KeyboardInterrupt:
        GPIO.cleanup()
        omx.stop()
    GPIO.cleanup()
    omx.stop()
