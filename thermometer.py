#!/usr/bin/python
# -*- coding: utf-8 -*-
# HD44780 LCD Script for Raspberry Pi

import RPi.GPIO as GPIO
import time
import re
import os
import glob
import time

os.system('modprobe w1-gpio')  # load one wire communication device modules
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

def read_temp_raw(i):
   device_file = device_folders[i] + '/w1_slave'
   f = open(device_file, 'r')
   lines = f.readlines()
   f.close()
   return lines

def read_temp(i):
      lines = read_temp_raw(i)
      while lines[0].strip()[-3:] != 'YES':             # ignore first line
         print ""
      lines = read_temp_raw(i)
      equals_pos = lines[1].find('t=')         # find temperature in the details
      if equals_pos != -1:
         temp_string = lines[1][equals_pos+2:]
         temp_c = float(temp_string) / 1000.0            # convert to Celsius
         return "%.1f" % temp_c

# Define GPIO to LCD mapping
LCD_RS = 21
LCD_E  = 20
LCD_D4 = 6
LCD_D5 = 13
LCD_D6 = 12
LCD_D7 = 16
 
# Define some device constants
LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 
 
# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
 
def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)  
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)  
 
def lcd_string(message):
    # Send string to display
    message = message.ljust(LCD_WIDTH,) 
 
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True for character
    #        False for command
 
    GPIO.output(LCD_RS, mode) # RS
 
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)
 
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)     
    GPIO.output(LCD_E, True)    
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)   
    time.sleep(E_DELAY)         
 
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)
 
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)     
    GPIO.output(LCD_E, True)    
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)   
    time.sleep(E_DELAY)
     
def main():
     
    # Main program block
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT) # E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
    # Initialise display
    lcd_init()
    while True:
    	temps = []
    	for i in range(len(device_folders)):
            temps.append(read_temp(i))
        # Send some text
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("Hey Babe! %s" % temps[0])
        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("%s %s" % (temps[1], temps[2]))
        print(temps[0], temps[1], temps[2])
	time.sleep(1)
 
if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      GPIO.cleanup()
