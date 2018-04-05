import pandas
import matplotlib.pyplot as plt

data = pandas.read_csv('data/raw_base_usd.csv', header=0)

# ["AUD","CAD","CHF","CZK","DKK","EUR","GBP","HKD","HUF","JPY","KRW","NOK","NZD","PLN","SEK","SGD","ZAR"]
selections = [
   "EUR","GBP","JPY"
]
data = data[selections]

i, num_rows = 4500, 500
data = data[i:(i+num_rows+1)]

data  = (data - data.mean()) / (data.max() - data.min())


labels = []
for cur, mark in zip(data,['r', 'b', 'g']):
   col = data[cur].values
   lab, = plt.plot(range(0,len(col)), col, mark)
   labels.append(lab)

plt.ylabel('$ Value in USD')
plt.xlabel('Transaction Number')
plt.title('Values of ' + str(selections))
plt.legend(labels, selections)
plt.show()