import paho.mqtt.client as mqtt
import tkinter
import psycopg2
import time
from Database.DatabaseHandler import insert_player

# The broker name or IP address.
broker = "kolkorzyzyk.duckdns.org"
port = 1883

# The MQTT client.
client = mqtt.Client()

# Thw main window.

def process_message(client, userdata, message):
    # Decode message.
    message_decoded = str(message.payload.decode("utf-8")).split(".")

    # Print message to console.
    if message_decoded[0] != "Client connected" and message_decoded[0] != "Client disconnected":
        print(message_decoded + " used RFID CARD")


        insert_player(*message_decoded)


def connect_message(client, userdata, a, b):
    print('connected')

def disconnect_message(client, userdata, a):
    print('disconnected')

def connect_to_broker():
    # Connect to the broker.
    client.username_pw_set('user-broker', 'P@ssw0rd')
    client.connect(broker, port)
    # Send message about conenction.
    client.on_connect = connect_message
    client.on_disconnect = disconnect_message
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("demo/one")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    while True:
        pass
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()