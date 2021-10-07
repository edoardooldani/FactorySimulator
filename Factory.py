from pyModbusTCP.server import ModbusServer, DataBank
import time
import socket
from datetime import datetime, timedelta
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import sys


pygame.init()

screenx = 1200
screeny = 800
displayColor = [255, 255, 255]

win = pygame.display.set_mode((screenx, screeny))
win.fill(displayColor)

pygame.display.update()
pygame.display.set_caption("Woolen hats for cats factory")

clock = pygame.time.Clock()


############################################
# SCREEN OBJECTS
############################################


myfont = pygame.font.SysFont('Comic Sans MS', 40)

# MOTOR

textMotor = myfont.render('Engine', False, (0, 0, 0))

motorIcon = pygame.image.load("motor.png")
motorIcon = pygame.transform.scale(motorIcon, (150, 150))
motorIconRect = motorIcon.get_rect()
motorIconRect = motorIconRect.move(30, 500)

motorStatusIcon = pygame.image.load("circleStatus.png")
motorStatusIcon = pygame.transform.scale(motorStatusIcon, (20, 20))
motorStatusIconRect = motorStatusIcon.get_rect()
motorStatusIconRect = motorStatusIconRect.move(30, 450)

# ARROW AFTER MOTOR AND BEFORE CONVEYOR BELT

arrow1Icon = pygame.image.load("arrow.png")
arrow1Icon = pygame.transform.scale(arrow1Icon, (50, 50))
arrow1IconRect = arrow1Icon.get_rect()
arrow1IconRect = arrow1IconRect.move(190, 580)

# CONVEYOR BELT

textConveyorBelt = myfont.render('Conveyor belt', False, (0, 0, 0))

conveyorBeltIcon = pygame.image.load("conveyorBelt.png")
conveyorBeltIcon = pygame.transform.scale(conveyorBeltIcon, (300, 300))
conveyorBeltIconRect = conveyorBeltIcon.get_rect()
conveyorBeltIconRect = conveyorBeltIconRect.move(200, 470)

conveyorBeltStatusIcon = pygame.image.load("circleStatus.png")
conveyorBeltStatusIcon = pygame.transform.scale(conveyorBeltStatusIcon, (20, 20))
conveyorBeltStatusIconRect = conveyorBeltStatusIcon.get_rect()
conveyorBeltStatusIconRect = conveyorBeltStatusIconRect.move(300, 500)

# ARROW AFTER CONVEYOR BELT AND BEFORE WEAVING LOOM

arrow2Icon = pygame.image.load("arrow.png")
arrow2Icon = pygame.transform.scale(arrow2Icon, (50, 50))
arrow2IconRect = arrow2Icon.get_rect()
arrow2IconRect = arrow2IconRect.move(460, 580)

# WEAVING LOOM

textWeavingLoom = myfont.render('Weaving loom', False, (0, 0, 0))

weavingLoomIcon = pygame.image.load("weavingloom.png")
weavingLoomIcon = pygame.transform.scale(weavingLoomIcon, (150, 150))
weavingLoomIconRect = weavingLoomIcon.get_rect()
weavingLoomIconRect = weavingLoomIconRect.move(550, 500)

weavingLoomStatusIcon = pygame.image.load("circleStatus.png")
weavingLoomStatusIcon = pygame.transform.scale(weavingLoomStatusIcon, (20, 20))
weavingLoomStatusIconRect = weavingLoomStatusIcon.get_rect()
weavingLoomStatusIconRect = weavingLoomStatusIconRect.move(550, 450)

# ARROW AFTER WEAVING LOOM AND BEFORE CONVEYOR BELT TO UP

arrow3Icon = pygame.image.load("arrow.png")
arrow3Icon = pygame.transform.scale(arrow3Icon, (50, 50))
arrow3IconRect = arrow3Icon.get_rect()
arrow3IconRect = arrow3IconRect.move(710, 580)

# CONVEYOR BELT TO UP

