import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import serial

class PololuMicroMaestro(object):
    def __init__(self, port= "/dev/ttyACM0"):
        self.ser = serial.Serial(port = port)
    def setAngle(self, channel, angle):
        minAngle = 0.0
        maxAngle = 1000.0
        minTarget = 256.0
        maxTarget = 13120.0
        scaledValue = int((angle / ((maxAngle - minAngle) / (maxTarget - minTarget))) + minTarget)
        commandByte = chr(0x84)
        channelByte = chr(channel)
        lowTargetByte = chr(scaledValue & 0x7F)
        highTargetByte = chr((scaledValue >> 7) & 0x7F)
        command = commandByte + channelByte + lowTargetByte + highTargetByte
        self.ser.write(command)
        self.ser.flush()
    def close(self):
        self.ser.close()

class BoxesGame(ConnectionListener):
    def Network_close(self, data):
        exit()
    def Network_gamepad(self, data):
        global throttle
        global rudder
        global elevator
        global aileron

        global robot

        if data["type"] == 10:
            #print "Pressed button "
            #print data["info"]["button"]
            if data["info"]["button"] == 0:
                throttle = throttle + 10
                if throttle > 675:
                    throttle = 675
                print "Throttle up to"
                print throttle
                robot.setAngle(2, throttle)
            if data["info"]["button"] == 1:
                throttle = throttle - 10
                if throttle < 275:
                    throttle = 275
                print "Throttle down to"
                print throttle
                robot.setAngle(2, throttle)
            if data["info"]["button"] == 5:
                rudder = rudder + 10
                if rudder > 675:
                    rudder = 675
                print "Rudder right to"
                print rudder
                robot.setAngle(3, rudder)
            if data["info"]["button"] == 4:
                rudder = rudder - 10
                if rudder < 275:
                    rudder = 275
                print "Rudder left to"
                print rudder
                robot.setAngle(3, rudder)
            if data["info"]["button"] == 9:
                print "ARMING"
                rudder = 445
                throttle = 275
                robot.setAngle(2, 275) # Throttle down
                robot.setAngle(3, 355) # Rudder left
#                sleep(.1)
#                robot.setAngle(2, throttle)
#                robot.setAngle(3, rudder)
            if data["info"]["button"] == 8:
                print "DISARMING"
                rudder = 445
                throttle = 275
                robot.setAngle(2, 275) # Throttle down
                robot.setAngle(3, 535) # Rudder right
#                sleep(.1)
#                robot.setAngle(2, throttle)
#                robot.setAngle(3, rudder)
            if data["info"]["button"] == 6:
                print "CENTERING"
                rudder = 445
                throttle = 275
                elevator = 445
                aileron = 445
                robot.setAngle(0, elevator)
                robot.setAngle(1, aileron)
                robot.setAngle(2, throttle)
                robot.setAngle(3, rudder) 
            if data["info"]["button"] == 7:
                print "CENTERING"
                rudder = 445
                throttle = 275
                elevator = 445
                aileron = 445
                robot.setAngle(0, elevator)
                robot.setAngle(1, aileron)
                robot.setAngle(2, throttle)
                robot.setAngle(3, rudder) 
        if data["type"] == 9:
            #print "Hat state is "
            #print data["info"]["value"]
            if data["info"]["value"][0] == -1:
                aileron = aileron - 10
                if aileron < 275:
                    aileron = 275
                print "Aileron left to"
                print aileron
                robot.setAngle(1, aileron)
            if data["info"]["value"][0] == 1:
                aileron = aileron + 10
                if aileron > 675:
                    aileron = 675
                print "Aileron right to"
                print aileron
                robot.setAngle(1, aileron)
            if data["info"]["value"][1] == 1:
                elevator = elevator - 10
                if elevator < 275:
                    elevator = 275
                print "Elevator back to"
                print elevator
                robot.setAngle(0, elevator)
            if data["info"]["value"][1] == -1:
                elevator = elevator + 10
                if elevator > 675:
                    elevator = 675
                print "Elevator forward to"
                print elevator
                robot.setAngle(0, elevator)
    def __init__(self):

        address=raw_input("Address of Server: ")
        try:
            if not address:
                host, port="localhost", 8000
            else:
                host,port=address.split(":")
            self.Connect((host, int(port)))
        except:
            print "Error Connecting to Server"
            print "Usage:", "host:port"
            print "e.g.", "localhost:31425"
            exit()
        print "Boxes client started"
        self.running=False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)

global throttle
global rudder
global elevator
global aileron

global robot

throttle = 275
rudder = 445
elevator = 445
aileron = 445

robot = PololuMicroMaestro()

robot.setAngle(0,445)
robot.setAngle(1,445)
robot.setAngle(2,275)
robot.setAngle(3,445)
robot.setAngle(4,0)

bg=BoxesGame() #__init__ is called right here
while 1:
    if bg.update()==1:
        break
bg.finished()
