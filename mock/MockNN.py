class MockNN:
   def __init__(self, debug=False):
      self.debug = debug
      print("WARINING: Mock Neural Network Being Used")
   
   def fit(self, data):
      self.predictions = data.shift(-1)
      if self.debug:
         print("[MockNN]: Loaded dataset and shifted by one day for predictions")
         print(self.predictions.head())

   def predict(self, data_row):
      return self.predictions[data_row.index._start:data_row.index._stop]