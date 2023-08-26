import requests

url = "http://localhost:4000/users/64e6e3c4b119181a8e8b408d"

payload = {}
headers = {}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
