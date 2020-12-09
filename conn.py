#!/usr/bin/python
import paho.mqtt.client as mqtt
from datareader import sensor_Data_Handler

# MQTT Settings
MQTT_Broker = "iot.research.hamk.fi"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "HAMK/intip20x6/weather/#"

#Subscribe to all Sensors at Base Topic
def on_connect(self, mosq, obj, rc):
    if rc != 0:
            pass
            print ("Unable to connect to MQTT Broker...")
    else:
            print ("Connected with MQTT Broker: " + str(MQTT_Broker))
            mqttc.subscribe(MQTT_Topic, 0)

#Save Data into statsd
def on_message(mosq, obj, msg):
        # This is the Master Call for saving MQTT Data to statsd
        print ("MQTT Data Received...")
        print ("MQTT Topic: " + msg.topic)
        print ("Data: " + str(msg.payload))
        sensor_Data_Handler(msg.topic, msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
#mqttc.username_pw_set(username='demo',password='demo007')

# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
mqttc.loop_forever()