textConveyorBeltToUp = myfont.render('Conveyor belt', False, (0, 0, 0))

conveyorBeltToUpIcon = pygame.image.load("conveyorToUp.png")
conveyorBeltToUpIcon = pygame.transform.scale(conveyorBeltToUpIcon, (150, 150))
conveyorBeltToUpIconRect = conveyorBeltToUpIcon.get_rect()
conveyorBeltToUpIconRect = conveyorBeltToUpIconRect.move(780, 470)

conveyorBeltToUpStatusIcon = pygame.image.load("circleStatus.png")
conveyorBeltToUpStatusIcon = pygame.transform.scale(conveyorBeltToUpStatusIcon, (20, 20))
conveyorBeltToUpStatusIconRect = conveyorBeltToUpStatusIcon.get_rect()
conveyorBeltToUpStatusIconRect = conveyorBeltToUpStatusIconRect.move(800, 650)

# ARROW AFTER CONVEYOR BELT TO UP AND BEFORE HYDRAULIC PRESS

arrow4Icon = pygame.image.load("arrow.png")
arrow4Icon = pygame.transform.scale(arrow4Icon, (50, 50))
arrow4Icon = pygame.transform.rotate(arrow4Icon, 90)
arrow4IconRect = arrow4Icon.get_rect()
arrow4IconRect = arrow4IconRect.move(880, 420)

# HYDRAULIC PRESS

textHydraulicPress = myfont.render('Hydraulic press', False, (0, 0, 0))

hydraulicPressIcon = pygame.image.load("hydraulicPress.png")
hydraulicPressIcon = pygame.transform.scale(hydraulicPressIcon, (150, 150))
hydraulicPressIconRect = hydraulicPressIcon.get_rect()
hydraulicPressIconRect = hydraulicPressIconRect.move(830, 260)

hydraulicPressStatusIcon = pygame.image.load("circleStatus.png")
hydraulicPressStatusIcon = pygame.transform.scale(hydraulicPressStatusIcon, (20, 20))
hydraulicPressStatusIconRect = hydraulicPressStatusIcon.get_rect()
hydraulicPressStatusIconRect = hydraulicPressStatusIconRect.move(950, 210)

# ARROW AFTER HYDRAULIC PRESS BEFORE CONVEYOR BELT 2

arrow5Icon = pygame.image.load("arrow.png")
arrow5Icon = pygame.transform.scale(arrow5Icon, (50, 50))
arrow5Icon = pygame.transform.rotate(arrow5Icon, 135)
arrow5IconRect = arrow5Icon.get_rect()
arrow5IconRect = arrow5IconRect.move(790, 210)

# CONVEYOR BELT 2

textConveyorBelt2 = myfont.render('Conveyor belt', False, (0, 0, 0))

conveyorBelt2Icon = pygame.image.load("conveyorBelt2.png")
conveyorBelt2Icon = pygame.transform.scale(conveyorBelt2Icon, (200, 200))
conveyorBelt2Icon = pygame.transform.rotate(conveyorBelt2Icon, 335)
conveyorBelt2IconRect = conveyorBelt2Icon.get_rect()
conveyorBelt2IconRect = conveyorBelt2IconRect.move(580, 50)

conveyorBelt2StatusIcon = pygame.image.load("circleStatus.png")
conveyorBelt2StatusIcon = pygame.transform.scale(conveyorBelt2StatusIcon, (20, 20))
conveyorBelt2StatusIconRect = conveyorBelt2StatusIcon.get_rect()
conveyorBelt2StatusIconRect = conveyorBelt2StatusIconRect.move(650, 70)

# ARROW AFTER CONVEYOR BELT 2 AND BEFORE BOX WOOL PIECES

arrow6Icon = pygame.image.load("arrow.png")
arrow6Icon = pygame.transform.scale(arrow6Icon, (50, 50))
arrow6Icon = pygame.transform.rotate(arrow6Icon, 180)
arrow6IconRect = arrow6Icon.get_rect()
arrow6IconRect = arrow6IconRect.move(550, 120)

