#!/usr/bin/python

# import debug
#
#
# if debug.RELAY_TEST == 0:

import RPi.GPIO as GPIO

# else:
#     import DUMMY_GPIO as GPIO
#     print "DEBUG RELAY"


class Relay(object):
    OFF = 0
    ON = 1
    FOFF = 2
    FON = 3
    UNKNOWN = 4

    def __init__(self, pin, name="relay"):
        super(Relay, self).__init__()
        self.pin = pin
        self.name = name
        self.current_state = Relay.UNKNOWN
        self.overridden = False

    def init(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.turn_relay_off()

    def current_pos(self):
        s = ""
        if self.current_state == Relay.ON:
            s = "ON"
        if self.current_state == Relay.OFF:
            s = "OFF"
        if self.overridden:
            s = s + " overridden"
        return s

    def toggle(self):
        over = self.overridden
        if self.current_state != Relay.ON:

            self.turn_relay_on(True)
            self.overridden = not over
            return
        if self.current_state != Relay.OFF:
            self.turn_relay_off(True)
            self.overridden = not over
            return

    def turn_relay_on(self, override=False):
        if not override and self.current_state != Relay.ON and self.overridden:
            return
        self.overridden = override


        if self.current_state != Relay.ON:
            GPIO.output(self.pin, GPIO.LOW)
        self.current_state = Relay.ON

    def turn_relay_off(self, override=False):
        if not override and  self.current_state != Relay.OFF and self.overridden:
            return

        self.overridden = override
        if self.current_state != Relay.OFF:
            GPIO.output(self.pin, GPIO.HIGH)
        self.current_state = Relay.OFF

class VirtualRelay(object):
    OFF = 0
    ON = 1
    FOFF = 2
    FON = 3
    UNKNOWN = 4

    def __init__(self, name="virtualrelay"):
        super(VirtualRelay, self).__init__()
        self.name = name
        self.current_state = VirtualRelay.UNKNOWN

    def init(self):
        self.turn_relay_off()

    def current_pos(self):
        s = ""
        if self.current_state == VirtualRelay.ON:
            s = "ON"
        if self.current_state == VirtualRelay.OFF:
            s = "OFF"
        return s

    def toggle(self):
        if self.current_state != VirtualRelay.ON:
            self.turn_relay_on()
            return
        if self.current_state != VirtualRelay.OFF:
            self.turn_relay_off()
            return

    def turn_relay_on(self):
        self.current_state = VirtualRelay.ON

    def turn_relay_off(self):
        self.current_state = VirtualRelay.OFF

