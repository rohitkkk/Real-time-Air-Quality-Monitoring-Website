import requests
import time
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "/home/Rohit231/credentials.json"  # Replace with the path to your downloaded credentials file
SPREADSHEET_ID = '1xNvLEx3AuzrkLFxVWTYb9bx66756YudSmXsWGyr11Ls'  # Replace with your Google Spreadsheet ID

# Loading credentials and creating a Google Sheets API client
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# OpenWeatherMap setup
api_key = "cd1c5b6d3730e76ea9ad5d0e419859fb"  # Replace with your OpenWeatherMap API key
base_url = "https://api.openweathermap.org/data/2.5/air_pollution?"

# List of cities here
cities = [
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"name": "Nagpur", "lat": 21.1458, "lon": 79.0882},
    {"name": "Nashik", "lat": 20.0058, "lon": 73.7902},
    {"name": "Aurangabad", "lat": 19.8762, "lon": 75.3433},
    {"name": "Solapur", "lat": 17.6599, "lon": 75.9064},
    {"name": "Amravati", "lat": 20.9374, "lon": 77.7796},
    {"name": "Kolhapur", "lat": 16.7050, "lon": 74.2433},
    {"name": "Akola", "lat": 20.7077, "lon": 77.0016},
    {"name": "Latur", "lat": 18.4088, "lon": 76.5604},
    {"name": "Dhule", "lat": 20.9042, "lon": 74.7745},
    {"name": "Chandrapur", "lat": 19.9615, "lon": 79.2961},
    {"name": "Parbhani", "lat": 19.2686, "lon": 76.7708},
    {"name": "Jalgaon", "lat": 21.0077, "lon": 75.5626},
    {"name": "Ichalkaranji", "lat": 16.7094, "lon": 74.4567},
    {"name": "Jalna", "lat": 19.8413, "lon": 75.8860},
    {"name": "Nanded", "lat": 19.1383, "lon": 77.3210},
    {"name": "Bhusawal", "lat": 21.0437, "lon": 75.7850},
    {"name": "Satara", "lat": 17.6805, "lon": 74.0183},
    {"name": "Osmanabad", "lat": 18.1860, "lon": 76.0419},
    {"name": "Wardha", "lat": 20.7453, "lon": 78.6022},
    {"name": "Nandurbar", "lat": 21.3700, "lon": 74.2405},
    {"name": "Yavatmal", "lat": 20.3888, "lon": 78.1204},
    {"name": "Sangli", "lat": 16.8600, "lon": 74.5758},
    {"name": "Gondia", "lat": 21.4559, "lon": 80.1922},
    {"name": "Hinganghat", "lat": 20.5470, "lon": 78.8353},
    {"name": "Washim", "lat": 20.1123, "lon": 77.1447},
    {"name": "Baramati", "lat": 18.1496, "lon": 74.5776},
    # More cities can be added here if required
]
def get_existing_ids(sheet):
    """Get all existing IDs from the Google Sheet."""
    try:
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="mastaqiprojecttableau!A:A").execute()
        return [row[0] for row in result.get('values', [])]
    except Exception as e:
        print(f"Error while fetching existing IDs: {e}")
        return []

def append_to_sheet(rows):
    """Append rows to Google Sheet."""
    try:
        body = {'values': rows}
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="mastaqiprojecttableau",
            body=body,
            valueInputOption="RAW"
        ).execute()
        print(f"Appended new rows: {rows}")
    except Exception as e:
        print(f"Error while appending: {e}")

while True:
    existing_ids = get_existing_ids(sheet)
    
    for city in cities:
        try:
            lat = city["lat"]
            lon = city["lon"]
            response = requests.get(f"{base_url}lat={lat}&lon={lon}&appid={api_key}")
            
            if response.status_code == 200:
                data = response.json()
                
                if "list" in data:
                    aqi_data = data["list"][0]["main"]["aqi"]
                    co = data["list"][0]["components"]["co"]
                    no = data["list"][0]["components"]["no"]
                    no2 = data["list"][0]["components"]["no2"]
                    o3 = data["list"][0]["components"]["o3"]
                    so2 = data["list"][0]["components"]["so2"]
                    pm2_5 = data["list"][0]["components"]["pm2_5"]
                    pm10 = data["list"][0]["components"]["pm10"]
                    nh3 = data["list"][0]["components"]["nh3"]
                    
                    new_row = [city['name'], aqi_data, co, no, no2, o3, so2, pm2_5, pm10, nh3]
                    
                if "list" in data:
                    # data extraction logic here
                    
                    new_row = [city['name'], aqi_data, co, no, no2, o3, so2, pm2_5, pm10, nh3]
                    
                    if city['name'] in existing_ids:
                        row_index = existing_ids.index(city['name']) + 1  # Add 2 to offset 0-based index and header row
                        sheet.values().update(
                            spreadsheetId=SPREADSHEET_ID,
                            range=f"mastaqiprojecttableau!A{row_index}",
                            valueInputOption="RAW",
                            body={"values": [new_row]}
                        ).execute()
                        print(f"Updated existing row for city: {city['name']}")
                    else:
                        append_to_sheet([new_row])
                        existing_ids.append(city['name'])

                else:
                    print(f"Unexpected JSON structure: {data}")
            else:
                print(f"Failed to get weather data: {response.content}")
        except Exception as e:
            print(f"An error occurred: {e}")

    time.sleep(86400)  # 24 hours

