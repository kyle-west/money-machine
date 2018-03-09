########################################################################
# 
# This script takes the data pulled from the server and splits it into
# seperate files. It then uses some functions from analysis.py to 
# preproccess the data and records that data into the files as new 
# columns. 
#
########################################################################


import pandas

filename = "raw_base_usd.csv"
data = pandas.read_csv(filename, header=0)
dat_files = []

########################################################################
# strip each currency into a seperate dat file for further processing
########################################################################
for col in data:
   if col != "Date":
      contents = "Date," + col + "\n"
      for i in range(0, len(data[col])):
         contents += data['Date'][i] + "," + str(data[col][i]) + "\n"
      dat_files.append("./per_currency/"+col+".csv")
      file = open(dat_files[-1],"w") 
      file.write(contents)
      file.close() 


########################################################################
# perform calculations and append data to the file
########################################################################
# calculations to apply to the rows of the data
from analysis import YTD

for location in dat_files:
   print("--------------------------------------------")
   currency = pandas.read_csv(location, header=0)
   ytd = []
   targ = location.split('/')[-1].split('.')[0]
   for index, row in currency.iterrows():
      ytd.append(YTD(row['Date'], currency, target_col = targ))
   currency['YTD'] = pandas.Series(ytd)
   file = open(location,"w")
   file.write(currency.to_csv(na_rep="?", index=False))
   file.close()
   print(location, "written")