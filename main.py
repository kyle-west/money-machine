########################################################################
#
# This script runs our main algorithms and processes.
#
########################################################################

########################################################################
# load libraries and data
########################################################################
from dataWrangler import DataWrangler
from Format import Format
from TransactionManager import TransactionManager
from BuySellStay import BuySellStay
from NNN import NNN
import pandas as pd

F = Format()

print("SPLITTING DATA")
wrangler = DataWrangler(windowSize=14, save=False)
nnn = NNN(wrangler)

print("TRAINING")
nnn.train(0.9)

testData = wrangler.loadTestData()
i, num_rows = 1, (testData.shape[0]-3)
day0 = F.DataFrameRow_to_Dictionary(testData[(i-1):i])
lastDay = F.DataFrameRow_to_Dictionary(testData[(i+num_rows+1):(i+num_rows+2)])
manager = TransactionManager(initialInvestment=(day0, 0.40), heartBeat=True)
bss = BuySellStay(aggressiveness = 10.0)

print("PREDICTING & TRADING")

for i in range(i, (i+num_rows+1)):
   row = testData[i:(i+1)]
   prediction = F.twoLists_to_Dictionary(
      wrangler.getCurrencyList(), 
      nnn.smartPredict(row.values[0])
   )
   row = F.DataFrameRow_to_Dictionary(row)
   actions = bss.getActions(row, prediction)
   manager.makeTransactions(actions, row)

manager.sellAll(lastDay)
manager.report()
manager.plotFundHistory()