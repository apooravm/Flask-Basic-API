import requests

url = "http://localhost:4000/users/64e6d89c7e774ccaf8e48f7a"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
