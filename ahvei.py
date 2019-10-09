import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
enable_pin = 17    
in_1_pin = 18
in_2_pin = 27

xenable_pin = 24    
xin_1_pin = 22
xin_2_pin = 23

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(in_1_pin, GPIO.OUT)
GPIO.setup(in_2_pin, GPIO.OUT)
motor_pwm = GPIO.PWM(enable_pin, 500)
motor_pwm.start(0)
 
GPIO.setup(xenable_pin, GPIO.OUT)
GPIO.setup(xin_1_pin, GPIO.OUT)
GPIO.setup(xin_2_pin, GPIO.OUT)
xmotor_pwm = GPIO.PWM(xenable_pin, 500)
xmotor_pwm.start(0)

GPIO.output(in_1_pin, False)
GPIO.output(in_2_pin, True)
motor_pwm.ChangeDutyCycle(75)
GPIO.output(xin_1_pin, True)
GPIO.output(xin_2_pin, False)
xmotor_pwm.ChangeDutyCycle(50)
time.sleep(10)   

