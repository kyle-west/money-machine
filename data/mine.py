########################################################################
# 
########################################################################
import requests
import datetime

storeFileName = "raw_base_usd.csv"
first_avaliable_day = datetime.date(1999, 1, 4)
# first_avaliable_day = datetime.date(2000,7, 17)
today = datetime.date.today()
diff = today - first_avaliable_day
day_range = range(0, diff.days)
# day_range = range(0, 10)

########################################################################
# fetch data from our endpoint
########################################################################
def forexOn(date):
   url = "https://api.fixer.io/" + date + "?base=USD"
   return requests.get(url).json()

########################################################################
# convert our buffer into a CSV file format
########################################################################
def toCSV(data):
   cols = data.keys()
   csv = ",".join(list(cols)) + "\n"
   for row in day_range:
      date = first_avaliable_day + datetime.timedelta(days=row)
      if (date.weekday() < 5): # Monday is 0 and Sunday is 6
         line = []
         for col in cols:
            if row in data[col]:
               line.append(str(data[col][row]))
            else:
               line.append("?")
         csv += ",".join(list(line)) + "\n"
   return csv



########################################################################
# Load data from the server and process it.
########################################################################
buffer = {}
for i in day_range:
   date = first_avaliable_day + datetime.timedelta(days=i)
   # Monday is 0 and Sunday is 6
   if (date.weekday() < 5):
      print(i+1,"/",diff.days, "days")
      d_str = date.strftime("%Y-%m-%d")

      try:
         res = forexOn(d_str)
      except: #try again
         # print to file for fail save
         file = open(storeFileName,"w")
         file.write(toCSV(buffer))
         file.close() 
         print(storeFileName, "written")
         print ("HIT EXCEPTION:", res)
         res = forexOn(d_str)
      
      # populate into storage
      for key in res['rates']:
         if key not in buffer:
            buffer[key] = {}
         buffer[key][i] = res['rates'][key] 
      

# write the buffer to our file
file = open(storeFileName,"w")
file.write(toCSV(buffer))
file.close() 
print(storeFileName, "written")