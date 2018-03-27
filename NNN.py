from DataWrangler import DataWrangler
from sklearn.ensemble import BaggingRegressor
from sklearn.neural_network import MLPRegressor
import os.path
from sklearn.externals import joblib


class NNN:
	def __init__(self, wrangler):
		self.wrangler = wrangler
		self.setup()

	def setup(self):
		self.regressors = []
		for i in range(len(self.wrangler.getCurrencyList())):
			self.regressors.append(BaggingRegressor(MLPRegressor(solver='lbfgs', hidden_layer_sizes=(150,), momentum=0.9)))

	def train(self):
		self.models = []
		trainData, testData, trainTargetList, testTargetList = self.wrangler.getFormattedDataSplit(1)
		for regressor, targets in zip(self.regressors, trainTargetList):
			self.models.append(regressor.fit(trainData, targets))

	def furtherFit(self, dailyData):
		self.models = []
		lastWindowData = self.wrangler.getLastWindowSizedData()
		for regressor, target in zip(self.regressors, dailyData):
			self.models.append(regressor.fit(lastWindowData, [target]))
		self.wrangler.addDailyData(dailyData)

	def predict(self):
		predicted = []
		lastWindowData = self.wrangler.getLastWindowSizedData()
		for model in self.models:
			predicted.append(model.predict(lastWindowData)[0])
		return predicted

	def saveNNN(self, model):
		if not os.path.exists("NN.pkl"):
                joblib.dump(model, "NN.pkl")

	def loadNNN(self, model):
            model = joblib.load("NN.pkl")

if __name__ == "__main__":
	debug = False
	wrangler = DataWrangler(filePath="data/raw_base_usd.csv", windowSize=2, debug=debug)
	nnn = NNN(wrangler)
	#------------#
	#Train takes about maybe 15 minutes
	nnn.train()
	#------------#
	print(nnn.predict())
	if debug:
		nnn.furtherFit([21,22,23,24])
	else:
		pass
	print(nnn.predict())
	print("------")
	print(wrangler.getOriginalData())
	
