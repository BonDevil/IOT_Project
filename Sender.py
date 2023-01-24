from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time
from mfrc522 import MFRC522
import paho.mqtt.client as mqtt
import psycopg2
from Database.DatabaseHandler import get_players_rfid

is_on = False
time_start = time.localtime()
time_stop = time.localtime()

broker = "kolkorzyzyk.duckdns.org"
port = 1883
# broker = "127.0.0.1"
# broker = "10.0.0.1"

client = mqtt.Client()

def connect_to_broker():
 # Connect to the broker.
    client.username_pw_set('user-broker', 'P@ssw0rd')
    client.connect(broker, port) # Send message about conenction

def disconnect_from_broker():
     client.disconnect()
# Send message about disconenction.
#  call_worker("Client disconnected")
# Disconnet the client.

def rfidRead():
    global is_on
    global time_start
    global time_stop
    MIFAREReader = MFRC522()
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # while status == MIFAREReader.MI_OK:
    #     (status, uid) = MIFAREReader.MFRC522_Anticoll()
    #     if status == MIFAREReader.MI_OK:
    #         num = 0
    #         for i in range(0, len(uid)):
    #             num += uid[i] << (i*8)
    #         if not is_on:
    #             time_start = time.localtime()
    #             is_on = True
    #            # print(f"Card read UID: {uid} > {num}")
    #            # print(f"time: {time.strftime('%H:%M:%S', time_start)}")
    #             client.publish("pi/rfid", f"{num}")
    #         buzzer(True)
    #         GPIO.output(led1, True)
    if status == MIFAREReader.MI_OK:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            num = 0
            for i in range(0, len(uid)):
                num += uid[i] << (i*8)

            # connention = psycopg2.connect(
            #     host="hostname",
            #     database="dbname",
            #     user="username",
            #     password="password"
            # )
            # cursor = connention.cursor()
            # uids_tuples = list(cursor.execute("SELECT * FROM workers_log").fetchall())
            # print(uids_tuples)
            # uids = [elem[1] for elem in uids_tuples]
            uids = get_players_rfid()
                       
                           
            if str(num) not in uids:
                print(f"Card read UID: {uid} > {num}")
                call_worker(str(num))
                time.sleep(0.5)
                buzzer(True)
                pixels.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
                pixels.show()
                time.sleep(1)
                pixels.fill((0, 0, 0))
                pixels.show()
                buzzer(False)
    is_on = False
    buzzer(False)
    GPIO.output(led1, False)

def buzzer(state):
    GPIO.output(buzzerPin, not state)  # pylint: disable=no-member

def test():
    print('\nBuzzer test.')
    buzzer(True)
    time.sleep(1)
    buzzer(False)

def fun():
    rfidRead()

if __name__ == "__main__":
    connect_to_broker()
    print("Activating...")
    while True:
        fun()
    disconnect_from_broker()