#!/usr/bin/python

import hcsr04sensor.sensor as sensor
import time


class DistSensor(object):
    def __init__(self,  tempsensor, echo_pin, trig_pin, tank_depth=80, name="distance"):
        super(DistSensor, self).__init__()
        self.name = name
        self.echo_pin = echo_pin
        self.trig_pin = trig_pin
        self.tank_depth = tank_depth
        self._tempsensor = tempsensor
        self._current_dist = 100.0
        self._action_interval = 20
        self._next_read_time = 0  # self.time_next_action()

    @staticmethod
    def new(tempsensor, echo_pin,trig_pin, tank_depth=80, name="dist"):
        return DistSensor(tempsensor, echo_pin,trig_pin, tank_depth, name)

    @property
    def current_value(self):
        return self._current_dist

    # Override base
    def tick(self):
         now = time.time()
         if now >= self._next_read_time:
             self._get_distance()
             self._next_read_time = self.time_next_action()

    def _get_distance(self):
        round_to = 1
        temperature = self._tempsensor.current_value
        self._error_count = 0
        value = sensor.Measurement(self.trig_pin, self.echo_pin, temperature, 'metric', round_to)
        raw_distance = value.raw_distance()

        # If tank depth is defined then give a water depth
        if self.tank_depth is not None:
            water_depth = value.depth_metric(raw_distance, self.tank_depth)
            if water_depth < 0:
                water_depth = 0.0
            self._current_dist = water_depth
        else:
            # otherwise give a distance to water surface
            self._current_dist = raw_distance
        # logging.info("{x}".format(x=self._current_dist))

