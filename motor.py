from machine import PWM
from time import sleep

class Motor(object):
    
    def __init__(self, pino_b=0,pino_l=0,pino_r=0):
        self.__motor_b = PWM(pino_b, freq=20000, duty = 0)
        self.__motor_l = PWM(pino_l, freq=20000, duty = 0)
        self.__motor_r = PWM(pino_r, freq=20000, duty = 0)
                
        
        self.__motor_l.duty(0)
        self.__motor_r.duty(0)
        self.__motor_b.duty(0)



    def startMotors(self):
         for duty in range(1024):
           if duty < 440: duty = duty + 440
           self.__motor_b.duty(duty)
           sleep(0.005)

    def stopMotors(self):
        self.__motor_l.duty(440)
        self.__motor_r.duty(440)
        for duty in range(1023,440,-1):
           self.__motor_b.duty(duty)
           sleep(0.005)

    def standyMode(self):        
        self.__motor_l.duty(0)
        self.__motor_r.duty(0)


    def goFoward(self,duty):
        if duty < 440: duty = duty + 440
        self.__motor_l.duty(duty)
        self.__motor_r.duty(duty)

    def turnRight(self,duty):
        if duty < 440: duty = duty + 440
        self.__motor_r.duty(duty)
        self.__motor_l.duty(0)

    def turnLeft(self,duty):
        if duty < 440: duty = duty + 440
        self.__motor_r.duty(0)
        self.__motor_l.duty(duty)







