#!/usr/bin/python

import paho.mqtt.client as paho
import psutil
import pywapi
import signal
import sys
import time
from time import gmtime, strftime
#import socket
import pdb
from threading import Thread

import pyupm_grove as grove
relay = grove.GroveRelay(2) # GPIO pin 2

import dweepy

from uuid import getnode as get_mac

"""
import plotly.plotly as py
from plotly.graph_objs import Scatter, Layout, Figure
username = 'marcelarosalesj'
api_key = 'twr0hlw78c'
stream_token = '2v04m1lk1x'
"""

from flask import Flask
from flask_restful import Api, Resource
app = Flask(__name__)
api = Api(app)

#ip = socket.gethostbyname(socket.gethostname())

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = '61f1ed21b8d34499a249d227654d7077'
ADAFRUIT_IO_USERNAME = 'marcelarosalesj'

class Network(Resource):
    def get(self):
        data = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " - "+ message
        return data

api.add_resource(Network, '/network')


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
    global idDevice 
    idDevice = GetMACAddress() # Make this a global variable
    mqttclient = paho.Client()
    mqttclient.on_publish = on_publish
    adaclient = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    adaclient.connect()
    #adaclient.loop_background()
    while True:
        packets = dataNetwork()    
    	global message 
        message = idDevice + " " + str(packets)
    	#pdb.set_trace()
        print "dataNetworkHandler " + message
    	mqttclient.publish("IoT101/"+idDevice+"/Network", message)
    	adaclient.publish("IoT101/"+idDevice+"/Network", message)
	json = {'id':idDevice,'packets':int(packets)}
        dweepy.dweet_for('DataReportingSystem',json)
        time.sleep(3)

def on_message(mosq, obj, msg):
    print "on msg: ", msg.payload, " - ", msg.topic
    if msg.payload == "A":
	print "dentro on_message A  - ", relay.isON()
        if relay.isOn():
            relay.off()
	    print "MQTT dataMessageHandler: Relay OFF"
        else:
            relay.on()
	    print "MQTT dataMessageHandler: Relay ON"
    else:
	print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload) 

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/"+idDevice+"/Message", 0)
    
    while mqttclient.loop() == 0:
        pass

    while True:
        print "Data Message Handler"
	time.sleep(5)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    threadx = Thread(target=dataMessageHandler)
    threadx.start()

    app.run(host = '0.0.0.0', debug=True)

    while True:
        print "Main - Hello Internet of Things 101"
        time.sleep(5)


# End of File
