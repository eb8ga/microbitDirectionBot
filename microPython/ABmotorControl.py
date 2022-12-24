from microbit import *
from time import sleep_us
from machine import time_pulse_us
import neopixel

class RINGBIT(object):

    def __init__(self, left_wheel_pin=pin1, right_wheel_pin=pin2):

        i2c.init()
        self.__left_wheel_pin = left_wheel_pin
        self.__right_wheel_pin = right_wheel_pin
        self.__right_wheel_pin.set_analog_period(10)
        self.__left_wheel_pin.set_analog_period(10)
        self.__module_pin = pin0
        if self.__left_wheel_pin != pin1 and self.__right_wheel_pin != pin1:
            self.__module_pin = pin1
        if self.__left_wheel_pin != pin2 and self.__right_wheel_pin != pin2:
            self.__module_pin = pin2

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):

        if left_wheel_speed > 100 or left_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        if right_wheel_speed > 100 or right_wheel_speed < -100:
            raise ValueError('select motor error,1,2,3,4')
        if left_wheel_speed > 0:
            left_wheel_speed = ((left_wheel_speed - 0) *
                                (256 - 153.6)) / (100 - 0) + 153.6
            self.__left_wheel_pin.write_analog(left_wheel_speed)
        elif left_wheel_speed < 0:
            left_wheel_speed = ((left_wheel_speed - 0) *
                                (51.2 - 153.6)) / (-100 - 0) + 153.6
            self.__left_wheel_pin.write_analog(left_wheel_speed)
        else:
            self.__left_wheel_pin.write_analog(153.6)

        right_wheel_speed = right_wheel_speed * -1
        if right_wheel_speed > 0:
            right_wheel_speed = ((right_wheel_speed - 0)
                                 * (256 - 153.6)) / (100 - 0) + 153.6
            self.__right_wheel_pin.write_analog(right_wheel_speed)
        elif right_wheel_speed < 0:
            right_wheel_speed = ((right_wheel_speed - 0)
                                 * (51.2 - 153.6)) / (-100 - 0) + 153.6
            self.__right_wheel_pin.write_analog(right_wheel_speed)
        else:
            self.__right_wheel_pin.write_analog(153.6)

def stop():
	RB.set_motors_speed(0, 0)
	np[0] = (255, 0, 0)
	np[1] = (255, 0, 0)
	np.show()
	display.show(stopSign)
	sleep(1000)

def forward():
	RB.set_motors_speed(100, 100)
	np[0] = (0, 255, 0)
	np[1] = (0, 255, 0)
	np.show()
	display.show(Image.ARROW_S)
	sleep(880) #one tire revolution
	stop()

def leftTurn():
	RB.set_motors_speed(-100,100)
	np[0] = (0, 255, 0)
	np[1] = (0, 255, 0)
	np.show()
	display.show(Image.ARROW_E)
	sleep(380) #90 deg turn
	stop()

def rightTurn():
	RB.set_motors_speed(100,-100)
	np[0] = (0, 255, 0)
	np[1] = (0, 255, 0)
	np.show()
	display.show(Image.ARROW_W)
	sleep(380)
	stop()

def reverse():
	RB.set_motors_speed(-100,-100)
	np[0] = (0, 255, 0)
	np[1] = (0, 255, 0)
	np.show()
	display.show(Image.ARROW_N)
	sleep(1000)
	stop()

mode = 0
menuitem = 0
menu_options = [Image.ARROW_N, Image.ARROW_S, Image.ARROW_W, Image.ARROW_E]
dir_options = [reverse, forward, rightTurn, leftTurn]

def scrollmenu(direction):
	global menuitem
	menuitem
	menuitem += direction
	if menuitem < 0:
		menuitem +=len(menu_options)
	elif menuitem >= len(menu_options):
		menuitem = menuitem - len(menu_options)
	display.show(menu_options[menuitem])

stopSign = Image("09990:" "77077:" "90009:" "77077:" "09990:")
checkSymbol = Image("0000:" "00009:" "00090:" "90900:" "09000:")

RB = RINGBIT(pin1, pin2)
np = neopixel.NeoPixel(pin0, 2)
recorded_button = []
i = 0

while True:
# pressing A and B at same time clears the recorded program
	if button_a.is_pressed() and button_b.is_pressed():
		sleep(1000)		
		display.scroll("Clear")		
		del recorded_button[:]
		display.show(checkSymbol)
		sleep(500)
		display.clear()
# pressing A scrolls through the options
	elif button_a.was_pressed():
		if mode == 0:
			scrollmenu(1)
		elif mode == 1:
			pass
		elif mode == 2:
			pass
# pressing B selects the direction and adds it to the sequence in the program
	elif button_b.was_pressed():
		recorded_button.append(dir_options[menuitem])
		sleep(60)
# shake the microbit to start the recorded program
	if accelerometer.was_gesture("shake"):
		if recorded_button == []:
			display.scroll("No program!")
		else:
			display.scroll("3..2..1..GO!")
			while i < len(recorded_button):
				recorded_button[i]()
				i = i + 1			
			display.clear()
# cannot use the neopixels from ringbit at same time as speaker v2			
			np[0] = (0, 0, 0)
			np[1] = (0, 0, 0)
			np.show()
#			audio.play(Sound.TWINKLE)
#			sleep(2000)
#		else:
#			stop()