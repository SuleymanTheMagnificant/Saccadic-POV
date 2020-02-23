""" Control a persistence-of-vision LED display powered by an Arduino running Saccadic_POV_*_LEDs.ino.
Usage:
  leds = Pypovled(PORTNAME)
Functions:
  ready(): Returns true if comms established.
  brightness(VAL): Set display brightness 0-255
  cycle(): Rotate through all available images
  pick(VAL): Select image to show
  show(): Show image
  off(): Stop showing image
  time(VAL): Set display time (seconds)

"""

POV_BRIGHTNESS = b'b'
POV_CYCLE = b'c'
POV_PICK = b'p'
POV_OFF = b'o'
POV_SHOW = b's'
POV_TIME = b't'  
POV_NIMAGES = b'n'
POV_SEQUENCE = b'q'

import serial
import time
import re

class Pypovled:

    def __init__(self,comport=None):
        self.ready = False
        if comport is not None:
            self.open(comport)
    
    def ready(self):
        """True if connection to a working Arduino POV display is established."""
        return self.ready
    
    def open(self,comport):
        """Open a serial connection on port comport."""
        self.ready = False
        try:
            self.ser = serial.Serial(comport,9600,timeout=1)
            self.ready = True
        except:
            print('Failed to open serial port ',comport)     
            self.ready = False
        if self.ready:
            # Send some greetings to the Arduino
            self.ser.flushInput()
            self.ser.write(POV_NIMAGES)       # Wake up!
            self.ser.flushOutput()
            resp = self.ser.readline()
            print(resp.decode())
            if len(resp) < 1:
                print('Arduino is not responding.')
                self.ready = False
                return
            else:
                print('Arduino responded.')
                self.ready = True
                self.ser.flushInput()
    
    def close(self):
        try:
            self.ser.close()
        except:
            pass
        self.ready = False

    def cmd_no_args(self,cmd):
        self.ser.flushInput()
        self.ser.write(cmd)
        self.ser.flushOutput()
        return self.ser.readline().decode().rstrip()
        
    def cmd_one_arg(self,cmd,arg):
        print(cmd+arg)
        self.ser.reset_input_buffer()
        self.ser.write(cmd+arg+b'\n')
        return self.ser.readline().decode().rstrip()

    def cycle(self):
        return self.cmd_no_args(POV_CYCLE)
        
    def off(self):
        return self.cmd_no_args(POV_OFF)

    def show(self):
        return self.cmd_no_args(POV_SHOW)

    def sequence(self,list):
        seq = b''
        for i in list[:-1]:
            seq += str(i).encode()+b','
        seq += str(list[-1]).encode()
        return self.cmd_one_arg(POV_SEQUENCE,seq)

    def get_num_images(self):
        resp = self.cmd_no_args(POV_NIMAGES)
        return int(re.match(r'\d+',resp)[0])
    
    def pick(self,image):
        return self.cmd_one_arg(POV_PICK,str(image).encode())
        
    def brightness(self,val):
        return self.cmd_one_arg(POV_BRIGHTNESS,str(val).encode())
                
    def time(self,val):
        return self.cmd_one_arg(POV_TIME,str(val).encode())