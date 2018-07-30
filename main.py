#!/usr/bin/env python

import datetime
import temp_sensor
import dist_sensor
import time
import relay
import sys
import timer
import log
import webserver

def fermenter():
    logger = log.RotatingFile("/var/log/picontroller/logs")

    sensorAir = temp_sensor.TempSensor.new(name='temp', sensor='/sys/bus/w1/devices/28-041501b016ff/w1_slave')

    pinList = [33,35,37]
    r0 = relay.Relay(pinList[0])
    r0.init()

    webserver.temps.append(sensorAir)
    webserver.relays.append(r0)

    webserver.start_server()

    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+6

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

        l = "time:{t}\ttemp:{r}\trelay:{r0}".format(t=timestamp, r=sensorAir.current_value,
                                                            r0=r0.current_state)

        logger.log(l)


def fishtank():
    logger = log.RotatingFile("/var/log/picontroller/logs")

    sensorAir = temp_sensor.TempSensor.new(name="Room",sensor="/sys/bus/w1/devices/28-0014117fb1ff/w1_slave")
    sensorTank = temp_sensor.TempSensor.new(name="Tank", sensor="/sys/bus/w1/devices/28-00000676eb5f/w1_slave")

    pinList = [11, 13, 15, 16]
    r0 = relay.Relay(pin=pinList[0],name="Relay1")
    r1 = relay.Relay(pin=pinList[1],name="Relay2")

    r0.init()
    r1.init()

    t0 = timer.Timer('Light1')
    t0.set(timer.S3,timer.S3,timer.S3,timer.S3,timer.S3,timer.S5,timer.S5)
    t1 = timer.Timer('Light2')
    t1.set(timer.S4,timer.S4,timer.S4,timer.S4,timer.S4,timer.S6,timer.S6)

    webserver.temps.append(sensorAir)
    webserver.temps.append(sensorTank)
    webserver.relays.append(r0)
    webserver.relays.append(r1)
    webserver.timers.append(t0)
    webserver.timers.append(t1)

    webserver.start_server()

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

        l = "time:{t}\troom:{r}\ttank:{w}\tlight0:{r0}\tline1:{r1}".format(t=timestamp,
                                                                      r=sensorAir.current_value,
                                                                      w=sensorTank.current_value,
                                                                      r0=r0.current_state,
                                                                      r1=r1.current_state)

        logger.log(l)

def shrimp():
    logger = log.RotatingFile("/var/log/picontroller/logs")

    sensorAir = temp_sensor.TempSensor.new(name='Room', sensor="/sys/bus/w1/devices/28-0315019a7bff/w1_slave")
    sensorTank = temp_sensor.TempSensor.new(name='Tank', sensor="/sys/bus/w1/devices/28-041501af2dff/w1_slave")

    pinList = [31,33,35,37]
    r_heater = relay.Relay(pin=pinList[0],name='Heater')
    r_fan = relay.Relay(pin=pinList[1],name='Fan')
    r_light = relay.Relay(pin=pinList[2],name='Light')
    r_xmas = relay.Relay(pin=pinList[3],name='XMAS')

    r_heater.init()
    r_fan.init()
    r_light.init()
    r_xmas.init()

    t_lights = timer.Timer("Lights")
    t_lights.set(timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1)
    t_xmas = timer.Timer("XMAS")
    t_xmas.set(timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1,timer.S1)

    webserver.temps.append(sensorAir)
    webserver.temps.append(sensorTank)
    webserver.relays.append(r_heater)
    webserver.relays.append(r_fan)
    webserver.relays.append(r_light)
    webserver.relays.append(r_xmas)
    webserver.timers.append(t_lights)
    webserver.timers.append(t_xmas)

    webserver.start_server()

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

        l = "time:{t}\troom:{r}\ttank:{w}\tlight:{r0}\tfan:{r1}\theater:{r2}\txmas:{r3}".format(t=timestamp,
                                                                                          r=sensorAir.current_value,
                                                                                          w=sensorTank.current_value,
                                                                                          r0=r_light.current_state,
                                                                                          r1=r_fan.current_state,
                                                                                          r2=r_heater.current_state,
                                                                                          r3=r_xmas.current_state)

        logger.log(l)


def garage():
    logger = log.RotatingFile("/var/log/picontroller/logs")

    sensorAir = temp_sensor.TempSensor.new(name='AirTemp', sensor="/sys/bus/w1/devices/28-041501b3a6ff/w1_slave")
    sensorTank = temp_sensor.TempSensor.new(name='TankTemp', sensor="/sys/bus/w1/devices/28-041501ad96ff/w1_slave")
    sensorDist = dist_sensor.DistSensor.new(sensorTank, echo_pin=13,trig_pin=11, tank_depth=82, name="WaterLevel")

    pinList = [31,33,35,37]
    r_airpump = relay.Relay(pin=pinList[0],name='Airpump')
    r_heater2 = relay.Relay(pin=pinList[1],name='Heater2')
    r_heater = relay.Relay(pin=pinList[2],name='Heater')
    r_valve = relay.Relay(pin=pinList[3],name='Valve')

    r_Active = relay.VirtualRelay(name='Active')

    r_heater.init()
    r_airpump.init()
    r_heater2.init()
    r_valve.init()

    t_airpump = timer.Timer("Airpump")
    t_airpump.set(timer.S10,timer.S10,timer.S10,timer.S10,timer.S10,timer.S10,timer.S10)

    webserver.temps.append(sensorAir)
    webserver.temps.append(sensorTank)
    webserver.dists.append(sensorDist)
    webserver.relays.append(r_heater)
    webserver.relays.append(r_airpump)
    webserver.relays.append(r_heater2)
    webserver.relays.append(r_valve)
    webserver.relays.append(r_Active)
    webserver.timers.append(t_airpump)

    webserver.start_server()

    now = 0
    while True:
        while time.time() < now:
            time.sleep(1)
        now = time.time()+60

        sensorAir.tick()
        sensorTank.tick()
        sensorDist.tick()

        # VALVE
        if r_Active.current_state == relay.Relay.ON:
            if sensorDist.current_value < 55:
                r_valve.turn_relay_on()
            if sensorDist.current_value > 62:
                r_valve.turn_relay_off()

            # HEATER
            if sensorTank.current_value > 22:
                r_heater.turn_relay_off()
            if sensorTank.current_value < 21:
                r_heater.turn_relay_on()
        else:
            r_heater.turn_relay_off()
            r_valve.turn_relay_off()

        # AIRPUMP
        if t_airpump.on():
            r_airpump.turn_relay_on()
        else:
            r_airpump.turn_relay_off()

        timestamp = datetime.datetime.utcnow().isoformat('T')+"000Z"
        l = "time:{t}\tairtemp:{r}\ttanktemp:{w}\twater:{d}\twatervalve:{r0}\tairpump:{r1}\theater1:{r2}\theater2:{r3}\tactive:{a}".\
            format(t=timestamp,
            r=sensorAir.current_value,
            w=sensorTank.current_value,
            d=sensorDist.current_value,
            r0=r_valve.current_state,
            r1=r_airpump.current_state,
            r2=r_heater.current_state,
            r3=r_heater2.current_state,
            a=r_Active.current_state)
        logger.log(l)

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
    try:
        main()
    except KeyboardInterrupt:
        print("SHUTTING DOWN")
    finally:
        webserver.stop_server()

