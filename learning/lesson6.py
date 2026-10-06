import copy

import requests

from lesson5 import login_event_without_geoip, get_country

API_URL = "http://ip-api.com/json/"

def lookup_ip(ip: str):
    'Lookup the given IP address using an external service, returns None if the lookup fails or the IP is private'
    try:
        response = requests.get(f"{API_URL}{ip}", timeout=10)
        response_data = response.json()
        if response.status_code == 200 and response_data.get('status') == 'success':
            return dict(
                country_name=response_data['country'],
                city_name=response_data['city'],
                location=dict(
                    lat=response_data['lat'],
                    lon=response_data['lon']
                ),
                isp=response_data['isp']
            )
        else:
            print(f"Failed to lookup IP {ip}: {response.status_code} {response_data.get('message')}")
            return None
    except requests.RequestException as e:
        print(f"Error looking up IP {ip}: {e}")
        return None

def get_geoip_info(event: dict):
    'Get geoip information for the given IP address'
    return dict(
        country=get_country(event),
        city=event.get('geoip', {}).get('city_name'),
        isp=event.get('geoip', {}).get('isp')
    )

if __name__ == "__main__":
    # Lookup a test IP address
    test_ip = "8.8.8.8"
    test_geoip = lookup_ip(test_ip)
    if test_geoip:
        test_geoip_info = get_geoip_info(dict(geoip=test_geoip))
        print(f"GeoIP information for IP {test_ip}:")
        print(test_geoip_info)

    # lookup the IP address of the login event without geoip
    login_event = copy.deepcopy(login_event_without_geoip)
    login_event_data = lookup_ip(login_event['src_ip'])
    if login_event_data:
        login_event['geoip'] = login_event_data
        login_event_info = get_geoip_info(login_event)
        print(f"GeoIP information for login event IP {login_event['src_ip']}:")
        print(login_event_info)

    # lookup local IP address (should return Failed to lookup IP since it's a private IP)
    local_ip = "192.168.56.1"
    local_ip_result = lookup_ip(local_ip)
    if local_ip_result:
        local_ip_info = get_geoip_info(dict(geoip=local_ip_result))
        print(f"GeoIP information for local IP {local_ip}:")
        print(local_ip_info)