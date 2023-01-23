#!/usr/bin/env python3
import random

from config import *
import RPi.GPIO as GPIO
import time

greenButtonClicked = False


def buttonRedPressedCallback(channel):
    print("Statystyki...")


def buttonGreenPressedCallback(channel):
    global greenButtonClicked
    greenButtonClicked = True
    global position
    global board
    board[position] = 1
    print("send chosen position to opponent")


def randomOrder():
    return random.randint(1, 2)


def encoderLeft():
    global position
    global board
    while board[position] != 0:
        if position == 0:
            position = 8
        else:
            position -= 1


def encoderRight():
    global position
    global board
    while board[position] != 0:
        if position == 8:
            position = 0
        else:
            position += 1


def resetPointer():
    global position
    position = 8
    encoderRight()


def myTurn():
    global greenButtonClicked
    greenButtonClicked = False

    encoderLeftPreviousState = GPIO.input(encoderLeft)
    encoderRightPreviousState = GPIO.input(encoderRight)

    while not greenButtonClicked:
        encoderLeftCurrentState = GPIO.input(encoderLeft)
        encoderRightCurrentState = GPIO.input(encoderRight)

        if encoderLeftPreviousState == 1 and encoderLeftCurrentState == 0:
            encoderLeft()
        if encoderRightPreviousState == 1 and encoderRightCurrentState == 0:
            encoderRight()

        print("set moved pointer on oled")
        encoderLeftPreviousState = encoderLeftCurrentState
        encoderRightPreviousState = encoderRightCurrentState


def opponentsTurn():
    while 1:
        print("checking for opponents move"
              "get position"
              "board[position] = -1")
        time.sleep(1)


def checkForWin():
    for i in [-1, 1]:

        # Three in a row
        if i == board[0] == board[1] == board[2]:
            return i
        if i == board[3] == board[4] == board[5]:
            return i
        if i == board[6] == board[7] == board[8]:
            return i

        if i == board[0] == board[3] == board[6]:
            return i
        if i == board[1] == board[4] == board[7]:
            return i
        if i == board[2] == board[5] == board[8]:
            return i

        # Diagonals
        if i == board[0] == board[4] == board[8]:
            return i
        if i == board[2] == board[4] == board[6]:
            return i

        return 0


def run():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonRedPressedCallback, bouncetime=200)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=buttonGreenPressedCallback, bouncetime=200)
    order = randomOrder()
    turn = 1

    while 1:
        resetPointer()
        if turn % 2 == 0:
            opponentsTurn()
        else:
            myTurn()

        result = checkForWin()
        if result != 0:
            return result

        if turn == 9:
            return 0
        turn += 1


if __name__ == "__main__":
    while 1:
        board = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ]
        position = 0
        run()
        print("add win and lose to stats based on run() return")
