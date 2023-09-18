import json
import requests

url = "https://api-american-football.p.rapidapi.com/games"

querystring = {"league":"1","season":"2023"}

headers = {
	"X-RapidAPI-Key": "1e3ccc2439msh0e41508573472b1p12951ejsnbb3a79fa2ed1",
	"X-RapidAPI-Host": "api-american-football.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = json.loads( response.text )
pretty_schedule = json.dumps(data, indent=4)

#print(response.json())
print(pretty_schedule)

