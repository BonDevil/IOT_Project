# from config import *  # pylint: disable=unused-wildcard-import
import time
import paho.mqtt.client as mqtt

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
    # client.username_pw_set('user-broker', 'P@ssw0rd')
    client.connect(broker, port)


def disconnect_from_broker():
    client.disconnect()


def sendMessage(board):
    client.publish("pi/game", board)


if __name__ == "_main_":
    connect_to_broker()
