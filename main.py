import requests

latest = 'https://api.fixer.io/latest?base=USD'

json = requests.get(latest).json()

print(json)