import pandas

filename = "raw_base_usd.csv"
data = pandas.read_csv(filename, header=0)
dat_files = []

# strip each currency into a seperate dat file for further processing
for col in data:
   if col != "Date":
      contents = "Date," + col + "\n"
      for i in range(0, len(data[col])):
         contents += data['Date'][i] + "," + str(data[col][i]) + "\n"
      dat_files.append("./per_currency/"+col+".dat")
      file = open(dat_files[-1],"w") 
      file.write(contents)
      file.close() 


# calculations to apply to the rows of the data
from analysis import YTD

# perform calculations and append data to the file
for location in dat_files:
   print("--------------------------------------------")
   currency = pandas.read_csv(location, header=0)
   ytd = []
   for index, row in currency.iterrows():
      ytd.append(YTD(row['Date'], currency))
   currency['YTD'] = pandas.Series(ytd)
   print(currency)