# BOX WOOL PIECES

textBoxWoolPieces = myfont.render('Woolen pieces box', False, (0, 0, 0))

boxWoolPiecesIcon = pygame.image.load("boxWoolPieces.png")
boxWoolPiecesIcon = pygame.transform.scale(boxWoolPiecesIcon, (150, 150))
boxWoolPiecesIconRect = boxWoolPiecesIcon.get_rect()
boxWoolPiecesIconRect = boxWoolPiecesIconRect.move(410, 50)

# ARROW AFTER WOOL PIECES BOX AND BEFORE BOX WOOLEN HATS

arrow7Icon = pygame.image.load("arrow.png")
arrow7Icon = pygame.transform.scale(arrow7Icon, (50, 50))
arrow7Icon = pygame.transform.rotate(arrow7Icon, 180)
arrow7IconRect = arrow7Icon.get_rect()
arrow7IconRect = arrow7IconRect.move(300, 120)

# BOX WOOLEN HATS

textWoolenHats = myfont.render('Woolen hats made', False, (0, 0, 0))

woolenHatsIcon = pygame.image.load("woolenHat2.jpg")
woolenHatsIcon = pygame.transform.scale(woolenHatsIcon, (150, 150))
woolenHatsIconRect = woolenHatsIcon.get_rect()
woolenHatsIconRect = woolenHatsIconRect.move(80, 50)


#############################################
# SCREEN POSITION
#############################################

# Motor
win.blit(motorIcon, motorIconRect)
win.blit(motorStatusIcon, motorStatusIconRect)
win.blit(textMotor, (30, 410))

win.blit(arrow1Icon, arrow1IconRect)

# Conveyor Belt
win.blit(conveyorBeltIcon, conveyorBeltIconRect)
win.blit(conveyorBeltStatusIcon, conveyorBeltStatusIconRect)
win.blit(textConveyorBelt, (300, 460))

win.blit(arrow2Icon, arrow2IconRect)

# Weaving loom
win.blit(weavingLoomIcon, weavingLoomIconRect)
win.blit(weavingLoomStatusIcon, weavingLoomStatusIconRect)
win.blit(textWeavingLoom, (550, 400))

win.blit(arrow3Icon, arrow3IconRect)

# Conveyor belt to up
win.blit(conveyorBeltToUpIcon, conveyorBeltToUpIconRect)
win.blit(conveyorBeltToUpStatusIcon, conveyorBeltToUpStatusIconRect)
win.blit(textConveyorBeltToUp, (800, 690))

win.blit(arrow4Icon, arrow4IconRect)

# Hydraulic Press
win.blit(hydraulicPressIcon, hydraulicPressIconRect)
win.blit(hydraulicPressStatusIcon, hydraulicPressStatusIconRect)
win.blit(textHydraulicPress, (950, 170))

win.blit(arrow5Icon, arrow5IconRect)

#Conveyor belt 2
win.blit(conveyorBelt2Icon, conveyorBelt2IconRect)
win.blit(conveyorBelt2StatusIcon, conveyorBelt2StatusIconRect)
win.blit(textConveyorBelt2, (650, 30))

win.blit(arrow6Icon, arrow6IconRect)

#Woolen pieces box
win.blit(boxWoolPiecesIcon, boxWoolPiecesIconRect)

numberOfPiecesFont = pygame.font.SysFont('Comic Sans MS', 40)
textNumberOfWoolPieces = numberOfPiecesFont.render(str(0), True, (0, 0, 0)) 
rect = textNumberOfWoolPieces.get_rect()
rect = rect.move(490, 130)
win.blit(textNumberOfWoolPieces, rect)

def set_numberOfWoolPieces(number):
    
    win.fill(displayColor, (490, 130, 40, 42))
    numberOfPiecesFont = pygame.font.SysFont('Comic Sans MS', 40)
    textNumberOfWoolPieces = numberOfPiecesFont.render(str(number), True, (0, 0, 0)) 
    rect = textNumberOfWoolPieces.get_rect()
    rect = rect.move(490, 130)
    win.blit(textNumberOfWoolPieces, rect)

