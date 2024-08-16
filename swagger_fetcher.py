import requests
import json

def fetch_swagger_data(swagger_url):
    response = requests.get(swagger_url)
    return response.json()
