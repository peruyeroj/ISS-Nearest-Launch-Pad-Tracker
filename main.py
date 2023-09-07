import requests
import json
response = requests.get("http://api.open-notify.org/iss-now.json")
ipstack = requests.get("http://api.ipstack.com/2601:46:37e:aa50:38ff:a508:61c3:af8f?access_key=f44679348d7d2a8135627b0dbbfe22a0&format=1")

json_data = response.json()

longitude = json_data['iss_position']['longitude']
latitude = json_data['iss_position']['latitude']
print(json_data)

print(longitude)
print(latitude)