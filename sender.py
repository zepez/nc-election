import requests


def send(json):
  x = requests.post("http://localhost:3001/rail/test", data = json, headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'UTF-8'})
  print(x.status_code)