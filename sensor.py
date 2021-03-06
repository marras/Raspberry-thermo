#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import glob

os.system('modprobe w1-gpio')  # load one wire communication device modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

# Expose sensor IDs
def ids():
    return [folder.replace(base_dir, '') for folder in device_folders]

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

def read():
    return [read_temp(i) for i in range(len(device_folders))]
