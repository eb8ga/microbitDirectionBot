from microbit import *
import time
import machine

#using continuous servos as main driving mechanism, balancing without any encoders, use class:
#

class servoDrive(object):

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
#specific motor control functions
def stop():
	motors1.set_motors_speed(0, 0)
	display.show(stopSign)
	sleep(1000)

def forward():
	motors1.set_motors_speed(100, 100)
	display.show(Image.ARROW_N)
	sleep(1800) #one tire revolution
	stop()

def leftTurn():
	motors1.set_motors_speed(-100,100)
	display.show(Image.ARROW_W)
	sleep(880) #90 deg turn
	stop()

def rightTurn():
	motors1.set_motors_speed(100,-100)
	display.show(Image.ARROW_E)
	sleep(880)
	stop()

def reverse():
	motors1.set_motors_speed(-100,-100)
	display.show(Image.ARROW_S)
	sleep(1800)
	stop()
#custom symbols for LED display
stopSign = Image("09990:" "77077:" "90009:" "77077:" "09990:")
checkSymbol = Image("0000:" "00009:" "00090:" "90900:" "09000:")
#motor setup
motors1 = servoDrive(pin1, pin2)
#array to store directions when entered
recorded_button = []
i = 0
#pin assignments not interacting with MB buttons, i2c, or LED array on V2
stopButton = pin9
playButton = pin8
forwardButton = pin13
reverseButton = pin14
leftButton = pin16
rightButton = pin15

dButtons = [pin13, pin14, pin16, pin15]
#pull up resistors on all pins
stopButton.set_pull(stopButton.PULL_UP)
playButton.set_pull(playButton.PULL_UP)
forwardButton.set_pull(forwardButton.PULL_UP)
reverseButton.set_pull(reverseButton.PULL_UP)
leftButton.set_pull(leftButton.PULL_UP)
rightButton.set_pull(rightButton.PULL_UP)

#setting initial button states for comparison of pressing
buttonState1 = 0
lastState1 = 0
buttonState2 = 0
lastState2 = 0
buttonState3 = 0
lastState3 = 0
buttonState4 = 0
lastState4 = 0

while True:
# read direction button states
	sleep(50)
#!!!need to condense into for loop for scanning!!
	buttonState1 = forwardButton.read_digital()
	buttonState2 = reverseButton.read_digital()
	buttonState3 = leftButton.read_digital()
	buttonState4 = rightButton.read_digital()
# pressing red button clears the program and stops the robot
	if stopButton.read_digital() == 0:
		sleep(20)
		stop()
		sleep(1000)		
		del recorded_button[:]
		display.show(checkSymbol)
		sleep(1000)
		display.clear()
		reset()
# pressing pins to record each movement
# !!!need to condense into IPO function!!!
	elif buttonState1 != lastState1:
		if buttonState1 == 0:
			recorded_button.append(forward)
		sleep(50)
		lastState1 = buttonState1
	elif buttonState2 != lastState2:
		if buttonState2 == 0:
			recorded_button.append(reverse)
		sleep(50)
		lastState2 = buttonState2
	elif buttonState3 != lastState3:
		if buttonState3 == 0:
			recorded_button.append(leftTurn)
		sleep(50)
		lastState3 = buttonState3
	elif buttonState4 != lastState4:
		if buttonState4 == 0:
			recorded_button.append(rightTurn)
		sleep(50)
		lastState4 = buttonState4
# start the recorded program
	elif playButton.read_digital() == 0:
		sleep(20)
		if recorded_button != []:
			display.scroll("GO!")
			while i < len(recorded_button):
				recorded_button[i]()
				i = i + 1			
			display.clear()
			del recorded_button[:]
			audio.play(Sound.TWINKLE)
			sleep(2000)
			reset() #!!!need to address reset issue and count button presses vs. reset!!!
		else:
			display.scroll("No program!")