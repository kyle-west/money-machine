class BSS:
    def __init__(self, current_data, predicted_data):
        self.current_data   = current_data
        self.predicted_data = predicted_data
        self.predictions = []
        self.ids = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY'
                   ,'CYP', 'CZK', 'DKK' ,'EEK', 'EUR', 'GBP'
                   ,'HKD', 'HRK', 'HUF' ,'IDR', 'ILS', 'INR'
                   ,'ISK', 'JPY', 'KRW' ,'LTL', 'LVL', 'MTL'
                   ,'MXN', 'MYR', 'NOK' ,'NZD', 'PHP', 'PLN'
                   ,'ROL', 'RON', 'RUB' ,'SEK', 'SGD', 'SIT'
                   ,'SKK', 'THB', 'TRL' ,'TRY', 'ZAR']

    def applyRuleset(self,diff):
        magnitude = 1
        influence = 1
        decision = 'STAY'
        if diff < 0:
            influence = -1
        if abs(diff) > .05:
            magnitude += .25
            if diff < 0:
                decision = 'SELL'
            else:
                decision = 'BUY'
        if abs(diff) > .1:
            magnitude += .25

        return (magnitude * influence), decision

    def decide(self):
        for i in range(len(self.predicted_data)):
            curr = self.current_data[i]
            pred = self.predicted_data[i]
            diff = ((pred - curr)/float(curr))
            mag, decision = self.applyRuleset(diff)
            self.predictions.append((self.ids[i],pred,mag,decision))
        return self.predictions
