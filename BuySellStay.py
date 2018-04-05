########################################################################
#
# Buy Sell Stay
#
# Takes a row of current FOREX values, and a row of predicted values.
# Calculates a mamgitude and computes a trade action. Returns a tupple 
# including relevant data in the following form:
#     (CURRENCY, PREDICTED_VALUE, MAGNITUDE, BUY_SELL_STAY) 
#
########################################################################

from numpy import e
sigmoid = lambda x: 1.0 / (1.0 + e**(-x))

class BuySellStay:
    #===================================================================
    # We don't need to provide a constructor
    #===================================================================
    def __init__(self, aggressiveness = 1.0, threshold = 0.001):
       self.aggressiveness = aggressiveness # how much to buy when we buy
       self.threshold = threshold
    
    #===================================================================
    # Helper function to compute the magnitude and action
    #===================================================================
    def applyRuleset(self, diff):
        magnitude = 0
        influence = 1
        decision = 'STAY'
        if diff < 0.0:       
            influence = -1

        if abs(diff) > self.threshold: 
            
            if diff < 0:
                decision = 'SELL'
                magnitude += sigmoid(diff * self.aggressiveness) 
            else:
                decision = 'BUY'
                magnitude += sigmoid(diff)
                magnitude *= self.aggressiveness

        # boost if large percent change
        if abs(diff) > self.threshold * 10:  
            magnitude += sigmoid(diff) * .25

        return (magnitude * influence), decision

    #===================================================================
    # Returns a list of actions given predictions and current values
    #===================================================================
    def getActions(self, current_data, predicted_data):
        predictions = []
        for name in current_data.keys():
            curr = current_data[name]
            pred = predicted_data[name]
            diff = ((pred - curr)/float(curr))
            mag, decision = self.applyRuleset(diff)
            predictions.append((name, pred, mag, decision))
        return predictions
