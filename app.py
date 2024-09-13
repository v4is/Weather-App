from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

API_KEY = 'your API key' #go to openweathermap.org and take a api key

def get_weather_data(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&units=metric&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    # Hata kontrolü
    if response.status_code != 200:
        print(f"Error: {data.get('message', 'Unknown error')}")
        return None
    
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    location = None
    
    if request.method == 'POST':
        if 'location' in request.form:
            location = request.form['location']
            geolocator = Nominatim(user_agent="weather_app")
            loc = geolocator.geocode(location)
            
            if loc:
                weather_data = get_weather_data(loc.latitude, loc.longitude)
            else:
                print("Error: Location not found")
                
        elif 'lat' in request.form and 'lon' in request.form:
            lat = request.form['lat']
            lon = request.form['lon']
            weather_data = get_weather_data(lat, lon)
        
    return render_template('index.html', weather_data=weather_data, location=location)

if __name__ == '__main__':
    app.run(debug=True)
