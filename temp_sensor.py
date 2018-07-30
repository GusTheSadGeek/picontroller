#!/usr/bin/python

import debug
import time

import logging


class TempSensor(object):
    def __init__(self, name, sensor, test):
        super(TempSensor, self).__init__()
        self.name = name
        self.test = test
        self.sensor = sensor
        self._current_temp = self._read_temp()

    @staticmethod
    def new(name="temp", sensor='', test=False):
        return TempSensor(name, sensor, test)

    def test_temp(self):
        """
        Provides Test Values
        """
        if self.name.startswith('tank'):
            return 20.5
        else:
            return 24.5

    @property
    def current_value(self):
        return self._current_temp

    def get_new_relay_state(self, onval=None, offval=None):
        """
        Return the state the controlled object should be in according to passed in values
        """
        if onval is None or offval is None:
            return 0

        if onval > offval:
            if self._current_temp >= onval:
                return 1
            if self._current_temp < offval:
                return -1
        else:
            if self._current_temp <= onval:
                return 1
            if self._current_temp > offval:
                return -1
        return 0

    # Override base
    def tick(self):
        self._read_temp()

    def _get_temp_raw(self):
        try:
            with open(self.sensor, 'r') as f:
                lines = f.readlines()
        except IOError:
            lines = None
            logging.error("Failed to read sensor {f}".format(f=self.sensor))
        return lines

    def _read_temp(self):
        if self.test:
            self._current_temp = self.test_temp()
        else:
            lines = self._get_temp_raw()
            if lines:
                while lines is not None and lines[0].strip()[-3:] != 'YES':
                    time.sleep(0.2)
                    lines = self._get_temp_raw()

                temp_output = lines[1].find('t=')
                if temp_output != -1:
                    temp_string = lines[1].strip()[temp_output+2:]
                    self._current_temp = float(temp_string) / 1000.0
        return self._current_temp
