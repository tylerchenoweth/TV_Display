import json
import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"league":39,"season":"2023"}

headers = {
    "X-RapidAPI-Key": "1e3ccc2439msh0e41508573472b1p12951ejsnbb3a79fa2ed1",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads( response.text )
data = data['response']
pretty_schedule = json.dumps(data, indent=4)

#print(response.json())
print(pretty_schedule)