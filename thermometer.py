#!/usr/bin/python
# -*- coding: utf-8 -*-
import display
import sensor
import time
import requests
import json
import hashlib
import RPi.GPIO as GPIO

signing_code = ''

def handleSuccessfulRead (temps):
    display.println(1, "Hey Babe! %s" % temps[0])
    display.println(2, "%s %s" % (temps[1], temps[2]))
    print(temps[0], temps[1], temps[2])
    data = {'Temp1': temps[0], 'Temp2': temps[1], 'Temp3': temps[2]}
    doc_to_sign = json.dumps(data, separators=(',',':')) + signing_code
    signature = hashlib.md5(doc_to_sign).hexdigest()
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://lab-monitor.herokuapp.com/data', data = json.dumps({"values": data, "signature": signature}), headers=headers)
    if r.status_code != 200:
        print "Failed to send data to server! %s" % r.text
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
	f = open('signing_code')
	signing_code = f.read().rstrip()
	f.close()
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
