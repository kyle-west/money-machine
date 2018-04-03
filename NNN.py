from dataWrangler import DataWrangler
from sklearn.ensemble import BaggingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
import os.path
import pandas as pd

class NNN:
	def __init__(self, wrangler, useEnsemble):
		self.wrangler = wrangler
		self.counter = 0
		self.added = []
		self.setup(useEnsemble)

	def setup(self, useEnsemble):
		self.regressors = []
		for i in range(len(self.wrangler.getCurrencyList())):
			mlp = MLPRegressor(hidden_layer_sizes=130, activation='logistic', solver='adam',
				               alpha=.001, batch_size='auto', learning_rate='constant',
				               learning_rate_init=.01, max_iter = 10000, shuffle=False, random_state=None,
				               momentum=0.9)
			if useEnsemble:
				self.regressors.append(BaggingRegressor(mlp))
			else:
				self.regressors.append(mlp)

	def train(self):
		self.models = []
		if os.path.exists("NNN.pkl"):
			self.loadNNN()
		else:
			i = 0
			trainData, trainTargetList = self.wrangler.getFormattedTrainDataAndTargets()
			for regressor, targets in zip(self.regressors, trainTargetList):
				self.models.append(regressor.fit(trainData, targets))
				print("[NNN] Trained " + str(i))
				i += 1
			self.saveNNN()

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

	def smartPredict(self, dailyData):
		self.furtherFit(dailyData)
		return self.predict()

	#-------------
	# Used only with batchPredict
	#-------------
	def specialFit(self):
		self.models = []
		data, targets = self.wrangler.formatData(pd.DataFrame(self.added))
		i = 0
		for regressor, target in zip(self.regressors, targets):
			self.models.append(regressor.fit(data, target))
			print("[NNN] Special Further Fitted " + str(i))
			i += 1

	#--------------
	# Update Every 100
	#--------------
	def batchPredict(self, dailyData, period = 100):
		if (self.counter == period):
			self.specialFit()
			self.added = []
			self.counter = 0
		self.counter += 1
		self.added.append(dailyData)
		self.wrangler.addDailyData(dailyData)
		return self.predict()

	def trainWithoutPkl(self):
		i = 0
		trainData, trainTargetList = self.wrangler.getFormattedTrainDataAndTargets()
		for regressor, targets in zip(self.regressors, trainTargetList):
			self.models.append(regressor.fit(trainData, targets))
			print("[NNN] Trained " + str(i))
			i += 1

	def trainAllEverytimePredict(self, dailyData):
		self.wrangler.addDailyDataToTrainData(dailyData)
		self.wrangler.addDailyData(dailyData)
		self.trainWithoutPkl()
		return self.predict()

	def saveNNN(self):
		joblib.dump(self.models, "NNN.pkl")

	def loadNNN(self):
		self.models = joblib.load("NNN.pkl")

if __name__ == "__main__":
	pass
	
