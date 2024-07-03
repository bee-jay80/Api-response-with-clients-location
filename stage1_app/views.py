from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.gis.geoip2 import GeoIP2
import requests


def home(request):
    return render(request,"home.html")
@require_GET
def hello(request):
    visitor_name = request.GET.get(str('visitor_name'), 'Visitor')
    r = requests.get('http://127.0.0.1:8000/')
    print(r.status_code)
    print(str(r.content))
    client_ip_x = request.META.get('HTTP_X_FORWARDED_FOR')
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    if client_ip_x:
        address = client_ip_x.split(',')[0]
    else:
        address = request.META.get('REMOTE_ADDR')

    try:
        if address:
            g = GeoIP2()
            location = g.city(address)
            location_country = location["country_name"]
            r = requests.get(url.format(location_country)).json()
            temperature = r["main"]["temp"]
        else:
            location_country = 'Unknown'

        # Default temperature value
        # temperature = 11

        # JSON response
        json_response_data = {
            'client_ip': address,
            'location': location_country,
            'greeting': f'Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location_country}'
        }

        return JsonResponse(json_response_data)

    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch location','address':address,'error':str(e)}, status=500)