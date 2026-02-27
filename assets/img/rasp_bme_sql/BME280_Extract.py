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
    


