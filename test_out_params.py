########################################################################
#
# This script tries out a bunch of changes to the MLP params
#
########################################################################

########################################################################
# load libraries and data
########################################################################
from sklearn.neural_network import MLPRegressor
import pandas
import output
import math

print("LOADING DATASET")
data = pandas.read_csv('./data/raw_base_usd.csv', header=0)

# opt in which curencies we care about
data = data[[
   "AUD","CAD","CHF","CZK","DKK",
   "EUR","GBP","HKD","HUF","JPY",
   "KRW","NOK","NZD","PLN","SEK",
   "SGD","ZAR"
]] 


def calcError(actual, predictions):
   diff = 0
   for act, pred in zip(actual, predictions):
      diff += act - pred
   return abs(diff / len(actual))

def findSmallestErrorInRecords(records):
   smallest = math.inf
   smallest_record = None
   for rec in records:
      if (rec[2] < smallest):
         smallest_record = rec
         smallest = rec[2]
   return smallest_record

########################################################################
# Train on our dataset
########################################################################
print("BEGIN TRAINING TESTS")

TEST_SIZE = 1
TRAINING_SLICE = slice(0,-(TEST_SIZE + 1))
TEST_SLICE = slice(-(TEST_SIZE + 1), -1)

records = []
numTrys = 3

for layer_size in range(80, 141, 5):
   for iteration_size in [1000, 10000, 100000, 1000000]: # range(1000, 100001, 1000):
      error = 0.0
      for trial in range(0, numTrys):
         NN = MLPRegressor(
            hidden_layer_sizes=(layer_size,),  activation='logistic', solver='adam', 
            alpha=0.001, batch_size='auto', learning_rate='constant', 
            learning_rate_init=0.01, max_iter=iteration_size, shuffle=False,
            random_state=None, warm_start=False, momentum=0.9
         )
         model = NN.fit(data[TRAINING_SLICE], data.shift(-1)[TRAINING_SLICE])
         predictions = model.predict(data[TEST_SLICE])
         actual = data[-1:]
         error += calcError(actual.values[0], predictions[0])
      record = (layer_size, iteration_size, error/numTrys)
      records.append(record)
      print(record)

smallest = findSmallestErrorInRecords(records)

print("PARAMS WITH LOWEST ERROR", smallest)