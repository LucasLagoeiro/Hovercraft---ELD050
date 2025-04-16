from machine import Pin
from time import sleep

class Motor(object):
    
    def __init__(self, pino_b=0,pino_l=0,pino_r=0):
        self.__motor_b = Pin(pino_b,Pin.OUT)
        self.__motor_l = Pin(pino_l,Pin.OUT)
        self.__motor_r = Pin(pino_r,Pin.OUT)
        
        self.__motor_l.value(0)
        self.__motor_r.value(0)
        self.__motor_b.value(0)



    def startRobot(self):
        self.__motor_b.value(1)
        sleep(1)

    def stopRobot(self):
        self.__motor_l.value(0)
        self.__motor_r.value(0)
        self.__motor_b.value(0)
        sleep(1)

    def turnRight(self):
        self.__motor_r.value(1)
        self.__motor_l.value(0)
        sleep(0.1)

    def turnLeft(self):
        self.__motor_r.value(0)
        self.__motor_l.value(1)
        sleep(0.1)

