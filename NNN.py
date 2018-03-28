from dataWrangler import DataWrangler
from sklearn.ensemble import BaggingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import os.path

class NNN:
	def __init__(self, wrangler):
		self.wrangler = wrangler
		self.setup()

	def setup(self):
		self.regressors = []
		for i in range(len(self.wrangler.getCurrencyList())):
			self.regressors.append(BaggingRegressor(MLPRegressor(solver='lbfgs', hidden_layer_sizes=(130,), momentum=0.9)))

	def individualTrain(self, regressor, trainData, targets):
		return regressor.fit(trainData, targets)

	def train(self, trainSize=1):
		self.models = []
		if os.path.exists("NNN.pkl"):
			self.loadNNN()
		else:
			trainData, testData, trainTargetList, testTargetList = self.wrangler.getFormattedDataSplit(trainSize)
			for regressor, targets in zip(self.regressors, trainTargetList):
				self.models.append(regressor.fit(trainData, targets))
			self.saveNNN()

	def furtherFit(self, dailyData):
		self.models = []
		lastWindowData = self.wrangler.getLastWindowSizedData()
		print("\t:", lastWindowData)
		for regressor, target in zip(self.regressors, dailyData):
			self.models.append(regressor.fit(lastWindowData, [target]))
		self.wrangler.addDailyData(dailyData)

	def predict(self):
		predicted = []
		lastWindowData = self.wrangler.getLastWindowSizedData()
		for model in self.models:
			predicted.append(model.predict(lastWindowData)[0])
		return predicted

	def smartPredict(self, dailyData):
		self.furtherFit(dailyData)
		return self.predict()

	def saveNNN(self):
		joblib.dump(self.models, "NNN.pkl")

	def loadNNN(self):
		self.models = joblib.load("NNN.pkl")

if __name__ == "__main__":
	wrangler = DataWrangler(14)
	nnn = NNN(wrangler)
	nnn.train(0.9)
	
