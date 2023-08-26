import requests
import json

url = "http://localhost:4000/users/64e6dadab119181a8e8b408b"

payload = json.dumps({
  "name": "Very Generic User",
  "email": "user.gen@gmail.com",
  "password": "1234"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
