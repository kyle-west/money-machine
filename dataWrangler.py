import pandas as pd
import numpy as np
import os.path

class DataWrangler:
	def __init__(self, windowSize, debug=False):
		self.windowSize = windowSize
		self.currencyList = ["AUD","CAD","CHF","CZK","DKK","EUR","GBP","HKD","HUF","JPY","KRW","NOK","NZD","PLN","SEK","SGD","ZAR"]
		self.setup(debug)

	def setup(self, debug):
		if os.path.exists("data/currentData.csv"):
			self.originalData = pd.read_csv("data/currentData.csv", header=0)
		else:
			self.originalData = pd.read_csv("data/raw_base_usd.csv", header=0)
		self.originalData = self.originalData[self.currencyList]
		if debug:
			self.originalData = pd.DataFrame([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]])
		self.reformatData()

	def reformatData(self):
		dataRowCount = len(self.originalData)
		dataColCount = len(self.originalData.columns)
		rowCount = dataRowCount - self.windowSize
		colCount = dataColCount * self.windowSize
		self.data = np.empty(shape=[rowCount, colCount])
		self.targets = np.empty(shape=[dataColCount, rowCount])
		for index, row in self.originalData.iterrows():
			if (index + self.windowSize >= dataRowCount):
				break
			for i in range(self.windowSize):
				row = self.originalData.iloc[[index + i]].get_values()
				for j in range(dataColCount):
					self.data[index][(i * dataColCount) + j] = row[0][j]
			targetRow = self.originalData.iloc[[index + self.windowSize]].get_values()
			for i in range(dataColCount):
				self.targets[i][index] = targetRow[0][i]

	def addDailyData(self, dailyData):
		self.originalData = self.originalData.append(pd.DataFrame(np.atleast_2d(dailyData)), ignore_index=True)
		self.saveOriginalData()

	def saveOriginalData(self):
		self.originalData.to_csv("data/currentData.csv", index=False)

	def getLastWindowSizedData(self):
		return np.atleast_2d(np.ravel(self.originalData.tail(self.windowSize)))

	def getOriginalData(self):
		return self.originalData

	def getFormattedDataSplit(self, trainSize):
		splitData = np.split(self.data, [int(trainSize * len(self.data))])
		trainData = splitData[0]
		testData = splitData[1]
		trainTargetList = []
		testTargetList = []
		for i in range(len(self.targets)):
			splitTargets = np.split(self.targets[i], [int(trainSize * len(self.targets[i]))])
			trainTargetList.append(splitTargets[0])
			testTargetList.append(splitTargets[1])
		return trainData, testData, trainTargetList, testTargetList

	def getWindowSize(self):
		return self.windowSize

	def getCurrencyList(self):
		return self.currencyList

if __name__ == "__main__":
	wrangler = DataWrangler(2, False)
	print(wrangler.getOriginalData().head())
	wrangler.saveOriginalData()

	wrangler2 = DataWrangler(2, False)
	print(wrangler2.getOriginalData().head())


'''
	X_train, X_test, y_train_list, y_test_list = wrangler.getFormattedDataSplit(0.7)

	print("Original Data")
	print(wrangler.getOriginalData())

	print("X_train")
	print(X_train)

	print("X_test")
	print(X_test)

	print("y_train_list")
	for i in range(len(y_train_list)):
		print(y_train_list[i])

	print("y_test_list")
	for i in range(len(y_test_list)):
		print(y_test_list[i])

	print("LastWindowSizedData")
	print(wrangler.getLastWindowSizedData())'''