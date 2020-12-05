#!/usr/bin/env python3
from threading import Thread, Lock
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import sys


ADC.setup()

mutex_l3 = Lock()
mutex_l5 = Lock()
mutex_l4 = Lock()
mutex_l6 = Lock()
mutex_l10 = Lock()

debug = 0
adc = 0.5

rail_1 = [1,2,3,4]
rail_2 = [7,5,6,3]
rail_3 = [8,9,10,5]
rail_4 = [13,11,4,6,10,12]

led_rail_1 = ["P8_11","P8_12","P8_14","P8_15"]
led_rail_2 = ["P8_16","P8_17","P8_18","P8_26"]
led_rail_3 = ["P9_12","P9_17","P9_18","P9_41"]
led_rail_4 = ["P8_25","P8_20","P9_23","P9_15","P9_27","P8_30"]

def set_gpio_out(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

set_gpio_out(led_rail_1)
set_gpio_out(led_rail_2)
set_gpio_out(led_rail_3)
set_gpio_out(led_rail_4)


def led_on_sequence_four(pins, s_type):
    if s_type == "HLLL":
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)

    elif s_type == "LHLL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.HIGH)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)

    elif s_type == "LLHL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.HIGH)
        GPIO.output(pins[3], GPIO.LOW)

    elif s_type == "LLLH":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.HIGH)


def led_on_sequence_six(pins, s_type):
    if s_type == "HLLLLL":
        GPIO.output(pins[0], GPIO.HIGH)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)
        GPIO.output(pins[4], GPIO.LOW)
        GPIO.output(pins[5], GPIO.LOW)

    elif s_type == "LHLLLL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.HIGH)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)
        GPIO.output(pins[4], GPIO.LOW)
        GPIO.output(pins[5], GPIO.LOW)

    elif s_type == "LLHLLL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.HIGH)
        GPIO.output(pins[3], GPIO.LOW)
        GPIO.output(pins[4], GPIO.LOW)
        GPIO.output(pins[5], GPIO.LOW)

    elif s_type == "LLLHLL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.HIGH)
        GPIO.output(pins[4], GPIO.LOW)
        GPIO.output(pins[5], GPIO.LOW)

    elif s_type == "LLLLHL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)
        GPIO.output(pins[4], GPIO.HIGH)
        GPIO.output(pins[5], GPIO.LOW)

    elif s_type == "LLLLLL":
        GPIO.output(pins[0], GPIO.LOW)
        GPIO.output(pins[1], GPIO.LOW)
        GPIO.output(pins[2], GPIO.LOW)
        GPIO.output(pins[3], GPIO.LOW)
        GPIO.output(pins[4], GPIO.LOW)
        GPIO.output(pins[5], GPIO.LOW)


def train1_function():
    global adc

    while True:
        for l in rail_1:
            time.sleep(adc)
            if l == 3:
                if (mutex_l3.locked() or mutex_l6.locked()) and debug:
                    print('t1 esperando l3 ficar livre')
                while mutex_l3.locked() or mutex_l6.locked():
                    pass
                if debug:
                    print('t1 encontrou l3 livre')
                mutex_l3.acquire()
            if l == 4:
                if mutex_l4.locked() and debug:
                    print('t1 esperando l4 ficar livre')
                while mutex_l4.locked() == True:
                    pass
                if debug:
                    print('t1 encontrou l4 livre')
                mutex_l4.acquire()
                if mutex_l3.locked():
                    if debug:
                        print('t1 liberou l3')
                    mutex_l3.release()
            if l == 1:
                if mutex_l4.locked():
                    if debug:
                        print('t1 liberou l4')
                    mutex_l4.release()
            print('t1: ' + str(l))
            if l == 1:
                led_on_sequence_four(led_rail_1, "HLLL")
            if l == 2:
                led_on_sequence_four(led_rail_1, "LHLL")
            if l == 3:
                led_on_sequence_four(led_rail_1, "LLHL")
            if l == 4:
                led_on_sequence_four(led_rail_1, "LLLH")


