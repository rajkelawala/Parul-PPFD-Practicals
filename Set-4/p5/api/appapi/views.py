#pip install requests

from django.shortcuts import render
import requests

def weather_view(request):
    weather_data = None

    if request.method == "POST":
        city = request.POST['city']

        # Simple city to latitude-longitude mapping (basic example)
        cities = {
            "surat": {"lat": 21.1702, "lon": 72.8311},
            "mumbai": {"lat": 19.0760, "lon": 72.8777},
            "delhi": {"lat": 28.7041, "lon": 77.1025},
        }

        city = city.lower()

        if city in cities:
            lat = cities[city]["lat"]
            lon = cities[city]["lon"]

            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

            response = requests.get(url)
            data = response.json()

            temperature = data["current_weather"]["temperature"]

            weather_data = {
                "city": city.title(),
                "temperature": temperature
            }

    return render(request, "weather.html", {"weather": weather_data})
