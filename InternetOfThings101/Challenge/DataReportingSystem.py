#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import signal
import sys
import time
import pdb
from threading import Thread
from uuid import getnode as get_mac

def interruptHandler(signal, frame):
    sys.exit(0)

def GetMACAddress():
    mac = str.upper(hex(get_mac()))
    mac = mac[2:-1]
    return ':'.join(s.encode('hex') for s in mac.decode('hex'))

def on_publish(mosq, obj, msg):
    pass

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
    idDevice = GetMACAddress() # Make this a global variable
    
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    mqttclient.connect("test.mosquitto.org", 1883, 60)

    while True:
        packets = dataNetwork()    
    	message = idDevice + " " + str(packets)
    	print "dataNetworkHandler " + message
    	mqttclient.publish("IoT101/"+idDevice+"/Network", message)
    	time.sleep(1)


def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/"+idDevice+"/Message", 0)

    while mqttclient.loop() == 0:
        pass

    while True:
        print "Hello Internet of Things 101"
        time.sleep(5)



#dataNetworkHandler()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()

    while True:
        print "Hello Internet of Things 101"
        time.sleep(5)


# End of File
