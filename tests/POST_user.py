import requests
import json

url = "http://localhost:4000/users"

payload = json.dumps({
  "name": "Generic User",
  "email": "user.gen@gmail.com",
  "password": "1234"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
