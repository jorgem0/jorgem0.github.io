from Adafruit_BME280 import *
import time
import datetime
import csv
import MySQLdb

db = MySQLdb.connect(host="localhost",user="newuser", passwd="newuserpassword",db="RaspberryPi") #connects to MySQL/MariaDB
cur = db.cursor() #creates cursor to pass on demands to MySQL/MariaDB

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

with open(r'BME280CSV','w') as f: #w means write to file
    writer = csv.writer(f)
    writer.writerow(['Date Time (YYYY-MM-DD HH:MM:SS','Temperature (deg C)','Pressure (Pa)','Humidity (%)']) #CSV file headers



while True: #collects data indefinitely

    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()
    timenow = datetime.datetime.utcnow()
    

    #executes the SQL command in MySQL/MariaDB to insert data.
    cur.execute('''INSERT INTO BME280_Data(date_time, temperature, pressure, humidity) VALUES(%s,%s,%s,%s);''',(timenow,degrees,pascals,humidity)) 


    db.commit() #commits the data entered above to the table

   # print 'Time      = ' + str(timenow) 
   # print 'Temp      = {0:0.3f} deg C'.format(degrees)
   # print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
   # print 'Humidity  = {0:0.2f} %'.format(humidity)
    
    with open(r'BME280CSV', 'a') as f: #a means append to file
        writer = csv.writer(f)
        writer.writerow([timenow,degrees,pascals,humidity])



    time.sleep(60) #waits for 60 seconds to collect data again


