---
title: Raspberry Pi BME280 MySQL Data Collection
description: Collect data using a Raspberry Pi and BME280 sensor and upload it to a MySQL database.
layout: post
toc: true
mermaid: true
---

![jorgem0/raspberry\u005fpi\u005fbme280\u005fmysql](/assets/images/github.svg){: width="100" height="100" }
_<a href="https://github.com/jorgem0/raspberry_pi_bme280_mysql" target="_blank" rel="noopener noreferrer">jorgem0/raspberry_pi_bme280_mysql</a>_

## Introduction

This tutorial will use a Raspberry Pi Zero W, a BME280 sensor, and MariaDB in order to collect temperature, pressure, and humidity data and store it in a DBMS.

## Setting Up the Raspberry Pi

The first step for this project is to install the Raspbian Stretch OS for the Raspberry Pi. Download the Raspbian Stretch OS image from the [Raspberry Pi website](https://www.raspberrypi.org/downloads/raspbian/){:target="_blank" rel="noopener noreferrer"} and flash it to your MicroSD card using [Etcher](https://etcher.io){:target="_blank" rel="noopener noreferrer"} as seen in the [Raspberry Pi tutorial](https://www.raspberrypi.org/documentation/installation/installing-images/README.md){:target="_blank" rel="noopener noreferrer"}. Once the process has been completed, insert the MicroSD card into your Raspberry Pi and install the OS (it should install automatically). You will now be greeted with the Raspbian Stretch OS desktop. Go to **Raspberry Pi Configuration** by selecting the menu in the top left corner of the screen. Select the **Interfaces** tab and enable **SSH** and **I2C**. Also set up your Wi-Fi in the top right corner.

![Settings](/assets/images/rasp_bme_sql/settings.png)
_Settings_

![Interfaces and Wi-Fi](/assets/images/rasp_bme_sql/interfaces.png)
_Interfaces and Wi-Fi_

Open up the terminal and type in the command `sudo ifconfig` in order to locate your local IP address which will be used to connect to the Raspberry Pi remotely using PuTTY.

![Local IP Address](/assets/images/rasp_bme_sql/localip.png)
_Local IP Address_

Now open up PuTTY and enter your Raspberry Pi's IP Address in the **Host Name** box. The default user is `pi` and default password is `raspberry`. You can now start installing the necessary packages and libraries for this tutorial.

![PuTTY](/assets/images/rasp_bme_sql/putty.png)
_PuTTY_

## Installing Necessary Packages and Libraries

The first set of packages and libraries that need to be installed include the Adafruit Python GPIO Library which allows the Raspberry Pi to interact with the sensor. The necessary packages and libraries can be installed with the commands below as stated in the [Adafruit Python GPIO Library GitHub](https://github.com/adafruit/Adafruit_Python_GPIO){:target="_blank" rel="noopener noreferrer"} page.

```bash
sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```

Move one directory up and clone the [Adafruit_Python_BME280](https://github.com/adafruit/Adafruit_Python_BME280){:target="_blank" rel="noopener noreferrer"} and install MySQL as well. Raspberry Pi will install MariaDB instead but the SQL commands that work for MySQL will work with MariaDB. Also install the Python MySQL package `MySQLdb` in order for Python to be able to communicate with MySQL/MariaDB and `vim` to edit text files.

```bash
cd ..
git clone https://github.com/adafruit/Adafruit_Python_BME280.git
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb
sudo apt-get install vim
```

Log in to MySQL with `sudo mysql -u root` and create a database and table in MariaDB in order to enter the BME280 data. I have created a database named `RaspberryPi` and a table named `BME280_Data` with the columns `date_time`, `temperature`, `pressure`, and `humidity`. Also create a new user with the `CREATE USER` command below where `newuser` is the username of the new user and `newuserpassword` is the password of the new user. Grant all privileges for the user. You can exit MariaDB by typing `exit` in the terminal.

```sql
CREATE DATABASE RaspberryPi;
USE RaspberryPi;
CREATE TABLE BME280_Data (date_time VARCHAR(50), temperature FLOAT, pressure FLOAT, humidity FLOAT);
DESCRIBE BME280_Data;

CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'newuserpassword';
GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost';
```

![MariaDB](/assets/images/rasp_bme_sql/mariadb.png)
_MariaDB_

## Wiring Raspberry Pi and BME280

The wiring for the BME280 sensor and the Raspberry Pi is seen in the diagram below. This diagram was created using [Fritzing](http://fritzing.org/home/){:target="_blank" rel="noopener noreferrer"}. The pinout diagram for the Raspberry Pi is from [pinout.xyz](https://pinout.xyz){:target="_blank" rel="noopener noreferrer"}. The wires are connected as follows:

```mermaid
flowchart LR
    VIN[VIN] -->|5V| PIN2[Pin 2 / 4]
    GND[GND] -->|Ground| PIN6[Pin 6]
    SCL[SCK / SCL] -->|I2C Clock| PIN5[Pin 5]
    SDA[SDI / SDA] -->|I2C Data| PIN3[Pin 3]
```

![Raspberry Pi and BME280 Diagram](/assets/images/rasp_bme_sql/rasppibme280_bb.png)
_Raspberry Pi and BME280 Diagram_

![Raspberry Pi Zero Pinout Diagram from pinout.xyz](https://pinout.xyz/resources/raspberry-pi-pinout.png)
_Raspberry Pi Zero Pinout Diagram from pinout.xyz_

![BME 280](/assets/images/rasp_bme_sql/bme280connected.jpg)
_BME 280_

![Raspberry Pi Connected](/assets/images/rasp_bme_sql/piconnected.jpg)
_Raspberry Pi Connected_

Type the command `sudo i2cdetect -y 1` in the terminal and you should be able to see the output below if everything is connected correctly.

![i2cdetect](/assets/images/rasp_bme_sql/i2cdetect.png)
_i2cdetect_

You can run the Adafruit_BME280_Example.py script with `python Adafruit_BME280_Example.py` in order to see the BME280 sensor data at the time at which the aforementioned script was executed.

![Adafruit BME280 Example Script](/assets/images/rasp_bme_sql/example.png)
_Adafruit BME280 Example Script_

## Python Code

Go to the Adafruit_Python_BME280 directory and copy the Adafruit_BME280_Example.py script using `cp Adafruit_BME280_Example.py BME280_Custom.py`. Also create a file named BME280CSV with `touch BME280CSV` in order to save data to a CSV file which can also be done with the Raspberry Pi. Open up the BME280_Custom.py file with the vi editor using `vi BME280_Custom.py`. You should now see the unedited copy of Adafruit_BME280_Example.py. We will modify the original file in order for the BME280 sensor to continuously collect data and add it to the `BME280_Data` table created earlier in MariaDB.

![Original Adafruit BME280 Example](/assets/images/rasp_bme_sql/bme1.png)
_Original Adafruit BME280 Example_

The modified Python script for the BME280 sensor can be seen below. The `MySQLdb` module allows one to connect to the MySQL/MariaDB DBMS and run queries through the cursor execute option. The module `csv` allows easy editing of csv files. The `datetime` module states the current date time when the data is collected inside the `while True:` loop. The module `time` allows the data collection `while True:` loop to pause for 60 seconds with `time.sleep(60)` before it collects data again. More specific details about the code are comments within the code. You can run the BME280_Custom.py script with the `python BME280_Custom.py &`. The addition of `&` allows the script to run in the background so one can resume working on other things since this script goes on indefinitely due to `while True:`.

```python
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

```
{: file="BME280_Custom.py" }

Open up BME280CSV with `vi BME280CSV` and you should see the CSV file populated.

![BME280CSV](/assets/images/rasp_bme_sql/csv.png)
_BME280CSV_

You can also see the data being added to the table we created earlier in MySQL/MariaDB with `SELECT * FROM BME280_Data;`.

![MySQL/MariaDB Data](/assets/images/rasp_bme_sql/data.png)
_MySQL/MariaDB Data_

Now copy the BME280_Custom.py script and name the new file BME280_Extract.py use the command with `cp BME280_Custom.py BME280_Extract.py`. This file will be used to pull data from MySQL/MariaDB. Also create a new file named BME280CSVNEW with `touch BME280CSVNEW` in order to save the data from the query. The modified file for the BME280 sensor can be seen below along with some comments.

```python
import csv
import MySQLdb

db = MySQLdb.connect(host="localhost",user="newuser", passwd="newuserpassword",db="RaspberryPi") #connects to MySQL/MariaDB
cur = db.cursor() #creates cursor to pass on demands to MySQL/MariaDB


with open(r'BME280CSVNEW','w') as f: #w means write to file
    writer = csv.writer(f)
    writer.writerow(['Date Time (YYYY-MM-DD HH:MM:SS','Temperature (deg C)','Pressure (Pa)','Humidity (%)']) #CSV file headers



#executes the SQL command in MySQL/MariaDB to collect data.
cur.execute('''SELECT * FROM BME280_Data''')




for row in cur.fetchall(): #prints all rows
    print row #this prints a row in all columns
   # print row[0] #this prints a row in a specific column
    with open(r'BME280CSVNEW', 'a') as f: #a means append to file
        writer = csv.writer(f)
        writer.writerow([row])


db.close()

```
{: file="BME280_Extract.py" }

Run the new Python script with `python BME280_Extract.py`. Note that there is no `&` since this script does not run indefinitely as it doesn't contain the `while True:` statement. You can also view the new CSV file with `vi BME280CSVNEW`.

![BME280 Extract](/assets/images/rasp_bme_sql/extract1.png)
_BME280 Extract_

![BME280CSVNEW](/assets/images/rasp_bme_sql/extract2.png)
_BME280CSVNEW_
