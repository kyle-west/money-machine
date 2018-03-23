########################################################################
#
# Transaction Manager
#
# Take a list of currencies and trading data from the BSS Machine. 
# Carries out actions and manges money on a paper trading account. 
#
########################################################################

import matplotlib.pyplot as plt


########################################################################
# Inupt rows are ordered: 
#     (CURRENCY, PREDICTED_VALUE, MAGNITUDE, BUY_SELL_STAY)
# these constants allow us to access those by index, in a modular way
########################################################################
_CUR_ = 0
_VAL_ = 1
_MAG_ = 2
_BSS_ = 3



########################################################################
# TransactionManager Class 
########################################################################
class TransactionManager:
   #====================================================================
   # Constructor, initializes parameter values
   #====================================================================
   def __init__(self, initialInvestment = None, debug = False):
      self.totalFunds = 100000.0
      self.purchaseCap = 250.0
      self.currentShares = {}
      self.history = [self.totalFunds]
      self.debug = debug
      self.recording = True

      if debug: self.report()

      if initialInvestment:
         half = (self.totalFunds * initialInvestment[1]) // 1 
         portionSize = half // len(initialInvestment[0])
         self.invest(initialInvestment[0], portionSize)

   #====================================================================
   # Make a flat-rate investment in a series of stocks
   #====================================================================
   def invest(self, currentValues, portionSize):
      self.recordState(-1)
      for currency, value in currentValues.items():
         self.buy((currency,), currentValues, portionSize // value)
      self.recordState(1)

   #====================================================================
   # Given a list of BSS Transaction, Buy and Sell as indicated
   #====================================================================
   def makeTransactions(self, currencyPredictionList, currentValues):
      buy_list =  [x for x in currencyPredictionList if x[_BSS_] == "BUY"]
      sell_list = [x for x in currencyPredictionList if x[_BSS_] == "SELL"]
      stay_list = [x for x in currencyPredictionList if x[_BSS_] == "STAY"]

      for currency in sell_list: self.sell(currency, currentValues)
      for currency in buy_list:  self.buy(currency,  currentValues)

   #====================================================================
   # Calculates the number of shares to buy based on allocated funds
   #====================================================================
   def buy(self, currency, currentValues, shares = None):
      if not shares:
         shares = abs(currency[_MAG_] * (self.totalFunds / self.purchaseCap))
         shares = shares // currency[_VAL_]
         shares = min(shares, self.purchaseCap)
      
      if self.debug: print("Buying {} units of {}".format(shares, currency[_CUR_]))
      if currency[_CUR_] in self.currentShares:
         self.currentShares[currency[_CUR_]] += shares
      else:
         self.currentShares[currency[_CUR_]] = shares
      
      self.totalFunds -= shares * currentValues[currency[_CUR_]]
      self.recordState()

   #====================================================================
   # Sells a given percentage of shares for a certain currency
   #====================================================================
   def sell(self, currency, currentValues):
      if currency[_CUR_] in self.currentShares:
         shares = abs((currency[_MAG_] * self.currentShares[currency[_CUR_]])//1)
         if self.debug: print("Selling {} units of {}".format(shares, currency[_CUR_]))
         self.currentShares[currency[_CUR_]] -= shares
         self.totalFunds += shares * currentValues[currency[_CUR_]]
         self.recordState()
   
   #====================================================================
   # Sell everything share we own at the current values
   #====================================================================
   def sellAll(self, currentValues):
      self.recordState(-1)
      for cur in self.currentShares:
         self.sell((cur, None, 1, None), currentValues)
      self.recordState(1)

   #====================================================================
   # Print a simple report to the screen of what we own
   #====================================================================
   def report(self):
      print("TOTAL FUNDS:", self.totalFunds, sep = "\t")
      print("TOTAL PROFIT:", self.totalFunds - self.history[0], sep = "\t")
      print("SHARES HELD:", self.currentShares, "", sep = "\n")

   #====================================================================
   # Show a plot to report the changing values of the system
   #====================================================================
   def plotFundHistory(self, showEachTransaction=False):
      print("GENERATING PLOT...")
      plt.plot(range(0,len(self.history)), self.history)
      if showEachTransaction:
         plt.plot(range(0,len(self.history)), self.history, 'ro')
      plt.ylabel('$ Value in USD')
      plt.xlabel('Transaction Number')
      plt.show()

   #====================================================================
   # Push the current financial history if recording
   # {quiet} - (-1|1) pause recording with -1, start again with 1
   #====================================================================
   def recordState(self, quiet = 0):
      if (quiet != 0):
         self.recording = (quiet > 0)
      if self.recording:
         self.history.append(self.totalFunds)





########################################################################
# Test out our class
########################################################################
if __name__ == "__main__":

   from mock.MockNN import MockNN
   from BuySellStay import BuySellStay
   from Format      import Format
   import pandas

   F = Format()

   print("LOADING DATASET")
   # read in file data opt in which curencies we care about
   data = pandas.read_csv('data/raw_base_usd.csv', header=0)
   data = data[[
      "AUD","CAD","CHF","CZK","DKK",
      "EUR","GBP","HKD","HUF","JPY",
      "KRW","NOK","NZD","PLN","SEK",
      "SGD","ZAR"
   ]]
   print(data.head())

   print("-----------------------------------------------")
   NN = MockNN(debug=True)
   NN.fit(data)

   print("-----------------------------------------------")
   i, num_rows = 4500, 500
   testRows = data[i:(i+num_rows+1)]
   day0 = F.DataFrameRow_to_Dictionary(data[(i-1):i])
   lastDay = F.DataFrameRow_to_Dictionary(data[(i+num_rows+1):(i+num_rows+2)])
   
   manager = TransactionManager(initialInvestment=(day0, 0.40))
   bss = BuySellStay()
   
   print("TRADING")

   for i in range(i, (i+num_rows+1)):
      row = data[i:(i+1)]
      prediction = F.DataFrameRow_to_Dictionary(NN.predict(row))
      row = F.DataFrameRow_to_Dictionary(row)
      actions = bss.getActions(row, prediction)
      manager.makeTransactions(actions, row)

   manager.sellAll(lastDay)
   manager.report()
   manager.plotFundHistory()
