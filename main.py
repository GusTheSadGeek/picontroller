#!/usr/bin/env python

import datetime
import temp_sensor
import time
import relay
import sys
import timer


def fermenter():
    sensorAir = temp_sensor.TempSensor.new(sensor='/sys/bus/w1/devices/28-041501b016ff/w1_slave')

    pinList = [33,35,37]
    r0 = relay.Relay(pinList[0])

    r0.init()

    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+60

        sensorAir.tick()

        if sensorAir.current_value < 21.75:
            if relay_state == 0:
                relay_state = 1
                r0.turn_relay_on()

        if sensorAir.current_value > 22.00 or last_temp < sensorAir.current_value:
            relay_state = 0
            r0.turn_relay_off()

        last_temp = sensorAir.current_value

        timestamp = datetime.datetime.utcnow().isoformat('T')+"000Z"

        l = "{t}\ttemp:{r}\trelay:{r0}".format(t=timestamp, r=sensorAir.current_value,
                                                            r0=r0.current_state)

        log_fname = r'/var/log/picontroller/log'
        try:
            with open(log_fname, 'a') as f:
                f.write("{log}\n".format(log=l))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(log_fname)


def fishtank():
    sensorAir = temp_sensor.TempSensor.new(sensor="/sys/bus/w1/devices/28-0014117fb1ff/w1_slave")
    sensorTank = temp_sensor.TempSensor.new(sensor="/sys/bus/w1/devices/28-00000676eb5f/w1_slave")

    pinList = [11, 13, 15, 16]
    r0 = relay.Relay(pinList[0])
    r1 = relay.Relay(pinList[1])

    r0.init()
    r1.init()

    t0 = timer.Timer().set(timer.S3,timer.S3,timer.S3,timer.S3,timer.S3,timer.S5,timer.S5)
    t1 = timer.Timer().set(timer.S4,timer.S4,timer.S4,timer.S4,timer.S4,timer.S6,timer.S6)


    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+60

        sensorAir.tick()
        sensorTank.tick()

        if t0.on():
            r0.turn_relay_on()
        else:
            r0.turn_relay_off()

        if t1.on():
            r1.turn_relay_on()
        else:
            r1.turn_relay_off()

        timestamp = datetime.datetime.utcnow().isoformat('T')+"000Z"

        l = "{t}\troom:{r}\ttank:{w}\tlight0:{r0}\tline1:{r1}".format(t=timestamp,
                                                                      r=sensorAir.current_value,
                                                                      w=sensorTank.current_value,
                                                                      r0=r0.current_state,
                                                                      r1=r1.current_state)

        log_fname = r'/var/log/picontroller/log'
        try:
            with open(log_fname, 'a') as f:
                f.write("{log}\n".format(log=l))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(log_fname)

def shrimp():
    sensorAir = temp_sensor.TempSensor.new(sensor="/sys/bus/w1/devices/28-0315019a7bff/w1_slave")
    sensorTank = temp_sensor.TempSensor.new(sensor="/sys/bus/w1/devices/28-041501af2dff/w1_slave")



    pinList = [31,33,35,37]
    r_heater = relay.Relay(pinList[0])
    r_fan = relay.Relay(pinList[1])
    r_light = relay.Relay(pinList[2])
    r_xmas = relay.Relay(pinList[3])

    r_heater.init()
    r_fan.init()
    r_light.init()
    r_xmas.init()

    t_lights = timer.Timer().set(timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1)
    t_xmas = timer.Timer().set(timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1)

    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+60

        sensorAir.tick()
        sensorTank.tick()

        # FAN
        if sensorTank.current_value > 22.8:
            r_fan.turn_relay_on()
        if sensorTank.current_value < 22.5:
            r_fan.turn_relay_off()

        # HEATER
        if sensorTank.current_value > 22.5:
            r_fan.turn_relay_off()
        if sensorTank.current_value < 22.3:
            r_fan.turn_relay_on()

        # LIGHT
        if t_lights.on():
            r_light.turn_relay_on()
        else:
            r_light.turn_relay_off()

        # XMAS Lights
        if t_xmas.on():
            r_xmas.turn_relay_on()
        else:
            r_xmas.turn_relay_off()

        timestamp = datetime.datetime.utcnow().isoformat('T')+"000Z"

        l = "{t}\troom:{r}\ttank:{w}\tlight:{r0}\tfan:{r1}\theater:{r2}\txmas:{r3}".format(t=timestamp,
                                                                                          r=sensorAir.current_value,
                                                                                          w=sensorTank.current_value,
                                                                                          r0=r_light.current_state,
                                                                                          r1=r_fan.current_state,
                                                                                          r2=r_heater.current_state,
                                                                                          r3=r_xmas.current_state)

        log_fname = r'/var/log/picontroller/log'
        try:
            with open(log_fname, 'a') as f:
                f.write("{log}\n".format(log=l))
        except IOError as e:
            print str(e)
            print "Error writing to temp file {f}".format(log_fname)


def garage():
    pass

def main():
    if len(sys.argv) > 1:
        OPTION = sys.argv[1]

        if OPTION == "FISH":
            fishtank()

        if OPTION == "SHRIMP":
            shrimp()

        if OPTION == "FERMENTER":
            fermenter()

        if OPTION == "GARAGE":
            garage()

    return 1


if __name__ == '__main__':
    main()

