#!/usr/bin/env python3
from os import environ
from influxdb import InfluxDBClient
from datetime import datetime
from socket import socket, AF_UNIX, SOCK_STREAM
from sys import argv

def main():
    username = environ['INFLUX_USERNAME']
    password = environ['INFLUX_PASSWORD']
    database = environ['INFLUX_DATABASE']

    db = InfluxDBClient(username=username, password=password, database=database)

    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.connect('/tmp/tempergold1.sock')

    temp = b''
    while True:
        x = sock.recv(4096)
        if x == b'':
            break
        temp += x

    temp = temp.decode()

    json_body = {
        'measurement': 'temp',
        'time': datetime.utcnow().isoformat(),
        'tags': { 'source': 'loft_thermometer' },
        'fields': { 'temp': float(temp) },
    }
    sock.close()

    if '-' in argv:
        print(temp)
    else:
        db.write_points([json_body])

if __name__ == '__main__':
    main()
