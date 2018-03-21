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
   def makeTransactions(self, currency_prediction_list):
      first = currency_prediction_list[0]
      print(first)
      print("We will {} from {}".format(first[_BSS_], first[_CUR_]))
      

   #====================================================================
   # 
   #====================================================================



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
      ("JPY", 3.21, -.13, "BUY"),
      ("KRW", 0.12, -.50, "SELL"),
      ("NOK", 0.78, 0.52, "BUY"),
      ("NZD", 0.46, -.26, "BUY"),
      ("PLN", 0.75, 0.78, "SELL"),
      ("SEK", 1.75, 0.45, "SELL"),
      ("SGD", 2.02, 0.78, "STAY"),
      ("ZAR", 3.56, -.26, "SELL")
   ]
   print("MOCK INPUTS:", mock_inputs, sep="\n")
   print("-----------------------------------------------")
   
   manager = TransactionManager()

   manager.makeTransactions(mock_inputs)
