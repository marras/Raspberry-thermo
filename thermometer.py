#!/usr/bin/python
# -*- coding: utf-8 -*-
import display
import sensor
import time
import requests
import json
import RPi.GPIO as GPIO

def handleSuccessfulRead (temps):
    display.println(1, "Hey Babe! %s" % temps[0])
    display.println(2, "%s %s" % (temps[1], temps[2]))
    print(temps[0], temps[1], temps[2])
    data = {'values': {'Temp1': temps[0], 'Temp2': temps[1], 'Temp3': temps[2]} }
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://lab-monitor.herokuapp.com/data', data = json.dumps(data), headers=headers)
    time.sleep(1)

def main():
    display.lcd_init()
    while True:
        temps = sensor.read()

        if len(temps) != 3:
            display.println(1, "SENSOR ERROR!")
            display.println(2, "Sensors avail: %d" % len(temps))
            print "Error: only %d sensors available!" % len(temps)
        else:
            handleSuccessfulRead(temps)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
