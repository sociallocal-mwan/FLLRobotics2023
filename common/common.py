from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import *
from math import *

def LineFollowing_incomplete():
    count = 0

    while count < 200:
        print (count)
        print("light: {}".format(left_eye.get_reflected_light()))
        #when see white
        if (left_eye.get_reflected_light()>80 and right_eye.get_reflected_light()>80):
            left.start_at_power(-25)
            right.start_at_power (0)
        #when see black
        else:
            right.start_at_power(25)
            left.start_at_power(0)       
        count +=1    
    


#stanley's perfect turn 
#don't go above 175 or below -175
def turn(target_number):
    left.start_at_power(5)
    right.start_at_power(5)
    print (hub.motion_sensor.get_yaw_angle())
    if hub.motion_sensor.get_yaw_angle()>target_number:
        #motor_pair.start(steering=20)
        motor_pair.start_tank(-25,25)
        wait_until(hub.motion_sensor.get_yaw_angle, less_than, target_number)
        motor_pair.stop()
    else :
        motor_pair.start_tank(25,-25)
        wait_until(hub.motion_sensor.get_yaw_angle, greater_than, target_number)
        motor_pair.stop()

hub.motion_sensor.reset_yaw_angle()
#turn(175)
print (hub.motion_sensor.get_yaw_angle())

# stanley's perfect gryo straight spike prime wheel we are using is 56 mm in diameter
def gyro_straight(length, desired_yaw):
    right.set_degrees_counted(0)
   # degree is a variable I defined. the equation tells means degrees is equal to (length*360)/(56*pi)
   # 56 times pi is the circumfrence. 
    degree= (length*360)/(56*3.141592)
    print (degree)
    motor_pair.start(steering=0, speed=10)
    #this loops until the desired length is reached
    while(right.get_degrees_counted()<degree):
        #correction is how much degrees is away from the desired angle; 0.75 is the scale factor. For example, if you increase the number there will be a larger correction made.
        correction=int((hub.motion_sensor.get_yaw_angle()-desired_yaw)*0.75)
        motor_pair.start_tank(50-correction, 50+correction)
        #print (right.get_degrees_counted())
        print (correction)
    
    motor_pair.stop()

# Simple stop-at-line using reflective sensor
def stop_at_line():
    wait_for_seconds(1)
    motor_pair.start(0,30)
    while right_eye.get_reflected_light()>50 and left_eye.get_reflected_light(50):
        pass
    motor_pair.stop()

    if right_eye.get_reflected_light()<50:
        motor_pair.start(50,20)
        while(left_eye.get_reflected_light()>50):
            pass
        motor_pair.stop()
    else:
        motor_pair.start(-50,20)
        while(left_eye.get_reflected_light()>50):
            pass
        motor_pair.stop()
