# Blink an LED once a second
from synapse.platforms import *
from synapse.switchboard import *


blinkPin = 20   # a pin with an LED attached, pyXY boards have an LED on pin 10
blinkFlag = 0
otherNodeAddr = "\x5D\x27\x6C"

@setHook(HOOK_STARTUP)
def init():
    initUart(1, 9600)
    crossConnect(DS_TRANSPARENT, DS_STDIO)
    ucastSerial(otherNodeAddr)
    

@setHook(HOOK_1S)
def callBlink():
    global blinkFlag # Need to use the global blinkFlag variable
    
    if blinkFlag == 0:
        blink(0)    # turn LED off
        blinkFlag = 1
        print '\x41\x42\x43\x0d\x0a'
    else:
        blink(1)    # turn LED on
        blinkFlag = 0

def blink(b):
    if b == 1:
        writePin(blinkPin, True)    # write blinkPin high
    else:
        writePin(blinkPin, False)   # write blinkPin low


@setHook(HOOK_STDOUT)
def stdoutEvent(text):
    pulsePin(blinkPin, 50, True)