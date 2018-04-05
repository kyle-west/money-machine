import pandas as pd
import numpy as np
import os.path

class DataWrangler:
	INITIAL_DATAFILE = "data/raw_base_usd.csv"
	DATAFILE = "data/currentData.csv"

	def __init__(self, windowSize, currencyList, trainSize, debug=False):
		self.windowSize = windowSize
		self.currencyList = currencyList
		self.dataToSave = []
		self.setup(trainSize, debug)

	def setup(self, trainSize, debug):
		if debug:
			self.data = pd.DataFrame([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]])
		elif os.path.exists(self.DATAFILE):
			self.data = pd.read_csv(self.DATAFILE, header=0)
		else:
			self.data = pd.read_csv(self.INITIAL_DATAFILE, header=0)
		if not debug:
			self.data = self.data[self.currencyList]
		splitData = np.split(self.data, [int(len(self.data) * trainSize)])
		self.trainData = splitData[0]
		self.testData = splitData[1]

	def getFormattedTrainDataAndTargets(self):
		return self.formatData(self.trainData)

	def formatData(self, data):
		dataRowCount = len(data)
		dataColCount = len(data.columns)
		rowCount = dataRowCount - self.windowSize
		colCount = dataColCount * self.windowSize
		formattedData = np.empty(shape=[rowCount, colCount])
		formattedTargets = np.empty(shape=[dataColCount, rowCount])
		for index, row in data.iterrows():
			if (index + self.windowSize >= dataRowCount):
				break
			for i in range(self.windowSize):
				row = data.iloc[[index + i]].get_values()
				for j in range(dataColCount):
					formattedData[index][(i * dataColCount) + j] = row[0][j]
			targetRow = data.iloc[[index + self.windowSize]].get_values()
			for i in range(dataColCount):
				formattedTargets[i][index] = targetRow[0][i]
		return formattedData, formattedTargets

	def addDailyData(self, dailyData):
		if (len(self.dataToSave) < self.windowSize):
			self.data = self.data.append(pd.DataFrame(np.atleast_2d(dailyData), columns=self.data.columns), ignore_index=True)
		self.dataToSave.append(dailyData)

	def addDailyDataToTrainData(self, dailyData):
		self.trainData = self.trainData.append(pd.DataFrame(np.atleast_2d(dailyData), columns=self.trainData.columns), ignore_index=True)

	def getLastWindowSizedData(self):
		if (len(self.dataToSave) < self.windowSize):
			return np.atleast_2d(np.ravel(self.data.tail(self.windowSize)))
		return np.atleast_2d(np.ravel(self.dataToSave[-self.windowSize:]))

	def getData(self):
		return self.data

	def getTrainData(self):
		return self.trainData

	def getTestData(self):
		return self.testData

	def getWindowSize(self):
		return self.windowSize

	def getCurrencyList(self):
		return self.currencyList

	def saveData(self):
		if (len(self.dataToSave) > self.windowSize):
			self.data = self.data.append(pd.DataFrame(np.atleast_2d(self.dataToSave[self.windowSize:]), columns=self.data.columns), ignore_index=True)
		self.data.to_csv(self.DATAFILE, index=False)


if __name__ == "__main__":
	wrangler = DataWrangler2(windowSize=2, currencyList=[], trainSize=0.7, debug=True)
	print("DATA")
	print(wrangler.getData())
	print("TRAIN DATA")
	print(wrangler.getTrainData())
	print("TEST DATA")
	print(wrangler.getTestData())
	print("FORMATTED DATA")
	trainData, trainTargets = wrangler.getFormattedTrainDataAndTargets()
	print("Train")
	print(trainData)
	print("Targets")
	print(trainTargets)
	print("Last Window Sized Data")
	print(wrangler.getLastWindowSizedData())
	print("Adding 3 daily data rows")
	wrangler.addDailyData([21,22,23,24])
	wrangler.addDailyData([25,26,27,28])
	wrangler.addDailyData([29,30,31,32])
	print("New Last Window Sized Data")
	print(wrangler.getLastWindowSizedData())
	print("Saving data")
	wrangler.saveData()