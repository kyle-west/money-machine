########################################################################
#
# This script runs our main algorithms and processes.
#
########################################################################

########################################################################
# load libraries and data
########################################################################
from DataWrangler import DataWrangler
from Format import Format
from TransactionManager import TransactionManager
from BuySellStay import BuySellStay
from NNN import NNN

F = Format()

print("SPLITTING DATA")
#IF YOU CHANGE ANYTHING HERE, YOU MUST RETRAIN NNN
wrangler = DataWrangler(windowSize=10, 
      						currencyList=["AUD","CAD","CHF","CZK","DKK","EUR","GBP","HKD","HUF","JPY","KRW","NOK","NZD","PLN","SEK","SGD","ZAR"], 
      						trainSize=0.9) #Automatically loads currentData.csv if it exists instead of raw_base_usd.csv
nnn = NNN(wrangler, useEnsemble=True)

print("TRAINING")
nnn.train() #Automatically uses .pkl if it exists

testData = wrangler.getTestData()
i, num_rows = 1, (testData.shape[0]-3)
day0 = F.DataFrameRow_to_Dictionary(testData[(i-1):i])
lastDay = F.DataFrameRow_to_Dictionary(testData[(i+num_rows+1):(i+num_rows+2)])
manager = TransactionManager(initialInvestment=(day0, 0.40), heartBeat=True)
bss = BuySellStay(aggressiveness = 10.0)

print("PREDICTING & TRADING")

for i in range(i, (i+num_rows+1)):
   row = testData[i:(i+1)]
   #print(row.get_values())
   prediction = F.twoLists_to_Dictionary(
      wrangler.getCurrencyList(), 
      #nnn.predict()
      #nnn.smartPredict(row.get_values()[0])
      nnn.batchPredict(row.get_values()[0], period = 100) #This predict does furtherfit every 100 Heartbeats
   )
   row = F.DataFrameRow_to_Dictionary(row)
   actions = bss.getActions(row, prediction)
   manager.makeTransactions(actions, row)

manager.sellAll(lastDay)
manager.report()
manager.plotFundHistory()