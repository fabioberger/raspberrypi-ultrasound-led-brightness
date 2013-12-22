#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# Define pin 11 as the ultrasound pin
GPIO_SIG = 11

def getAndPrint():

    # Endlessly measure
    while(True):
        measurementInCM()

    # Reset GPIO settings
    GPIO.cleanup()


def measurementInCM():

    # setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)

    GPIO.output(GPIO_SIG, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(GPIO_SIG, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIO_SIG, GPIO.LOW)
    start = time.time()

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG) == 0:
        start = time.time()

    while GPIO.input(GPIO_SIG) == 1:
        stop = time.time()

    measurementPulse(start, stop)


def measurementPulse(start, stop):

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    outfile = open('/dev/pi-blaster','w')

    # Calculate an LED brightness value between 0 and 1
    percent = (distance * 2) / 100.0

    # If more then 1 meter away, default to full brightness
    if(percent > 1):
        percent = 1.0

    # Prepare string to be written to /dev/pi-blaster
    # i.e "0=0.8\n"
    val = "0="+str(percent)+"\n"
    
    outfile.write(val)
    outfile.close()

    print "Distance : %.1f CM" % distance




if __name__ == '__main__':
    # rpi board gpio or bcm gpio
    GPIO.setmode(GPIO.BOARD)

    # loop method
    getAndPrint()