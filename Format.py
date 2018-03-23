########################################################################
#
# Format
#
# This class is a collection of data formatting functions.
#
########################################################################

class Format:
   def DataFrameRow_to_Dictionary(self, dfWithOneRow):
      dict = {}
      for col in dfWithOneRow:
         dict[col] = dfWithOneRow[0:1][col].values[0]
      return dict