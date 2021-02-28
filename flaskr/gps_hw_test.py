import serial
import time
import string
import pynmea2

while True:
    data = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=2.0)
    print('data is ' + str(data))
    #gps_data = data.readline().decode('ascii', errors='replace')
    while data.read().decode("utf-8") != '$': # Wait for the begging of the string
        pass # Do nothing
    gps_data = data.readline().decode("utf-8")
    print('gps_data is ' + str(gps_data))

    if "GPGGA" in gps_data:
        print('found GPGGA in gps_data ')
        nmeaObj = pynmea2.parse(gps_data)
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