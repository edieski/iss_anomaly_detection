import requests
import mysql.connector
from datetime import datetime

def get_iss_data():
    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url)
    data = response.json()
    timestamp = datetime.fromtimestamp(data['timestamp'])
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    velocity = float(data['iss_velocity'])
    altitude = float(data['iss_altitude'])
    return {'timestamp': timestamp, 'latitude': latitude, 'longitude': longitude, 'velocity': velocity, 'altitude': altitude}

def insert_iss_data_into_db():
    cnx = mysql.connector.connect(user='user', password='root',
                                      host='localhost',
                                      database='iss_data')
    cursor = cnx.cursor()
    data = get_iss_data()
    add_data_query = ("INSERT INTO iss_data "
                      "(timestamp, latitude, longitude, velocity, altitude) "
                      "VALUES (%s, %s, %s, %s, %s)")
    data_tuple = (data['timestamp'], data['latitude'], data['longitude'], data['velocity'], data['altitude'])
    cursor.execute(add_data_query, data_tuple)
    cnx.commit()
    cursor.close()
    cnx.close()