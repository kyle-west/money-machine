########################################################################
#
# When I originally saved the 5000+ line CSV file, I forgot to include 
# dates. This adds those dates to the file.
#
########################################################################


import datetime

readFileName = "raw_base_usd.csv"
writeFileName = readFileName
first_avaliable_day = datetime.date(1999, 1, 4)
today = datetime.date.today()
diff = today - first_avaliable_day
day_range = range(0, diff.days)
buffer = ""
i = 0
with open(readFileName, 'r') as f:
   for line in f:
      if (i > 0):
         date = first_avaliable_day + datetime.timedelta(days=i)
         while (date.weekday() > 4):
            i += 1
            date = first_avaliable_day + datetime.timedelta(days=i)
         buffer += date.strftime("%Y-%m-%d") + "," + line
      else:
         buffer += "Date," + line
      i += 1

# write the buffer to our file
file = open(writeFileName,"w")
file.write(buffer)
file.close()
print(writeFileName, "written")