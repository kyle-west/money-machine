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

allCurrencies = ["AUD","CAD","CHF","CZK","DKK","EUR","GBP","HKD","HUF","JPY","KRW","NOK","NZD","PLN","SEK","SGD","ZAR"]
fiveCurrencies = ["EUR","GBP","JPY","NZD","CAD"]
fourCurrencies = ["EUR","GBP","JPY","NZD"]
threeCurrencies = ["EUR","GBP","JPY"]
twoCurrencies = ["EUR", "JPY"]
oneCurrencies = ["GBP"]

SETTINGS = {
   "WINDOW-SIZE": 4,
   "CURRENCIES": threeCurrencies,
   "INIT-INVESTMENT": 0.40,
   "BSS-aggressiveness": 80.0,
   "BSS-threshold": .02,
   "NNN-batchPredict-period": 100
}

print("SPLITTING DATA")
#IF YOU CHANGE ANYTHING HERE, YOU MUST RETRAIN NNN
wrangler = DataWrangler(windowSize=SETTINGS["WINDOW-SIZE"], 
      						currencyList=SETTINGS["CURRENCIES"], 
      						trainSize=0.9) #Automatically loads currentData.csv if it exists instead of raw_base_usd.csv
nnn = NNN(wrangler, useEnsemble=True)

print("TRAINING")
nnn.train() #Automatically uses .pkl if it exists
#nnn.trainWithoutPkl()

testData = wrangler.getTestData()
i, num_rows = 1, (testData.shape[0]-3)
day0 = F.DataFrameRow_to_Dictionary(testData[(i-1):i])
lastDay = F.DataFrameRow_to_Dictionary(testData[(i+num_rows+1):(i+num_rows+2)])
manager = TransactionManager(initialInvestment=(day0, SETTINGS["INIT-INVESTMENT"]), heartBeat=True)
bss = BuySellStay(aggressiveness = SETTINGS["BSS-aggressiveness"], threshold = SETTINGS["BSS-threshold"])

print("PREDICTING & TRADING")
predictions = {"EUR":[],"GBP":[],"JPY":[]}
for i in range(i, (i+num_rows+1)):
   row = testData[i:(i+1)]
   #print(row.get_values())
   prediction = F.twoLists_to_Dictionary(
      wrangler.getCurrencyList(), 
      #nnn.predict()
      #nnn.smartPredict(row.get_values()[0])
      nnn.batchPredict(row.get_values()[0], period = SETTINGS["NNN-batchPredict-period"]) #This predict does furtherfit every 100 Heartbeats
      #nnn.trainAllEverytimePredict(row.get_values()[0])
   )
   predictions["EUR"].append(prediction["EUR"])
   predictions["GBP"].append(prediction["GBP"])
   predictions["JPY"].append(prediction["JPY"])
   row = F.DataFrameRow_to_Dictionary(row)
   actions = bss.getActions(row, prediction)
   manager.makeTransactions(actions, row)

manager.sellAll(lastDay)
manager.report()

manager.plotFundHistory(specs=SETTINGS, showStats=True)


# Shows the prediction values
# import matplotlib.pyplot as plt
# import pandas

# data = pandas.DataFrame(predictions)
# # data  = (data - data.mean()) / (data.max() - data.min())
# selections = [
#    "EUR","GBP"
# ]
# data = data[selections]
# labels = []
# for cur, mark in zip(data,['r', 'b', 'g']):
#    col = data[cur].values
#    lab, = plt.plot(range(0,len(col)), col, mark)
#    labels.append(lab)

# plt.ylabel('$ Value in USD')
# plt.xlabel('Transaction Number')
# plt.title('Predictions of ' + str(selections))
# plt.legend(labels, selections)
# print(data)
# plt.show()