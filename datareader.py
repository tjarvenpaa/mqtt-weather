#!/usr/bin/python

import json
import paho.mqtt.client as mqtt
from datetime import datetime
import time
from statsd import StatsClient
import socket

#===============================================================
# stastd tallennus functiot
# Function to save Temperature to statsd
def Temp_Data_Handler(jsonData):
        #Parse Data
        json_Dict = json.loads(jsonData)
        SensorID = json_Dict['Sensor_ID']
        Temperature = json_Dict['Temperature']
        #Push into statsd
        temp_statsd = StatsClient(host='localhost', port=8125, prefix='Temperature')
        temp_statsd.gauge(SensorID, Temperature)

        print("Inserted Temperature Data into Database.")
        print("")

# Function to save Pressure to statsd
def Pressure_Data_Handler(jsonData):
        #Parse Data
        json_Dict = json.loads(jsonData)
        SensorID = json_Dict['Sensor_ID']
        Pressure = json_Dict['Pressure']


        #Push into statsd
        pres_statsd = StatsClient(host='localhost', port=8125, prefix='Pressure')
        pres_statsd.gauge(SensorID, Pressure)
        print("Inserted Pressure Data into Database.")
        print("")
#===============================================================
#kanta function valinta topikin perusteella
def sensor_Data_Handler(Topic, jsonData):
        if Topic == "HAMK/intim19a6/weather/Temperature":
                Temp_Data_Handler(jsonData)
        elif Topic == "HAMK/intim19a6/weather/Pressure":
                Pressure_Data_Handler(jsonData)

#===============================================================

