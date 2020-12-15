import requests

def is_auth(ip_address = ''):
    response = requests.get('http://localhost:5281/auth?ip='+ip_address)
    return response.json()['status']