import numpy as np


class Data:
	def __init__(self, data, flag=None, prediction=None):
		self.data = np.array(data, dtype=np.str_)
		if flag.endswith("\n"):
			flag = flag[:-1]
		self.flag = flag
		self.prediction = prediction
	
	def find_branch(self, branch_list):
		return_list = []
		for branch in branch_list:
			temp_flag = True
			for i in range(len(branch)-1):
				temp = branch[i].split(":")
				if not self.data[int(temp[0])] == temp[1]:
					temp_flag = False
					break
			if temp_flag:
				return_list.append(branch)
		try:
			self.prediction = max(return_list)[-1]
		except ValueError:
			self.prediction = "unpredictable"
		

