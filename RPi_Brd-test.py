#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel
# Modified on date:2021-03-21
# Import necessary libraries for communication and display use
import drivers
from time import sleep
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15 as ADS
import Adafruit_DHT


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
output_channel = [18,23,24,25,8,26] #Led pin numbers
GPIO.setup(output_channel, GPIO.OUT,initial=GPIO.LOW)
input_channel = [4,20,21]
GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setmode(GPIO.BCM)


#GPIO.setup(output_channel, GPIO.OUT,initial=GPIO.LOW)
# Or create an ADS1015 ADC (12-bit) instance.
adc = ADS.ADS1015()

display = drivers.Lcd()
display.lcd_backlight(1)
display.lcd_display_string("ADC value is:",1)

dB_lvl = 10**(-5/20) #5dB per step
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#>left, <righ & ^centered 
print('| {0:>6} | {1:<6} | {2:^6} | {3:>6} |'.format(*range(4)))
print('-' * 37) #print * 37 times
# Main loop.
try:
     while True:          # Read all the ADC channel values in a list.
         values = [0]*4
         for i in range(4):
            # Read the specified ADC channel using the previously set gain value.
             values[i] = adc.read_adc(i, gain=GAIN)
         print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
        #display.lcd_clear()
         display.lcd_display_string("           ",2)
         display.lcd_display_string(("      "+str(values[1])),2)#Adc i/p ch
         # Pause for half a second.
         GPIO.output(output_channel,GPIO.LOW)
        #LED light up by sound level
         if values[2]> 38:
            GPIO.output(18,GPIO.HIGH)
         if values[2] > 191:
            GPIO.output(23,GPIO.HIGH)
         if values[2] > 372:
            GPIO.output(24,GPIO.HIGH)  
         if values[2] > 455:#555
            GPIO.output(25,GPIO.HIGH)
         if values[2] > 600:
            GPIO.output(8,GPIO.HIGH)#750
         if GPIO.input(20)==0:
            GPIO.output(26, True)
         if GPIO.input(21)==0:
            GPIO.output(8, True)   
         if values[3] < 500:
            GPIO.output(26,GPIO.HIGH)           
            
        #if values[1]>(1600*(dB_lvl**4)):
         #  GPIO.output(output_channel[4],GPIO.HIGH)
        #if values[1]>(1600*(dB_lvl**3)):
          #  GPIO.output(output_channel[3],GPIO.HIGH)
        #if values[1]>(1600*(dB_lvl**2)):
         #   GPIO.output(output_channel[2],GPIO.HIGH)
        #if values[1]>(1600*dB_lvl):
          #  GPIO.output(output_channel[1],GPIO.HIGH)
        #if values[1]>1600:
          #  GPIO.output(output_channel[0],GPIO.HIGH)
           
         time.sleep(0.5)
   
    
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_display_string("THE END!!       ",1)
    display.lcd_display_string("Cleaning up!!",2)
    time.sleep(1)
    #GPIO.cleanup()
    display.lcd_clear()
    display.lcd_backlight(0)
