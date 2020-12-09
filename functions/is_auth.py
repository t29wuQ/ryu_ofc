import requests

def is_auth(ip_address = ''):
    response = requests.get('http://localhost:5281/auth?ip='+ip_address)
    return response.json()['status']

print(is_auth(ip_address = '172.29.0.1'))