import serial
import time
import string
import pynmea2

port="/dev/ttyAMA0"
while True:
    data = serial.Serial(port, baudrate=9600, timeout=0.5)
    newdata = data.readline().decode('ascii', errors='replace')
    if "GPGGA" in newdata:
        nmeaObj = pynmea2.parse(newdata)
        time = nmeaObj.timestamp
        satellites = nmeaObj.num_sats
        gpsQuality = nmeaObj.gps_qual
        altitude = nmeaObj.altitude
        altitudeUm = nmeaObj.altitude_units
        latitude = nmeaObj.lat
        longitude = nmeaObj.lon
        latitude_dir = nmeaObj.lat_dir
        longitude_dir = nmeaObj.lon_dir
        print('Time={0} Satellites={1} GPSQuality={2} Altitude={3}{4} Latitude={5},{6} Longitude={7},{8}'.format(time, satellites, gpsQuality, altitude, altitudeUm, latitude_dir, latitude, longitude_dir, longitude))