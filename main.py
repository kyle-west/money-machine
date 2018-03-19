########################################################################
#
# This script runs our main algorithms and processes.
#
########################################################################

########################################################################
# load libraries and data
########################################################################
from sklearn.neural_network import MLPRegressor
import pandas
import output

print("LOADING DATASET")
data = pandas.read_csv('./data/raw_base_usd.csv', header=0)

# opt in which curencies we care about
data = data[[
   "AUD","CAD","CHF","CZK","DKK",
   "EUR","GBP","HKD","HUF","JPY",
   "KRW","NOK","NZD","PLN","SEK",
   "SGD","ZAR"
]] 
print(data.head())


########################################################################
# Train on our dataset
########################################################################
print("BEGIN TRAINING")

NN = MLPRegressor(
   hidden_layer_sizes=(130,),  activation='logistic', solver='adam', 
   alpha=0.001, batch_size='auto', learning_rate='constant', 
   learning_rate_init=0.01, max_iter=1000, shuffle=False,
   random_state=None, warm_start=False, momentum=0.9
)

TEST_SIZE = 1
TRAINING_SLICE = slice(0,-(TEST_SIZE + 1))
TEST_SLICE = slice(-(TEST_SIZE + 1), -1)

model = NN.fit(data[TRAINING_SLICE], data.shift(-1)[TRAINING_SLICE])

predictions = model.predict(data[TEST_SLICE])

print('ACUTAL', data[-1:], sep="\n")
pred = pandas.DataFrame(predictions)
pred.columns = data.columns
print("PREDICTIONS",pred, sep = "\n")