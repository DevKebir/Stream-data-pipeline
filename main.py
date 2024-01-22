import json
import os
from datetime import datetime
from time import sleep

import boto3
import botocore.exceptions
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
cities = [
    'Texas', 'Tokyo', 'Mexico City', 'São Paulo', 'Seoul', 'Buenos Aires', 'Cairo', 'Istanbul', 'Moscow',
    'Lagos', 'Kolkata', 'Beijing', 'Dhaka', 'Shanghai', 'Mumbai', 'Rio de Janeiro', 'Bangkok', 'Chicago',
    'Los Angeles', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'San Jose', 'Seattle', 'Toronto',
    'Sydney', 'Melbourne', 'Johannesburg', 'Madrid', 'Portland', 'Houston', 'London', 'Paris', 'Marseille', 'Nice',
    'New York', 'Berlin', 'Rome', 'Amsterdam', 'Athens', 'Barcelona', 'Vienna', 'Prague', 'Dublin', 'Warsaw',
    'Stockholm', 'Oslo', 'Copenhagen', 'Helsinki', 'Reykjavik', 'Budapest', 'Zurich', 'Geneva', 'Lisbon', 'Brussels',
    'Brasília', 'Ankara', 'Kyiv', 'Tehran', 'Baghdad', 'Riyadh', 'Abu Dhabi', 'Doha', 'Kuwait City', 'Manila',
    'Jakarta', 'Hanoi', 'Ho Chi Minh City', 'Singapore', 'Kuala Lumpur', 'Bangalore', 'Colombo', 'Doha', 'Kuwait City',
    'Manila', 'Jakarta', 'Hanoi', 'Ho Chi Minh City', 'Singapore', 'Kuala Lumpur', 'Bangalore', 'Colombo', 'Cape Town',
    'Nairobi', 'Copenhagen', 'Auckland', 'Wellington', 'Stockholm', 'Oslo', 'Helsinki', 'Reykjavik', 'Budapest',
    'Zurich', 'Geneva', 'Lisbon', 'Brussels', 'Brasília', 'Ankara', 'Kyiv', 'Tehran', 'Baghdad', 'Riyadh', 'Abu Dhabi',
    'Dubai', 'Muscat', 'Sanaa', 'Khartoum', 'Tunis', 'Nairobi', 'Dakar', 'Accra', 'Monrovia', 'Freetown'
]

STREAM_NAME = os.getenv("STREAM_NAME")
API_KEY  = os.getenv("API_KEY")

# create a kinesis firehose client with my personal credentials
client = boto3.client("firehose",
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    region_name = os.getenv("REGION_NAME"))

# convert celsius to celsius
def kelvin_to_celsius(temp_in_kelvin):
    kelvin_to_celsius = (temp_in_kelvin - 273.15)
    return kelvin_to_celsius

# make an api call to extract weather data
def weather_data(url):
    r = requests.get(url)
    data = r.json()
    #print(data)

    city = data["name"]
    weather_description = data["weather"][0]["description"]
    temp_celsius = kelvin_to_celsius(data["main"]["temp"])
    feels_like_celsius = kelvin_to_celsius(data["main"]["feels_like"])
    min_temp_celsius = kelvin_to_celsius(data["main"]["temp_min"])
    max_temp_celsius = kelvin_to_celsius(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    visibility = data["visibility"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data["dt"] + data["timezone"])
    sunrise_time = datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"])
    sunset_time = datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"])

    transformed_data = {
        "City": city,
        "Description": weather_description,
        "Temperature (°C)": temp_celsius,
        "Feels Like (°C)": feels_like_celsius,
        "Minimum Temp (°C)": min_temp_celsius,
        "Maximum Temp (°C)": max_temp_celsius,
        "Pressure (hPa)": pressure,
        "Humidity (%)": humidity,
        "Visibility (km)": visibility,
        "Wind Speed (mph)": wind_speed,
        "Time of Record (UTC)": time_of_record,
        "Sunrise (UTC)": sunrise_time,
        "Sunset (UTC)": sunset_time,
    }
    
    #transformed_data_list.append(transformed_data)
    return transformed_data

    
# Send weather data to kinesis firehose
def generate_kinesis_stream(client):
    data = weather_data(url)
    stream_name = STREAM_NAME
    print(data)
    try:
        responses = client.put_record(
            DeliveryStreamName=stream_name,
            Record={
                'Data': json.dumps(data, default=str)
                }
            )
        print(responses)
    except botocore.exceptions.ClientError as e:
        print(f"Error: {e}")


def store_weather_data():
    store =[]
    store_data = weather_data(url)
    store_data_list = store.append(store_data)
    df_data = pd.DataFrame(store_data_list)
    # print(df_data)
    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_file = f"C:\\Users\\PMJ\\Documents\\Own_projects\\LearningsPython\\PROJETS-DATA-ENGINEERING\\Kinesis\\output\\current_weather_data_{current_timestamp}.csv"

    df_data.to_csv(output_file, index = False)





if __name__ =="__main__":
    api_key = API_KEY
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID=" + api_key
        weather_data(url)
        generate_kinesis_stream(client)
        store_weather_data()
        sleep(5)
    

