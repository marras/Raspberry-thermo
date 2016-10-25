#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import os
import glob
import display
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')  # load one wire communication device modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

# Read output from a thermometer
def read_temp_raw(i):
    device_file = device_folders[i] + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Extract temperature data
def read_temp(i):
    lines = read_temp_raw(i)
    while lines[0].strip()[-3:] != 'YES':   # ignore first line
        print ""
    lines = read_temp_raw(i)
    equals_pos = lines[1].find('t=')        # find temperature in the details
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0  # convert to Celsius
        return "%.1f" % temp_c

def main():
    display.lcd_init()
    while True:
        temps = []
        for i in range(len(device_folders)):
            temps.append(read_temp(i))

        # Send some text
        display.println(1, "Hey Babe! %s" % temps[0])
        display.println(2, "%s %s" % (temps[1], temps[2]))
        print(temps[0], temps[1], temps[2])
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
