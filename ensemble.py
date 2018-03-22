########################################################################
# load libraries and data
########################################################################
from sklearn.ensemble import BaggingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn import model_selection
import pandas
import output
import math
import matplotlib.pyplot as plt

print("LOADING DATASET")
data = pandas.read_csv('./data/raw_base_usd.csv', header=0)

# opt in which curencies we care about
data = data[[
   "AUD","CAD","CHF","CZK","DKK",
   "EUR","GBP","HKD","HUF","JPY",
   "KRW","NOK","NZD","PLN","SEK",
   "SGD","ZAR"
]]

########################################################################
# Train on our dataset
########################################################################
TEST_SIZE = 1
TRAINING_SLICE = slice(0,-(TEST_SIZE + 1))
TEST_SLICE = slice(-(TEST_SIZE + 1), -1)

X_Train = data[TRAINING_SLICE]
X_Test = data.shift(-1)[TRAINING_SLICE]

NN = MLPRegressor(hidden_layer_sizes=130, activation='logistic', solver='adam',
                  alpha=.001, batch_size='auto', learning_rate='constant',
                  learning_rate_init=.01, max_iter = 1000, shuffle=False, random_state=None,
                  momentum=.9)

"""model = NN.fit(X_Train, X_Test)

predictions = model.predict(data[TEST_SLICE])

actual = data[-1:]
print(actual.values[0], predictions[0])


plt.plot(predictions[0])
plt.plot(data[-1:].values[0])
plt.ylabel('some numbers')
plt.show()
"""
########################################################################
# Build our ensemble neural nets
########################################################################

# Keep track of our random state
seed = 7

# The number of neural nets we are going to test on??
num_nets = 10

model = BaggingRegressor(base_estimator=NN, n_estimators=num_nets, random_state=seed, n_jobs=-1)

model.fit(X_Train,X_Test)

prediction = model.predict(data[TEST_SLICE])

print(prediction)