def train2_function():
    global adc

    while True:
        for l in rail_2:
            time.sleep(adc)
            if l == 3:
                if mutex_l3.locked() and debug:
                    print('t2 esperando l3 ficar livre')
                while mutex_l3.locked() == True:
                    pass
                if debug:
                    print('t2 encontrou l3 livre')
                mutex_l3.acquire()
                if mutex_l6.locked():
                    if debug:
                        print('t2 liberou l6')
                    mutex_l6.release()
            if l == 6:
                if (mutex_l6.locked() or mutex_l3.locked() or mutex_l4.locked()) and debug:
                    print('t2 esperando l6 ficar livre')
                while mutex_l6.locked() or mutex_l3.locked() or mutex_l4.locked():
                    pass
                if debug:
                    print('t2 encontrou l6 livre')
                mutex_l6.acquire()
                if mutex_l5.locked():
                    if debug:
                        print('t2 liberou l5')
                    mutex_l5.release()
            if l == 5:
                if (mutex_l5.locked() or mutex_l10.locked()) and debug:
                    print('t2 esperando l5 ficar livre')
                while mutex_l5.locked() or mutex_l10.locked():
                    pass
                if debug:
                    print('t2 encontrou l5 livre')
                mutex_l5.acquire()
            if l == 7:
                if mutex_l3.locked():
                    if debug:
                        print('t2 liberou l3')
                    mutex_l3.release()
            print('t2: ' + str(l))
            if l == 3:
                led_on_sequence_four(led_rail_2, "HLLL")
            if l == 7:
                led_on_sequence_four(led_rail_2, "LHLL")
            if l == 5:
                led_on_sequence_four(led_rail_2, "LLHL")
            if l == 6:
                led_on_sequence_four(led_rail_2, "LLLH")


def train3_function():
    global adc

    while True:
        for l in rail_3:
            time.sleep(adc)
            if l == 5:
                if mutex_l5.locked() and debug:
                    print('t3 esperando l5 ficar livre')
                while mutex_l5.locked() == True:
                    pass
                if debug:
                    print('t3 encontrou l5 livre')
                mutex_l5.acquire()
                if mutex_l10.locked():
                    if debug:
                        print('t3 liberou l10')
                    mutex_l10.release()
            if l == 10:
                if (mutex_l10.locked() or mutex_l5.locked() or mutex_l6.locked() or mutex_l4.locked()) and debug:
                    print('t3 esperando l10 ficar livre')
                while mutex_l10.locked() or mutex_l5.locked() or mutex_l6.locked() or mutex_l4.locked():
                    pass
                if debug:
                    print('t3 encontrou l10 livre')
                mutex_l10.acquire()
            if l == 8:
                if mutex_l5.locked():
                    if debug:
                        print('t3 liberou l5')
                    mutex_l5.release()
            print('t3: ' + str(l))
            if l == 5:
                led_on_sequence_four(led_rail_3, "HLLL")
            if l == 8:
                led_on_sequence_four(led_rail_3, "LHLL")
            if l == 9:
                led_on_sequence_four(led_rail_3, "LLHL")
            if l == 10:
                led_on_sequence_four(led_rail_3, "LLLH")


def train4_function():
    global adc

    while True:
        for l in rail_4:
            time.sleep(adc)
            if l == 4:
                if mutex_l4.locked() and debug:
                    print('t4 esperando l4 ficar livre')
                while mutex_l4.locked() == True:
                    pass
                if debug:
                    print('t4 encontrou l4 livre')
                mutex_l4.acquire()
            if l == 6:
                if mutex_l6.locked() and debug:
                    print('t4 esperando l6 ficar livre')
                while mutex_l6.locked() == True:
                    pass
                if debug:
                    print('t4 encontrou l6 livre')
                mutex_l6.acquire()
                if mutex_l4.locked():
                    if debug:
                        print('t4 liberou l4')
                    mutex_l4.release()
            if l == 10:
                if mutex_l10.locked() and debug:
                    print('t4 esperando l10 ficar livre')
                while mutex_l10.locked() == True:
                    pass
                if debug:
                    print('t4 encontrou l10 livre')
                mutex_l10.acquire()
                if mutex_l6.locked():
                    if debug:
                        print('t4 liberou l6')
                    mutex_l6.release()
            if l == 12:
                if mutex_l10.locked():
                    if debug:
                        print('t4 liberou l10')
                    mutex_l10.release()
            print('t4: ' + str(l)) 
            if l == 13:
                led_on_sequence_six(led_rail_4,"HLLLLL")
            if l == 11:
                led_on_sequence_six(led_rail_4,"LHLLLL")
            if l == 4:
                led_on_sequence_six(led_rail_4,"LLHLLL")
            if l == 6:
                led_on_sequence_six(led_rail_4,"LLLHLL")
            if l == 10:
                led_on_sequence_six(led_rail_4,"LLLLHL")
            if l == 12:
                led_on_sequence_six(led_rail_4,"LLLLLL")


def read_ADC_function():
    while True:
        global adc
        adc = ADC.read("P9_40")
        time.sleep(0.1)

def main():
    t1 = Thread(target = train1_function)
    t1.start()
    t2 = Thread(target = train2_function)
    t2.start()
    t3 = Thread(target = train3_function)
    t3.start()
    t4 = Thread(target = train4_function)
    t4.start()

    f5 = Thread(target = read_ADC_function)
    f5.start()

if __name__ == '__main__':
    main()
    sys.exit(0)
