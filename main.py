from motor import Motor
from time import sleep

robot = Motor(4,5,18)
robot.startRobot()
try:
    while True:
        robot.turnLeft()
        sleep(2)
        robot.turnRight()
        sleep(2)

except:
    robot.stopRobot()

