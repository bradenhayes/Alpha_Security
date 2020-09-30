#!/usr/bin/env python3
import sqlite3

dbconnect = sqlite3.connect("mydatabase.db");
dbconnect.row_factory = sqlite3.Row;
cursor = dbconnect.cursor();

cursor.execute('SELECT * FROM sensors');
print("Sensor ID | Type | Zone");

for row in cursor:
    if row['zone'] == 'kitchen':
        print(row['sensorID'],row['type'],row['zone']);
    if row['type'] == 'door':
        print(row['sensorID'],row['type'],row['zone']);

dbconnect.close();
