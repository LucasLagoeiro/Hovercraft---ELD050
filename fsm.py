from motor import Motor

robotOFF  = 0
turnON    = 1
robotON   = 2
turnLeft  = 3
turnRight = 4
goFoward  = 5
turnOff   = 6


class FSM_Robot(object):

    def __init__(self):
        self.state = robotOFF
        self.robot = Motor(18,19,21)
        

    def update(self,start_btn,stop_btn,foward_btn,yaw_btn):
        if self.state == robotOFF:
            print("Robot is off")
            if start_btn == 1:
                print("Will turn ON")
                self.state = turnON

        elif self.state == turnON:
            print("turn ON the robot")
            self.robot.startMotors()
            self.state = robotON
        
        elif self.state == robotON:
            print("Robot is ON")
            # Press R2 to go foward with the robot
            if foward_btn > 0:
                self.state = goFoward

            # Use the left joystick to control the yaw of the robot
            elif yaw_btn > 0:
                self.state = turnRight

            elif yaw_btn < 0:
                self.state = turnLeft
                

            # Press share button to stop the robot
            elif stop_btn == 1:
                self.state = turnOff

            # if you dont do any command the robot will enter in standy Mode
            else:
                self.robot.standyMode()


        elif self.state == goFoward:
            print("Robot is going foward")
            self.robot.goFoward(foward_btn)
            if foward_btn == 0:
                self.state = robotON


        elif self.state == turnLeft:
            print("Robot is turning left")
            self.robot.turnLeft(abs(yaw_btn))
            if yaw_btn == 0:
                self.state = robotON

        elif self.state == turnRight:
            print("Robot is turning right")
            self.robot.turnRight(abs(yaw_btn))
            if yaw_btn == 0:
                self.state = robotON

        elif self.state == turnOff:
            print("Robot is turning off")
            self.robot.stopMotors()
            self.state = robotOFF
        
        print(self.state)








