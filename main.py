import requests

latest = 'https://api.fixer.io/2000-05-29?base=USD'

json = requests.get(latest).json()

print(json)