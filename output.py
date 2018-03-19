def as_single_prediction(pred_list, sep = "  ",front_spacing = ""):
   str = "PREDICTION\n" + front_spacing
   for elem in pred_list:
      str += "{:.5f}{}".format(elem, sep)
   print(str)




if __name__ == "__main__":
   output.as_single_prediction([1.233, 245.23423])
