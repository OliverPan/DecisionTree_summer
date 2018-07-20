import numpy as np


class Data:
	def __init__(self, data, flag=None, prediction=None):
		self.data = np.array(data, dtype=np.str_)
		self.flag = flag
		self.prediction = prediction
