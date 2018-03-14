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

print ("LOADING DATASET")
data = pandas.read_csv('./data/raw_base_usd.csv', header=0)
data = data[['EUR', 'CAD']] # filter out the unwanted currencies
print(data.head())


########################################################################
# Train on our dataset
########################################################################
print("BEGIN TRAINING")

NN = MLPRegressor(
   hidden_layer_sizes=(10,2),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
   learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=1000, shuffle=True,
   random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
   early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08
)

model = NN.fit(data[:-1], data.shift(-1)[:-1])