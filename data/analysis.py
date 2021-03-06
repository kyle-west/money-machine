########################################################################
# 
# This file contains functions that query a dataset for information, 
# and/or run a function against that dataset for specific dates.
#
########################################################################


import datetime
from dateutil.relativedelta import relativedelta

########################################################################
# helper to allow functions to accept both strings and Date objects
########################################################################
def getDate(date):
   if (type(date) == str):
      return datetime.datetime.strptime(date, '%Y-%m-%d').date()
   else:
      return date

########################################################################
# Returns a data row closest to a given date in the fiscal year
########################################################################
def row_circa(date, df, date_col_name = 'Date'):
   day = getDate(date)
   first_availiable = getDate(df[date_col_name][0]) # assume sorted
   while True: # no do-whiles in python :(
      row = df[df[date_col_name] == day.strftime("%Y-%m-%d")]
      if not row.empty:
         return row
      day = day - datetime.timedelta(days=1)
      if (day < first_availiable):
         return None

########################################################################
# Returns a data row for "this time last year" in the fiscal year
########################################################################
def YTD(date, df, target_col = None):
   day = getDate(date)
   last_year = day - relativedelta(years=1)
   row = row_circa(last_year, df)
   if target_col:
      if row is not None: return row[target_col].tolist()[0]
      else: return None
   else: return row




########################################################################
# Test out our functions
########################################################################
if __name__ == "__main__":
   import pandas
   CAD = pandas.read_csv("./per_currency/CAD.dat", header=0)
   print("----------------------------------------------------")
   print("DATA")
   print(CAD)

   print("----------------------------------------------------")
   print("TEST row_circa")
   print("\n1999-01-05",row_circa("1999-01-05", CAD), sep="\n")
   print("\n1999-01-09",row_circa("1999-01-09", CAD), sep="\n")
   print("\n1999-01-16",row_circa(datetime.datetime.strptime("1999-01-16", '%Y-%m-%d').date(), CAD), sep="\n")

   print("----------------------------------------------------")
   print("TEST YTD")
   print("\n2000-01-05", YTD("2000-01-05", CAD), sep="\n")
   print("\n2000-01-09", YTD("2000-01-09", CAD, target_col = "CAD"), sep="\n")
   print("\n1999-01-09", YTD("1999-01-09", CAD, target_col = "CAD"), sep="\n")