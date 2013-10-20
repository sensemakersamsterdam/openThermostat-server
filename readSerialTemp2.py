# -*- coding: iso-8859-1 -*-

import serial
import sys
import string
import time 
import MySQLdb
from ConfigParser import SafeConfigParser




# read configuration file in (current directory) config.ini
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



# create database connection
db = MySQLdb.connect(host=host, port=port, user=user, db="home_temperatures")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS home_temperatures(TimeStamp TIMESTAMP NOT NULL PRIMARY KEY, Temperature INT)");



# open serial connection with first argument as device name (argVector[1]), baudrate 9600, and timeout 1s
ser = serial.Serial(device,baudrate, timeout = 1)


query = "INSERT INTO temperatures(Temperature) VALUES(%s)"



notFound = True;
# total size of reading from the arduino is 61 bytes 
while (notFound) :
 s = ser.read(61)
  # if 'C: ' is found in the buffer, print the 3-7 characters after it (whic is the temperature)
 if (s.find('C: ') >= 0):
  #notFound = False;
  currTemp = s[s.find('C: ') + 3:s.find('C: ')+7]
  cursor.execute(query,currTemp)
  
  db.commit
  
  
 
 # a little delay
 time.sleep(10);
 
 
 # what is left to do is outside the loop connect to the database, and inside the loop store the value


