import pandas as pd
import numpy as np

class DataWrangler:
	def __init__(self, filePath, windowSize, trainRatio):
		self.windowSize = windowSize
		self.trainRatio = trainRatio
		self.setup(filePath)

	def setup(self, filePath):
		self.originalData = pd.read_csv(filePath, header=0)
		self.originalData = self.originalData[["AUD","CAD","CHF","CZK","DKK","EUR","GBP","HKD","HUF","JPY","KRW","NOK","NZD","PLN","SEK","SGD","ZAR"]]
		self.reformatData()

	def reformatData(self):
		dataRowCount = len(self.originalData)
		dataColCount = len(self.originalData.columns)
		rowCount = dataRowCount - self.windowSize
		colCount = dataColCount * self.windowSize
		data = np.empty(shape=[rowCount, colCount])
		targets = np.empty(shape=[rowCount, dataColCount])
		for index, row in self.originalData.iterrows():
			if (index + self.windowSize >= dataRowCount):
				break
			for i in range(self.windowSize):
				row = self.originalData.iloc[[index + i]].get_values()
				for j in range(dataColCount):
					data[index][(i * dataColCount) + j] = row[0][j]
			targetRow = self.originalData.iloc[[index + self.windowSize]].get_values()
			for i in range(dataColCount):
				targets[index][i] = targetRow[0][i]
		self.splitData(data, targets)

	def splitData(self, data, targets):
		splitData = np.split(data, [int(self.trainRatio * len(data))])
		splitTargets = np.split(targets, [int(self.trainRatio * len(targets))])
		self.X_train = splitData[0]
		self.X_test = splitData[1]
		self.y_train = splitTargets[0]
		self.y_test = splitTargets[1]

	def getOriginalData(self):
		return self.originalData

	def getSplitData(self):
		return self.X_train, self.X_test, self.y_train, self.y_test

	def getWindowSize(self):
		return self.windowSize
