#!/usr/bin/python
# -*- coding: utf-8 -*-
import display
import sensor
from time import gmtime, strftime, sleep
import requests
import json
import hashlib
import RPi.GPIO as GPIO
from requests.exceptions import ConnectionError

signing_code = ''
sleep_time = 0
tunnel = ""

def getNgrokTunnel():
    global tunnel
    try:
         r = requests.get('http://localhost:4040/api/tunnels')
         tunnel = json.loads(r.text)['tunnels'][0]['public_url']
    except ConnectionError:
	 tunnel = "No active tunnel!"
	 log("Ngrok not running yet.")
    except IndexError:
	 log("Failed to parse Ngrok API response")
	 tunnel = "No active tunnel!"
    log("Tunnel: %s" % tunnel)

def log(*args):
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print timestamp, args

def handleSuccessfulRead (temps):
    global tunnel
    display.println(1, "%s %s %s" % tuple(temps))
    display.println(2, "Status: OK :)")
    log(temps[0], temps[1], temps[2])
    data = {'Temp1': temps[0], 'Temp2': temps[1], 'Temp3': temps[2]}
    doc_to_sign = json.dumps(data, separators=(',',':')) + signing_code
    signature = hashlib.md5(doc_to_sign).hexdigest()
    headers = {'Content-Type': 'application/json'}
    try:
        r = requests.post('http://150.254.80.131/data', data = json.dumps({"values": data, "signature": signature, "tunnel": tunnel}), headers=headers)
        if r.status_code != 200:
            log("Failed to send data to server! %s" % r.text)
    except ConnectionError as ex:
        log("Cannot connect to server! Error: %s" % ex)

def main():
    display.lcd_init()

    measurement_number = 0

    while True:
	# Refresh Ngrok data every 10 measurements
	if measurement_number % 10 == 0:
	    getNgrokTunnel()

        temps = sensor.read()

        if len(temps) != 3:
            display.println(1, "SENSOR ERROR!")
            display.println(2, "Sensors avail: %d" % len(temps))
            log("Error: only %d sensors available!" % len(temps))
        else:
            handleSuccessfulRead(temps)

	sleep(sleep_time)
	measurement_number += 1

if __name__ == '__main__':
    try:
	f = open('signing_code')
	signing_code = f.read().rstrip()
	f.close()
	f = open('sleep_time')
	sleep_time = int(f.read().rstrip())
	f.close()
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
