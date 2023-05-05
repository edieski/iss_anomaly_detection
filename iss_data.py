
import requests
import pymysql.cursors
from datetime import *


def get_iss_data():
    url = 'http://api.open-notify.org/iss-now.json'
    response = requests.get(url)
    data = response.json()
    timestamp = datetime.utcfromtimestamp(data['timestamp'])
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    return {'timestamp': timestamp, 'latitude': latitude, 'longitude': longitude}


def insert_iss_data_into_db():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='space_data',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    data = get_iss_data()
    try:
        with connection.cursor() as cursor:
            # Create table if it does not exist
            cursor.execute("CREATE TABLE IF NOT EXISTS iss_data "
                           "(id INT AUTO_INCREMENT PRIMARY KEY, "
                           "timestamp DATETIME, "
                           "latitude FLOAT, "
                           "longitude FLOAT)")

            # Insert data into table
            sql = "INSERT INTO iss_data (timestamp, latitude, longitude) VALUES (%s, %s, %s)"
            cursor.execute(sql, (data['timestamp'], data['latitude'], data['longitude']))
        connection.commit()
    finally:
        connection.close()
        
if __name__ == '__main__':
    insert_iss_data_into_db()