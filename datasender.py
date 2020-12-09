#!/usr/bin/python

import random, threading, json
import paho.mqtt.client as mqtt
from datetime import datetime
import time
from envirophat import weather, light, motion
#====================================================
# MQTT Settings
MQTT_Broker = "iot.research.hamk.fi"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Pressure = "HAMK/intip20x6/weather/Pressure"
MQTT_Topic_Temperature = "HAMK/intip20x6/weather/Temperature"
#====================================================

def on_connect(self, client, userdata, rc):
        if rc != 0:
                pass
                print("Unable to connect to MQTT Broker...")
        else:
                print("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
        pass

def on_disconnect(client, userdata, rc):
        if rc !=0:
                pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
#mqttc.username_pw_set(username="demo",password="demo007")
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_To_Topic(topic, message):
        mqttc.publish(topic,message)
        
        print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print ("")


#====================================================
# Sensor
# Code used pull values from Envirophat board on rasperry pi
# to MQTT Broker

toggle = 0

def publish_Sensor_Values_to_MQTT():
        threading.Timer(3.0, publish_Sensor_Values_to_MQTT).start()
        global toggle
        if toggle == 0:
                Pressure_Value = weather.pressure(unit='hPa')
                Pressure_light = light.light()
                Pressure_Data = {}
                Pressure_Data['Sensor_ID'] = "Sensor-1"
                Pressure_Data['Pressure'] = Pressure_Value
                Pressure_Data['Light'] = Pressure_light
                Pressure_json_data = json.dumps(Pressure_Data)
                print("Publishing fake Pressure Value: " + str(Pressure_Value) + "...")
                print("Publishing light amount: " + str(Pressure_light) + "...")
                publish_To_Topic (MQTT_Topic_Pressure, Pressure_json_data)
                toggle = 1

        else:
                Temperature_Value =  weather.temperature()-17
                Temperature_colour = light.rgb()
                Temperature_Data = {}
                Temperature_Data['Sensor_ID'] = "Sensor-1"
                Temperature_Data['Temperature'] = Temperature_Value
                Temperature_Data['Colour'] = Temperature_colour
                temperature_json_data = json.dumps(Temperature_Data)
                print("Publishing Temperature Value: " + str(Temperature_Value) + "...")
                print("Publishing light colour: " + str(Temperature_colour) + "...")
                publish_To_Topic (MQTT_Topic_Temperature, temperature_json_data)
                toggle = 0

publish_Sensor_Values_to_MQTT()

#====================================================
