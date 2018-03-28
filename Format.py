########################################################################
#
# Format
#
# This class is a collection of data formatting functions.
#
########################################################################

class Format:
   def DataFrameRow_to_Dictionary(self, dfWithOneRow):
      dict = {}
      for col in dfWithOneRow:
         dict[col] = dfWithOneRow[0:1][col].values[0]
      return dict

   def DataFrameRow_to_List(self, dfWithOneRow):
      vals = []
      for col in dfWithOneRow:
         vals.append(dfWithOneRow[0:1][col].values[0])
      return vals
   
   def twoLists_to_Dictionary(self, keyList, valueList):
      dict, i = {}, 0
      for key in keyList:
         dict[key] = valueList[i]
         i += 1 
      return dict



if __name__ == "__main__":
   F = Format()
   currencies = [
      "AUD","CAD","CHF","CZK","DKK",
      "EUR","GBP","HKD","HUF","JPY",
      "KRW","NOK","NZD","PLN","SEK",
      "SGD","ZAR"
   ]
   values = [
      1,2,4,8,16,
      32,64,128,256,512,
      1024,2048,4096,8192,16384,
      32768,65536
   ]
   d = F.twoLists_to_Dictionary(currencies, values)
   print(currencies, " - BOUND TO - ", values, " = CREATES = ", d, sep="\n")