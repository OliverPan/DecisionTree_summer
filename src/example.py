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
		wrong_list = []
		temp_num = 1
		for branch in branch_list:
			temp_flag = True
			i = 1
			for _ in range(len(branch)-1):
				temp = branch[_].split(":")
				if not self.data[int(temp[0])] == temp[1]:
					temp_flag = False
					break
				else:
					i += 1
			if temp_flag:
				return_list.append(branch)
			else:
				if i == temp_num:
					wrong_list.append(branch)
				elif i > temp_num:
					del(wrong_list[:])
					wrong_list.append(branch)
		try:
			self.prediction = max(return_list)[-1]
		except ValueError:
			predict_list =[]
			num_list = []
			for branch in wrong_list:
				if branch[-1] in predict_list:
					num_list[predict_list.index(branch[-1])] += 1
				else:
					predict_list.append(branch[-1])
					num_list.append(1)
			self.prediction = predict_list[num_list.index(max(num_list))]
		

