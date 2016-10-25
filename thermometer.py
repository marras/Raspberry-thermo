#!/usr/bin/python
# -*- coding: utf-8 -*-
import display
import sensor
import RPi.GPIO as GPIO

def handleSuccessfulRead (temps):
    display.println(1, "Hey Babe! %s" % temps[0])
    display.println(2, "%s %s" % (temps[1], temps[2]))
    print(temps[0], temps[1], temps[2])
    time.sleep(1)

def main():
    display.lcd_init()
    while True:
        temps = sensor.read()

        if len(temps) != 3:
            display.println(1, "SENSOR ERROR!")
            display.println(2, "Sensors avail: %d", len(temps))
        else:
            handleSuccessfulRead(temps)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
