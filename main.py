import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

locations = [
    {"city": "panda", "lat": 9.26242, "lon": 7.83852},
    {"city": "gurara", "lat": 9.3220, "lon": 7.0232},
    {"city": "bwari", "lat": 9.2856, "lon": 7.3787},
    {"city": "gwagwalada", "lat": 9.0764, "lon": 6.9854},
    {"city": "makurdi", "lat": 7.7306, "lon": 8.5361}
]

all_weather_data = []
for location in locations:
    lat = location["lat"]
    lon = location["lon"]

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    weather_record = {
    "city": location["city"],
    "latitude": data["coord"]["lat"],
    "longitude": data["coord"]["lon"],
    "weather_main": data["weather"][0]["main"],
    "weather_description": data["weather"][0]["description"],
    "base": data["base"],
    "temperature": data["main"]["temp"],
    "feels_like": data["main"]["feels_like"],
    "minimum_temperature": data["main"]["temp_min"],
    "maximum_temperature": data["main"]["temp_max"],
    "pressure": data["main"]["pressure"],
    "humidity": data["main"]["humidity"],
    "sea_level": data["main"].get("sea_level"),
    "ground_level": data["main"].get("grnd_level"),
    "visibility": data["visibility"],
    "wind_speed": data["wind"]["speed"],
    "wind_direction": data["wind"]["deg"],
    "gust": data["wind"].get("gust"),
    "clouds": data["clouds"]["all"],
    "weather_time": datetime.fromtimestamp(data["dt"]),
    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
    "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
    "country": data["sys"]["country"],
    "location_name": data["name"],
    "extraction_time": datetime.now()
    }
    
    all_weather_data.append(weather_record)

df= pd.DataFrame(all_weather_data)
print(df)

file_path = "weather_data.csv"

file_exists = os.path.isfile(file_path)
file_is_empty = file_exists and os.path.getsize(file_path) == 0

df.to_csv(
    file_path,
    mode="a",
    index=False,
    header=(not file_exists or file_is_empty)
)

print("weather data saved successfully")