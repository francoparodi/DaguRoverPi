import time, pynmea2
from flaskr.gps import Gps as gps

def gpsGetGPGGA():
    while gps.online:
        gps_data = gps.gpsData()
        print('gps_data is ' + gps_data)
        if "GPGGA" in gps_data:
            nmeaObj = pynmea2.parse(gps_data)
            gps.timestamp = nmeaObj.timestamp
            gps.satellites = nmeaObj.num_sats
            gps.gpsQuality = nmeaObj.gps_qual
            gps.altitude = nmeaObj.altitude
            gps.altitudeUm = nmeaObj.altitude_units
            gps.latitude = nmeaObj.lat
            gps.longitude = nmeaObj.lon
            gps.latitude_dir = nmeaObj.lat_dir
            gps.longitude_dir = nmeaObj.lon_dir
            print('Timestamp={0} Satellites={1} GPSQuality={2} Altitude={3}{4} Latitude={5},{6} Longitude={7},{8}'.format(gps.timestamp, gps.satellites, gps.gpsQuality, gps.altitude, gps.altitudeUm, gps.latitude_dir, gps.latitude, gps.longitude_dir, gps.longitude))
            break

# Safe terminating
def cleanUp():
    gps.online = False
    gps.GPIO.cleanup()
