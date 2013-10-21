# -*- coding: iso-8859-1 -*-

import serial
import sys
import string
import time 
import MySQLdb
from ConfigParser import SafeConfigParser




# read configuration file in (current directory) simple.ini
parser 		= SafeConfigParser()
parser.read('simple.ini')


# device parameters
device 		= parser.get('device', 'device_file')
baudrate 	= parser.get('device', 'baud_rate')


# database parameters
host 		= parser.get('database', 'host')
port 		= int(parser.get('database', 'port'))
user 		= parser.get('database', 'user')
password 	= parser.get('database','password')
database_name	= parser.get('database','database_name')


# create database connection
db = MySQLdb.connect(host=host, port=port, user=user, db="home_temperatures")

cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS %s(TimeStamp TIMESTAMP NOT NULL PRIMARY KEY, Temperature INT)",database_name);



# open serial connection with device, baudrate and timeout 1s
ser = serial.Serial(device,baudrate, timeout = 1)

# query string
query = "INSERT INTO temperatures(Temperature) VALUES(%s)"



notFound = True;
# total size of reading from the arduino is 61 bytes 
while (notFound) :
 s = ser.read(61)
  # if 'C: ' is found in the buffer, save the [3-7] characters after it (which is the temperature)
 if (s.find('C: ') >= 0):
  
  currTemp = s[s.find('C: ') + 3:s.find('C: ')+7]
  
  # store in db
  cursor.execute(query,currTemp)
  
  db.commit
  
  
 
 # a little delay
 time.sleep(10);
