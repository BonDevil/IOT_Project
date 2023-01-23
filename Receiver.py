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


    # Send message about conenction.
    client.on_connect = "connected"
    client.on_disconnect = "disconnected"
    client.on_message = process_message

    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("pi/game")


def process_message(client, userdata, message):
    # Decode message.
    message_decoded = str(message.payload.decode("utf-8"))
    print(message_decoded)


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
