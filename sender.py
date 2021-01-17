import requests
import os



def send(json):
  x = requests.post(os.environ.get('endpoint'), data = json, headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'UTF-8'})
  print(x.status_code)