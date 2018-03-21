########################################################################
#
# Transaction Manager
#
# Take a list of currencies and trading data from the BSS Machine. 
# Carries out actions and manges money on a paper trading account. 
#
########################################################################



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
   # 
   #====================================================================
   def __init__(self):
      self.total_funds = 100000.0
      self.purchaseCap = 250.0
      self.currentShares = {}


   #====================================================================
   # 
   #====================================================================
   def makeTransactions(self, currency_prediction_list, current_values):
      buy_list =  [x for x in currency_prediction_list if x[_BSS_] == "BUY"]
      sell_list = [x for x in currency_prediction_list if x[_BSS_] == "SELL"]
      stay_list = [x for x in currency_prediction_list if x[_BSS_] == "STAY"]
      
      for currency in sell_list: self.sell(currency, current_values)
      for currency in buy_list:  self.buy(currency,  current_values)


   #====================================================================
   # TODO: refine unit share calculation formula
   #====================================================================
   def buy(self, currency, current_values):
      shares = abs(currency[_MAG_] * (self.total_funds / self.purchaseCap))
      shares = shares // currency[_VAL_]
      shares = min(shares, self.purchaseCap)
      print("Buying {} units of {}".format(shares, currency[_CUR_]))

      if currency[_CUR_] in self.currentShares:
         self.currentShares[currency[_CUR_]] += shares
      else:
         self.currentShares[currency[_CUR_]] = shares
      
      self.total_funds -= shares * current_values[currency[_CUR_]]


   #====================================================================
   # 
   #====================================================================
   def sell(self, currency, current_values):
      if currency[_CUR_] in self.currentShares:
         shares = (currency[_MAG_] * self.currentShares[currency[_CUR_]])//1
         self.currentShares[currency[_CUR_]] -= shares
         self.total_funds += shares * current_values[currency[_CUR_]]
   
   #====================================================================
   # 
   #====================================================================
   def sellAll(self, current_values):
      for cur in self.currentShares:
         self.sell((cur, None, 1, None), current_values)


   #====================================================================
   # 
   #====================================================================
   def report(self):
      print("TOTAL FUNDS:", self.total_funds, sep = "\n")
      print("SHARES HELD:", self.currentShares, sep = "\n")

########################################################################
# Test out our class
########################################################################
if __name__ == "__main__":

   mock_inputs = [
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
   
   today = {
      "AUD": 6.41,
      "CAD": 1.25,
      "CHF": 12.45,
      "CZK": 3.42,
      "DKK": 5.78,
      "EUR": 122.08,
      "GBP": 45.27,
      "HKD": 20.32,
      "HUF": 8.91,
      "JPY": 3.25,
      "KRW": 0.13,
      "NOK": 0.84,
      "NZD": 0.45,
      "PLN": 0.53,
      "SEK": 1.85,
      "SGD": 2.08,
      "ZAR": 3.23
   }

   tomorrow = {
      "AUD": 6.35,
      "CAD": 1.16,
      "CHF": 12.75,
      "CZK": 3.43,
      "DKK": 5.68,
      "EUR": 122.12,
      "GBP": 45.10,
      "HKD": 20.32,
      "HUF": 8.92,
      "JPY": 3.26,
      "KRW": 0.15,
      "NOK": 0.85,
      "NZD": 0.42,
      "PLN": 0.51,
      "SEK": 1.87,
      "SGD": 2.08,
      "ZAR": 3.23
   }

   # print("MOCK INPUTS:", mock_inputs, sep="\n")
   print("-----------------------------------------------")
   
   manager = TransactionManager()
   manager.makeTransactions(mock_inputs, today)
   print("-----------------------------------------------")
   manager.report()

   print("-----------------------------------------------")
   manager.sellAll(tomorrow)
   manager.report()