win.blit(arrow7Icon, arrow7IconRect)

#Woolen hats made
win.blit(woolenHatsIcon, woolenHatsIconRect)

numberOfHatsFont = pygame.font.SysFont('Comic Sans MS', 40)
textNumberOfWoolenHats = numberOfHatsFont.render(str(0), True, (0, 0, 0)) 
rectHats = textNumberOfWoolenHats.get_rect()
rectHats = rectHats.move(50, 50)
win.blit(textNumberOfWoolenHats, rectHats)

def set_numberOfWoolenHats(number):
    
    win.fill(displayColor, (50, 50, 40, 42))
    numberOfHatsFont = pygame.font.SysFont('Comic Sans MS', 40)
    textNumberOfWoolenHats = numberOfHatsFont.render(str(number), True, (0, 0, 0)) 
    rectHats = textNumberOfWoolenHats.get_rect()
    rectHats = rectHats.move(50, 50)
    win.blit(textNumberOfWoolenHats, rectHats)


############################################
# BACK END START
############################################



# Setting starting values for products

def startingValues():
 
    woolReady = [0]
    woolenHatsCompleted = [0]

    DataBank.set_words(14, woolReady)
    DataBank.set_words(15, woolenHatsCompleted)


# Start the engine

def startProcess(firstProcess):

    # Starting values

    conveyorBeltStatus = [1]
    motorStatus = [1]
    weavingLoomStatus = [1]
    hydraulicPressStatus = [1]

    # Setting registers

    DataBank.set_words(10, conveyorBeltStatus)
    DataBank.set_words(11, motorStatus)
    DataBank.set_words(12, weavingLoomStatus)
    DataBank.set_words(13, hydraulicPressStatus)

    if firstProcess:
        startingValues()

    
# Stop the engine but keep products

def stopProcess():
    
    conveyorBeltStatus = [0]
    motorStatus = [0]
    weavingLoomStatus = [0]
    hydraulicPressStatus = [0]

    DataBank.set_words(10, conveyorBeltStatus)
    DataBank.set_words(11, motorStatus)
    DataBank.set_words(12, weavingLoomStatus)
    DataBank.set_words(13, hydraulicPressStatus)



########################################
# SERVER START
########################################

# Finding our IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

# Setting the variables
port = 12345
server = ModbusServer(ip, port,  no_block=True)


