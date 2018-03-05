import requests
import datetime

# latest = 'https://api.fixer.io/latest?base=USD'

# json = requests.get(latest).json()


# date = datetime.date(1999, 1, 1)
# print(date.strftime("%Y-%m-%d"))

def forexOn(date):
   url = "https://api.fixer.io/" + date + "?base=USD"
   return requests.get(url).json()


for i in range(1,35):
   date = datetime.date(1998, 12, 31) + datetime.timedelta(days=i)
   # Monday is 0 and Sunday is 6
   if (date.weekday() < 5):
      print(date.strftime("%Y-%m-%d"), date.weekday())
      print(forexOn(date.strftime("%Y-%m-%d")))
