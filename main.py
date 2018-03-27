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

F = Format()

print("SPLITTING DATA")
wrangler = DataWrangler(windowSize=14)
nnn = NNN(wrangler)

print("TRAINING")
nnn.train(0.9)

testData = wrangler.loadTestData()
#print(testData.head())
i, num_rows = 0, len(testData)
day0 = F.DataFrameRow_to_Dictionary(testData[(i-1):i])
lastDay = F.DataFrameRow_to_Dictionary(testData[(i+num_rows+1):(i+num_rows+2)])
manager = TransactionManager(initialInvestment=(day0, 0.40))
bss = BuySellStay(aggressiveness = 300.0)

print("PREDICTING & TRADING")

for i in range(i, (i+num_rows+1)):
	row = testData[i:(i+1)]
	prediction = F.twoLists_to_Dictionary(wrangler.getCurrencyList(), NN.smartPredict(row.get_values()[0]))
	row = F.DataFrameRow_to_Dictionary(row)
	actions = bss.getActions(row, prediction)
	manager.makeTransactions(actions, row)

manager.sellAll(lastDay)
manager.report()
manager.plotFundHistory()