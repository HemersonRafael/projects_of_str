# -*- coding: utf-8 -*-
#
# AUTHOR: IRAN MACEDO AND RICARDO CAVALCANTI 31/08/2018
#
# THIS GAME WAS MADE FOR ME (@IRANNETO) AND @RICAVALCANTI AT UFRN AT THE COURSE OF REAL-TIME SYSTEMS
# 
# UPDATING: HEMERSON RAFAEL AND RAFAEL GARCIA 06/10/2020
# THIS VERSION REMOVE BUGS AND ADDING THE BIPES TOGETHER  THE LEDS
#

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import random
import os

buzzer = "P9_14"
leds = ["P8_13", "P8_14", "P8_15", "P8_16", "P8_17"]
buttons = ["P8_7", "P8_8", "P8_9", "P8_10", "P8_11"]
               #  do,  re,  mi,  fa, sol
musical_notes = [262, 294, 330, 349, 392]

game_sequence = []
player_sequence = []

current_round = 1
game_started = False

for x in range(5):
    GPIO.setup(buttons[x], GPIO.IN)
    GPIO.setup(leds[x], GPIO.OUT)
    GPIO.add_event_detect(buttons[x], GPIO.FALLING)

def blink(mn, led, seconds):
    GPIO.output(led, GPIO.HIGH)
    PWM.start(buzzer, 50, mn, 1)
    time.sleep(seconds)

    GPIO.output(led, GPIO.LOW)
    PWM.stop(buzzer)
    PWM.cleanup()
    time.sleep(seconds)

def blink_all(seconds):
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
    time.sleep(seconds)

    for led in leds:
        GPIO.output(led, GPIO.LOW)
    time.sleep(seconds)

def flag():
    for x in range (0, 4):
        blink(musical_notes[x],leds[x], 0.5)

def generate_current_round():
    #Start with 1 led e add more one every round
    #for cont in range(0,current_round):
    current_led = random.randint(0,3)
    game_sequence.append(current_led)
    for count in game_sequence:
        blink(musical_notes[count], leds[count],0.5)
        #add leds in the sequence 
        #    
def click(num):
    player_sequence.append(num)
    print("B"+ str(num))
    blink(musical_notes[num],leds[num], 0.125)

def get_play():
    if(current_round > 1):
        del player_sequence[:]
    
    number_of_plays = 0
    play_time_begin = time.time() #Return the number of seconds since epoch
    play_time_end = time.time()
    # Player got 3 seconds for every led in the sequence on every round 
    while((play_time_end - play_time_begin) < current_round + 3):

        if(GPIO.input(buttons[0])):
            click(0)
            number_of_plays += 1

        if(GPIO.input(buttons[1])):
            click(1)
            number_of_plays += 1

        if(GPIO.input(buttons[2])):
            click(2)
            number_of_plays += 1

        if(GPIO.input(buttons[3])):
            click(3)
            number_of_plays += 1

        play_time_end = time.time()
        if(number_of_plays == current_round):
            break
    if(number_of_plays < current_round):
        print("Game Over")
        while not GPIO.input(buttons[4]):
            blink(musical_notes[4], leds[4], 0.1)

def validate_current_round():
    if(len(player_sequence) !=len(game_sequence)):
        return(False)
    else:
        for i in range(0,current_round):
            if(player_sequence[i] != game_sequence[i]):
                return(False)
    return(True)


print("__________________Game Genius__________________\n")
print("Press any button to start\n")

while True:
    #Press any button to start 
    
    while(GPIO.input(buttons[0]) or GPIO.input(buttons[1]) or GPIO.input(buttons[2]) or GPIO.input(buttons[3]) or GPIO.input(buttons[4])):
        #Show some standart sequence
        flag()    
        #flag game_started
        game_started = True
        #Game loop
        while game_started:
            print("Round: " + str(current_round))
            generate_current_round()    
            
            #Detect player's play
            get_play()

            #TO DEBUG
            print(game_sequence)
            print(player_sequence)

            if(not(validate_current_round())):
                print("Game Over")
                while not GPIO.input(buttons[4]):
                    blink(musical_notes[4], leds[4], 0.1)
                game_sequence = []
                player_sequence = []
                current_round = 0
                game_started = False

            blink_all(0.5)
            current_round += 1
        os.system("reset")
        print("__________________Game Genius__________________\n")
        print("Press any button to start\n")
        break
