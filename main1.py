#!/usr/bin/env python3
import random
import lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont

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
    board[position] = -1
    print("send chosen position to opponent")


def encoderRight():
    global position
    global board
    if position == 0:
        position = 8
    else:
        position -= 1
    while board[position] != 0:
        if position == 0:
            position = 8
        else:
            position -= 1


def encoderLeft():
    global position
    global board
    if position == 8:
        position = 0
    else:
        position += 1
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

    while not greenButtonClicked:
        print(position)
        displayBoard()


def opponentsTurn():
    while 1:
        print("checking for opponents move"
              "get position"
              "board[position] = 1")
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


def displayBoard():
    global board
    global position
    disp = SSD1331.SSD1331()

    # Initialize library.
    disp.Init()

    # disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 15)

    # Create lines
    draw.line([(0, 21), (95, 21)], fill="BLACK", width=5)
    draw.line([(0, 42), (95, 42)], fill="BLACK", width=5)
    draw.line([(32, 0), (32, 63)], fill="BLACK", width=5)
    draw.line([(64, 0), (64, 63)], fill="BLACK", width=5)

    # fill
    for i in range(3):
        if board[i] == 1:
            draw.text((12 + i * 32, 0), 'X', font=fontLarge, fill="BLACK")

        elif (board[i] == -1):
            draw.text((12 + i * 32, 0), 'O', font=fontLarge, fill="BLACK")

    for i in range(3, 6):
        if board[i] == 1:
            draw.text((12 + (i - 3) * 32, 21), 'X', font=fontLarge, fill="BLACK")

        elif (board[i] == -1):
            draw.text((12 + (i - 3) * 32, 21), 'O', font=fontLarge, fill="BLACK")

    for i in range(6, 9):
        if board[i] == 1:
            draw.text((12 + (i - 6) * 32, 42), 'X', font=fontLarge, fill="BLACK")

        elif (board[i] == -1):
            draw.text((12 + (i - 6) * 32, 42), 'O', font=fontLarge, fill="BLACK")

    # currentPosision
    if (position == 0):
        draw.rectangle([(0, 0), (32, 21)], fill="BLUE")
    elif (position == 1):
        draw.rectangle([(32, 0), (64, 21)], fill="BLUE")
    elif (position == 2):
        draw.rectangle([(64, 0), (95, 21)], fill="BLUE")
    elif (position == 3):
        draw.rectangle([(0, 21), (32, 42)], fill="BLUE")
    elif (position == 4):
        draw.rectangle([(32, 21), (64, 42)], fill="BLUE")
    elif (position == 5):
        draw.rectangle([(64, 21), (95, 42)], fill="BLUE")
    elif (position == 6):
        draw.rectangle([(0, 42), (32, 63)], fill="BLUE")
    elif (position == 7):
        draw.rectangle([(32, 42), (64, 63)], fill="BLUE")
    elif (position == 8):
        draw.rectangle([(64, 42), (95, 63)], fill="BLUE")

    disp.ShowImage(image1, 0, 0)
    # time.sleep(1)


def leftPinCallback(channel):
    if GPIO.input(27) == 0:
        # global my_diode
        encoderLeft()


def rightPinCallback(channel):
    if GPIO.input(17) == 0:
        # global my_diode
        encoderRight()


def run():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonRedPressedCallback, bouncetime=200)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=buttonGreenPressedCallback, bouncetime=200)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=leftPinCallback, bouncetime=80)
    GPIO.add_event_detect(27, GPIO.BOTH, callback=rightPinCallback, bouncetime=80)

    print("wait for order from opponent")
    turn = 1

    if order == 1:
        turn += 1

    while 1:
        resetPointer()
        if turn % 2 == 0:
            opponentsTurn()
        else:
            myTurn()

        result = checkForWin()
        if result != 0:
            return result

        if turn == 9 and order == 2 or turn == 10 and order == 1:
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
        gameResult = run()
        if gameResult == 0:
            print("add draw to both players")
        elif gameResult == 1:
            print("add win to this player, lose to second")
        else:
            print("add lose to this player, win to second")