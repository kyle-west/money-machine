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
         half = self.totalFunds // 2 
         portionSize = half // len(initialInvestment)
         self.invest(initialInvestment, portionSize)

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
      print("TOTAL FUNDS:", self.totalFunds, sep = "\n")
      print("SHARES HELD:", self.currentShares, "", sep = "\n")

   #====================================================================
   # Show a plot to report the changing values of the system
   #====================================================================
   def plotFundHistory(self):
      print("GENERATING PLOT...")
      plt.plot(range(0,len(self.history)), self.history)
      plt.plot(range(0,len(self.history)), self.history, 'ro')
      plt.ylabel('$ Value in USD')
      plt.xlabel('Transaction Number')
      plt.show()

   #====================================================================
   # Push the current financial histort if recording
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

   # init all our test values 
   BSS_d1 = [
      ("AUD", 6.40, 0.25, "BUY"),
      ("CAD", 1.35, -.53, "SELL"),
      ("CHF", 12.40, 0.78, "STAY"),
      ("CZK", 3.45, -.32, "BUY"),
      ("DKK", 5.62, 0.43, "BUY"),
      ("EUR", 122.01, -.11, "STAY"),
      ("GBP", 45.21, 0.03, "STAY"),
      ("HKD", 20.30, 0.02, "STAY"),
      ("HUF", 8.97, -.09, "BUY"),
      ("JPY", 3.21, 1.00, "BUY"),
      ("KRW", 0.12, -.50, "SELL"),
      ("NOK", 0.78, 0.52, "BUY"),
      ("NZD", 0.46, -.26, "BUY"),
      ("PLN", 0.75, 0.78, "SELL"),
      ("SEK", 1.75, 0.45, "SELL"),
      ("SGD", 2.02, 0.78, "STAY"),
      ("ZAR", 3.56, -.26, "SELL")
   ]

   BSS_d2 = [
      ("AUD", 6.40, 0.25, "STAY"),
      ("CAD", 1.35, -.53, "STAY"),
      ("CHF", 12.42, 0.78, "BUY"),
      ("CZK", 3.45, -.32, "STAY"),
      ("DKK", 5.62, 0.43, "STAY"),
      ("EUR", 119.60, -.25, "SELL"),
      ("GBP", 44.75, 0.25, "SELL"),
      ("HKD", 20.45, 0.02, "BUY"),
      ("HUF", 8.97, -.09, "STAY"),
      ("JPY", 3.21, 1.00, "STAY"),
      ("KRW", 0.12, -.50, "STAY"),
      ("NOK", 0.78, 0.52, "STAY"),
      ("NZD", 0.46, -.26, "STAY"),
      ("PLN", 0.75, 0.78, "STAY"),
      ("SEK", 1.75, 0.45, "STAY"),
      ("SGD", 2.14, 0.78, "SELL"),
      ("ZAR", 3.56, -.26, "STAY")
   ]
   
   # today's inputs (same as given to NNN)
   actual_day_one = {
      "AUD": 6.41, "CAD": 1.25, "CHF": 12.45, "CZK": 3.42, "DKK": 5.78, 
      "EUR": 122.08, "GBP": 45.27, "HKD": 20.32, "HUF": 8.91, "JPY": 3.25, 
      "KRW": 0.13, "NOK": 0.84, "NZD": 0.45, "PLN": 0.53, "SEK": 1.85, 
      "SGD": 2.08, "ZAR": 3.23
   }

   # the actual values of Day 1
   actual_day_two = {
      "AUD": 6.35, "CAD": 1.16, "CHF": 12.75, "CZK": 3.43, "DKK": 5.68, 
      "EUR": 122.12, "GBP": 45.10, "HKD": 20.32, "HUF": 8.92, "JPY": 3.26, 
      "KRW": 0.15, "NOK": 0.85, "NZD": 0.42, "PLN": 0.51, "SEK": 1.87, 
      "SGD": 2.08, "ZAR": 3.23
   }

   # the actual values of Day 2
   actual_day_three = {
      "AUD": 6.36, "CAD": 1.27, "CHF": 12.60, "CZK": 3.45, "DKK": 5.69, 
      "EUR": 122.53, "GBP": 45.25, "HKD": 20.14, "HUF": 8.75, "JPY": 3.25, 
      "KRW": 0.17, "NOK": 0.83, "NZD": 0.75, "PLN": 0.53, "SEK": 1.93, 
      "SGD": 2.06, "ZAR": 3.25
   }

   manager = TransactionManager(initialInvestment=actual_day_one, debug=True)
   manager.report()
   
   print("-----------------------------------------------")
   manager.makeTransactions(BSS_d1, actual_day_one)
   manager.report()

   print("-----------------------------------------------")
   manager.makeTransactions(BSS_d2, actual_day_two)
   manager.report()

   print("-----------------------------------------------")
   manager.sellAll(actual_day_three)
   manager.report()

   print("-----------------------------------------------")
   manager.plotFundHistory()
