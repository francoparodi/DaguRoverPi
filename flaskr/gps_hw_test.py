import serial
import time
import string
import pynmea2

serialPort = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=0.5)

def to_degrees(lat, lon):
    lat_deg = lat[0:2]
    lat_mins = lat[2:]
    latitude = float(lat_deg) + (float(lat_mins)/60)

    lon_deg = lon[0:3]
    lon_mins = lon[3:]
    longitude = float(lon_deg) + (float(lon_mins)/60)

    return [latitude, longitude]

while True:
    gps_data = serialPort.readline().decode('ascii', errors='ignore')

    if gps_data.find('GGA') > 0:
        print('found GGA in gps_data ')
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

        print('Lat-Lon to dec:' + str(to_degrees(latitude, longitude)[0]) + ' ' + str(to_degrees(latitude, longitude)[1])) 
