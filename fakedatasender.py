#!/usr/bin/python

import random, threading, json
import paho.mqtt.client as mqtt
from datetime import datetime
import time

#====================================================
# MQTT Settings
MQTT_Broker = "127.0.0.1"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Pressure = "Sensors/HAMK/LABRA/Pressure"
MQTT_Topic_Temperature = "Sensors/HAMK/LABRA/Temperature"

#====================================================

def on_connect(self, client, userdata, rc):
        if rc != 0:
                pass
                print "Unable to connect to MQTT Broker..."
        else:
                print "Connected with MQTT Broker: " + str(MQTT_Broker)

def on_publish(client, userdata, mid):
        pass

def on_disconnect(client, userdata, rc):
        if rc !=0:
                pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.username_pw_set(username="demo",password="demo007")
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_To_Topic(topic, message):
        mqttc.publish(topic,message)
        
        print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print ""


#====================================================
# FAKE SENSOR
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

def publish_Fake_Sensor_Values_to_MQTT():
        threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
        global toggle
        if toggle == 0:
                Pressure_Fake_Value = float("{0:.2f}".format(random.uniform(950, 1100)))

                Pressure_Data = {}
                Pressure_Data['Sensor_ID'] = "Dummy-1"
                Pressure_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
                Pressure_Data['Pressure'] = Pressure_Fake_Value
                Pressure_json_data = json.dumps(Pressure_Data)

                print "Publishing fake Pressure Value: " + str(Pressure_Fake_Value) + "..."
                publish_To_Topic (MQTT_Topic_Pressure, Pressure_json_data)
                toggle = 1

        else:
                Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))

                Temperature_Data = {}
                Temperature_Data['Sensor_ID'] = "Dummy-2"
                Temperature_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
                Temperature_Data['Temperature'] = Temperature_Fake_Value
                temperature_json_data = json.dumps(Temperature_Data)

                print "Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + "..."
                publish_To_Topic (MQTT_Topic_Temperature, temperature_json_data)
                toggle = 0

publish_Fake_Sensor_Values_to_MQTT()

#====================================================
