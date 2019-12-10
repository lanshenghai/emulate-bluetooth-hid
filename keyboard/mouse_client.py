#!/usr/bin/python
#
# YAPTB Bluetooth keyboard emulation service
# keyboard copy client. 
# Reads local key events and forwards them to the btk_server DBUS service
#
# Adapted from www.linuxuser.co.uk/tutorials/emulate-a-bluetooth-keyboard-with-the-raspberry-pi
#
#
import os #used to all external commands
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time
import evdev # used to get input from the keyboard
from evdev import *
import keymap # used to map evdev input to hid keodes



#Define a client to listen to local key events
class Mouse():


    def __init__(self):
        #the structure for a bt keyboard input report (size is 10 bytes)

        self.last_x = None
        self.last_y = None
        self.last_timestamp = None
        # the structure for a bluetooth mouse input report (size is 6 bytes)
        self.mouse_state = [
            0xA1,  # this is an input report
            0x02,  # Usage report = Mouse
            0x00,  # Bit array for Buttons ( Bits 0...4 : Buttons 1...5, Bits 5...7 : Unused )
            0x00,  # Rel X
            0x00,  # Rel Y
            0x00   # Mouse Wheel
        ]

        print "setting up DBus Client"    

        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object('org.yaptb.btkbservice','/org/yaptb/btkbservice')
        self.iface = dbus.Interface(self.btkservice,'org.yaptb.btkbservice')    


        print "waiting for keyboard"

        #keep trying to key a keyboard
        have_dev=False
        while have_dev==False:
            try:
                #try and get a keyboard - should always be event0 as
                #we're only plugging one thing in
                self.dev = InputDevice("/dev/input/event5")
                print self.dev.capabilities(verbose=True)
                #self.dev = InputDevice("/dev/input/mice")
                have_dev=True
            except OSError:
                print "Mouse not found, waiting 3 seconds and retrying"
                time.sleep(3)
            print "found a mouse"
        

    # take care of mouse buttons
    def change_state_button(self, event):
        if event.code == ecodes.BTN_LEFT:
            print("Left Mouse Button Pressed")
            self.mouse_state[2] = event.value
        elif event.code == ecodes.BTN_RIGHT:
            print("Right Mouse Button Pressed")
            self.mouse_state[2] = 2 * event.value
        elif event.code == ecodes.BTN_MIDDLE:
            print("Middle Mouse Button Pressed")
            self.mouse_state[2] = 3 * event.value
        self.mouse_state[3] = 0x00
        self.mouse_state[4] = 0x00
        self.mouse_state[5] = 0x00

    # take care of mouse movements
    def change_state_movement(self, event):
        self.mouse_state[3] = 0x00
        self.mouse_state[4] = 0x00
        self.mouse_state[5] = 0x00
        if event.code == ecodes.REL_X:
            self.mouse_state[3] = event.value & 0xFF
        elif event.code == ecodes.REL_Y:
            self.mouse_state[4] = event.value & 0xFF
        elif event.code == ecodes.REL_WHEEL:
            self.mouse_state[5] = event.value & 0xFF


    #poll for keyboard events
    def event_loop(self):
        for event in self.dev.read_loop():
            #only bother if we hit a key and its an up or down event
            #if event.type==ecodes.EV_KEY and event.value < 2:
            #    self.change_state(event)
            #    self.send_input()
            if event.type == ecodes.EV_KEY and event.value < 2:
                self.change_state_button(event)
                self.send_input()
            elif event.type == ecodes.EV_REL:
                self.change_state_movement(event)
                self.send_input()


    #forward keyboard events to the dbus service
    def send_input(self):
        # data = [0xA1, 0x2, 0,
        #     0,  # X
        #     0,     # Y
        #     0, 0, 0]    # Z
        # if event.type == ecodes.EV_ABS:
        #     if event.code == ecodes.ABS_X:
        #         if self.last_x != None:
        #             if event.value > self.last_x:
        #                 data[2] = min(event.value - self.last_x, 128) + 127
        #             else:
        #                 data[2] = max(event.value - self.last_x, -127) + 127
        #         self.last_x = event.value
        #     if event.code == ecodes.ABS_Y:
        #         if self.last_y != None:
        #             if event.value > self.last_y:
        #                 data[3] = min(event.value - self.last_y, 128) + 127
        #             else:
        #                 data[3] = max(event.value - self.last_y, -127) + 127
        #         self.last_y = event.value
        # else:
        #     if event.code == ecodes.REL_X:
        #         data[2] = event.value & 0xff
        #     if event.code == ecodes.REL_Y:
        #         data[3] = event.value & 0xff
        #print "Send with x=%d, y=%d" % (data[2], data[3])
        self.iface.send_keys(self.mouse_state)



if __name__ == "__main__":

    print "Setting up mouse"

    kb = Mouse()

    print "starting event loop"
    kb.event_loop()

