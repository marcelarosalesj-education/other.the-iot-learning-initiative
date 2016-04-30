import paho.mqtt.client as paho

def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = on_message
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/90:b6:86:03:a3:cc/Network", 0)
    while mqttclient.loop() == 0:
        pass

dataMessageHandler()
