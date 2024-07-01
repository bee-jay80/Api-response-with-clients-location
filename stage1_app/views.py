from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.gis.geoip2 import GeoIP2
import requests

@require_GET
def home(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')

    try:
        if client_ip:
            g = GeoIP2()
            location = g.country_code(client_ip)
        else:
            location = 'Unknown'

        # Default temperature value
        temperature = 11

        # JSON response
        json_response_data = {
            'client_ip': client_ip,
            'location': location,
            'greeting': f'Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}'
        }

        return JsonResponse(json_response_data)

    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch location'}, status=500)