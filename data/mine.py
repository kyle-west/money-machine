import requests
import datetime

storeFileName = "raw_base_usd.csv"
first_avaliable_day = datetime.date(1999, 1, 4)
today = datetime.date.today()
diff = today - first_avaliable_day


def forexOn(date):
   url = "https://api.fixer.io/" + date + "?base=USD"
   return requests.get(url).json()

def toCSVline(data):
   line = ""
   for key, value in data.items():
      line += str(value)
      if (key != "ZAR"): # last one
         line += ","
      else:
         line +="\n"
   return line

file = open(storeFileName,"w") 

file.write("Date,AUD,CAD,CHF,CYP,CZK,DKK,EEK,EUR,GBP,HKD,HUF,ISK,JPY,KRW,LTL,LVL,MTL,NOK,NZD,PLN,ROL,SEK,SGD,SIT,SKK,TRL,ZAR\n")

for i in range(0, diff.days):
   date = first_avaliable_day + datetime.timedelta(days=i)
   # Monday is 0 and Sunday is 6
   if (date.weekday() < 5):
      print(i+1,"/",diff.days, "days")
      d_str = date.strftime("%Y-%m-%d")

      try:
         res = forexOn(d_str)
      except: #try again
         print ("HIT EXCEPTION:", res)
         res = forexOn(d_str)

      file.write(d_str+","+toCSVline(res['rates']))
         


file.close() 
print(storeFileName, "written")