# Start the server and listen to register changing, then stop the server
try:
    print('Start server with ip address: ' + ip + ' at port ' + str(port))
    server.start()
    print('Server online')

    # Registers set and declaration
    
    processState = [0]
    resetState = [0]
    connectionState = [0]
    DataBank.set_words(0, connectionState)
    DataBank.set_words(1, processState)
    DataBank.set_words(2, resetState)

    firstProcess = True
    zeroTime = datetime.min
    startProcessTime = zeroTime
    startProcessHatTime = zeroTime
    exitFlag = False

    while not exitFlag:

        # Window settings

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitFlag = True
                break

        # If Connection status register's changes

        if connectionState != DataBank.get_words(0):

            connectionState = DataBank.get_words(0)
            print('Connection state has changed to ' + str(connectionState))

        # If Process status register's value changes

        if processState != DataBank.get_words(1):

            processState = DataBank.get_words(1)
            print('Process state has changed to ' + str(processState))
        
            if processState == [1]:
                startProcess(firstProcess)
                startProcessTime = datetime.now()

                if DataBank.get_words(14)[0] > 0:
                    startProcessHatTime = datetime.now()
               
            else:
                stopProcess() 
                startProcessTime = zeroTime
                startProcessHatTime = zeroTime

            firstProcess = False

        # If Reset register's value changes

        if resetState != DataBank.get_words(2):

            resetState = DataBank.get_words(2)
            print('Reset state has changed to ' + str(resetState))

            if resetState == [1]:
                startProcess(True)
                stopProcess()
                startProcessTime = zeroTime
                startProcessHatTime = zeroTime
                set_numberOfWoolPieces(0)
                set_numberOfWoolenHats(0)
            
            resetState = [0]
            DataBank.set_words(2, resetState)

        
        # Checking the status of each machine

        enginesRegs = list(DataBank.get_words(10, 4))

        if enginesRegs[0] == 1:
            win.fill(pygame.Color(0, 255 ,0), conveyorBeltStatusIconRect)
            win.fill(pygame.Color(0, 255 ,0), conveyorBelt2StatusIconRect)
            win.fill(pygame.Color(0, 255 ,0), conveyorBeltToUpStatusIconRect)

        else:
            startProcessTime = zeroTime
            win.fill(pygame.Color(255, 0 ,0), conveyorBeltStatusIconRect)
            win.fill(pygame.Color(255, 0 ,0), conveyorBelt2StatusIconRect)
            win.fill(pygame.Color(255, 0 ,0), conveyorBeltToUpStatusIconRect)
            
        if enginesRegs[1] == 1:
            win.fill(pygame.Color(0, 255 ,0), motorStatusIconRect)
        else:
            startProcessTime = zeroTime
            win.fill(pygame.Color(255, 0 ,0), motorStatusIconRect)

        if enginesRegs[2] == 1:
            win.fill(pygame.Color(0, 255 ,0), weavingLoomStatusIconRect)
        else:
            startProcessTime = zeroTime
            win.fill(pygame.Color(255, 0 ,0), weavingLoomStatusIconRect)

        if enginesRegs[3] == 1:
            win.fill(pygame.Color(0, 255 ,0), hydraulicPressStatusIconRect)
        else:
            startProcessTime = zeroTime
            win.fill(pygame.Color(255, 0 ,0), hydraulicPressStatusIconRect)


        # If the factory is working

        if enginesRegs[0] == 1 and enginesRegs[1] == 1 and enginesRegs[2] == 1 and enginesRegs[3] == 1 and startProcessTime > zeroTime:
        
            timeToProductPiece = startProcessTime + timedelta(seconds=5)

            # If it is passed enough time to product a piece of wool

            if datetime.now() > timeToProductPiece:
                newWoolPiecesValue = DataBank.get_words(14)[0] + 1
                listWoolPiecesToSet = [newWoolPiecesValue]
                DataBank.set_words(14, listWoolPiecesToSet)
            
                startProcessTime = datetime.now()

                # Set new wool pieces on graphics
                set_numberOfWoolPieces(newWoolPiecesValue)

                if startProcessHatTime == zeroTime:
                    startProcessHatTime = datetime.now()

            timeToProductHat = startProcessHatTime + timedelta(seconds=15)
            woolPieces = DataBank.get_words(14)[0]

            # If it is passed enough time to product a woolen hat

            if datetime.now() > timeToProductHat and woolPieces > 0:

                newWoolenHatsValue = DataBank.get_words(15)[0] + 1

                listWoolenHatsToSet = [newWoolenHatsValue]
                DataBank.set_words(15, listWoolenHatsToSet)
                set_numberOfWoolenHats(newWoolenHatsValue)

                woolPieces -= 1
                set_numberOfWoolPieces(woolPieces)

                listWoolPiecesToSet = [woolPieces]
                DataBank.set_words(14, listWoolPiecesToSet)

                if woolPieces > 0:
                    startProcessHatTime = datetime.now()
                else:
                    startProcessHatTime = zeroTime

        
        time.sleep(0.5)
        pygame.display.update()
    
    print("Planned server shutdown")
    pygame.quit()
    stopProcess()
    DataBank.set_words(0, [0])
    time.sleep(1)        # We give client(s) the time to get the new data
    server.stop()
    print('Server is offline')


except:
    print('Unplanned server shutdown')
    server.stop()
    print('Server is offline')

