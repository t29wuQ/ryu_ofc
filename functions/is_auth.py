import requests

def is_auth():
    response = requests.get('http://localhost:5281/auth')
    return response.json()['status']

print(is_auth())