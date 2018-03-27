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

wrangler = DataWrangler(windowSize=14)
nnn = NNN(wrangler)
nnn.train(0.7)
testData = wrangler.loadTestData()
manager = TransactionManager(initialInvestment=(day0, 0.40))
bss = BuySellStay(aggressiveness = 300.0)

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