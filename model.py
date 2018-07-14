import math
import example


class Model:
	def __init__(self, flag="info_gain"):
		self.flag = flag
		self.data_list = []
		
	@staticmethod
	def entropy(example_list):
		total = len(example_list)
		flag_name = []
		flag_list = []
		for example in example_list:
			if example.flag in flag_name:
				flag_list[flag_name.index(example.flag)] += 1
			else:
				flag_name.append(example.flag)
				flag_list.append(1)
		# flags = zip(flag_name, flag_list)
		result = 0
		try:
			for num in flag_list:
				pk = float(num/total)
				result -= pk*math.log2(pk)
		except ZeroDivisionError:
			print("empty list!")
		return result
	
	@staticmethod
	def gain(example_list, a):          # 第a个属性的信息增益
		length = len(example_list)
		if length == 0:
			return False
		temp_list = []
		for example in example_list:
			if example.data[a] in temp_list:
				continue
			else:
				temp_list.append(example.data[a])
		num = len(temp_list)
		final_list = [[] for i in range(num)]
		for example in example_list:
			for i in range(num):
				if example.data[a] == temp_list[i]:
					final_list[i].append(example)
					break
		temp_result = 0
		for lis in final_list:
			temp_result -= float(len(lis)/length) * Model.entropy(lis)
		return Model.entropy(example_list) + temp_result
	
	@staticmethod
	def gain_ratio(example_list, a):
		length = len(example_list)
		if length == 0:
			return False
		temp_list = []
		for example in example_list:
			if example.data[a] in temp_list:
				continue
			else:
				temp_list.append(example.data[a])
		num = len(temp_list)
		final_list = [[] for i in range(num)]
		for example in example_list:
			for i in range(num):
				if example.data[a] == temp_list[i]:
					final_list[i].append(example)
					break
		temp_result = 0
		for lis in final_list:
			temp_result -= float(len(lis) / length) * Model.entropy(lis)
		Gain = Model.entropy(example_list) + temp_result
		IV_result = 0
		for lis in final_list:
			IV_result -= float(len(lis) / length) * math.log2(float(len(lis) / length))
		try:
			IV = float(Gain / IV_result)
		except ZeroDivisionError:
			return 0
		return IV
	
	@staticmethod
	def gini(example_list):
		total = len(example_list)
		flag_name = []
		flag_list = []
		for example in example_list:
			if example.flag in flag_name:
				flag_list[flag_name.index(example.flag)] += 1
			else:
				flag_name.append(example.flag)
				flag_list.append(1)
		# flags = zip(flag_name, flag_list)
		result = 1
		try:
			for num in flag_list:
				pk = float(num / total)
				result -= pk**2
		except ZeroDivisionError:
			print("empty list!")
		return result
	
	@staticmethod
	def gini_index(example_list, a):
		length = len(example_list)
		if length == 0:
			return False
		temp_list = []
		for example in example_list:
			if example.data[a] in temp_list:
				continue
			else:
				temp_list.append(example.data[a])
		num = len(temp_list)
		final_list = [[] for i in range(num)]
		for example in example_list:
			for i in range(num):
				if example.data[a] == temp_list[i]:
					final_list[i].append(example)
					break
		temp_result = 0
		for lis in final_list:
			temp_result += float(len(lis) / length) * Model.gini(lis)
		return temp_result
	
	def initialize(self, filename):
		with open(filename, "r") as fi:
			temp_list = fi.readlines()
		for line in temp_list:
			line_list = line.split(",")
			self.data_list.append(example.Data(line_list[1:-1], flag=line_list[0]))
			
	def find_node(self, list_input, flag=None):
		if not flag:
			flag = self.flag
		list_handle = list_input.copy()
		dimension = list_handle[0].data.size
		if flag == "info_gain": # 信息增益
			list_entropy = []
			for i in range(dimension):
				list_entropy.append(Model.gain(list_handle, i))
			node_index = list_entropy.index(max(list_entropy))
			return list_handle, node_index
		elif flag == "gain_ratio":     # 增益率
			list_gain = []
			for i in range(dimension):
				list_gain.append(Model.gain_ratio(list_handle, i))
			node_index = list_gain.index(max(list_gain))
			return list_handle, node_index
		elif flag == "gini_index":     # 基尼指数
			list_gini = []
			for i in range(dimension):
				list_gini.append(Model.gini_index(list_handle, i))
			node_index = list_gini.index(min(list_gini))
			return list_handle, node_index
		else:
			return False
	
	"""
	@staticmethod
	def generate(data_list, str):
		if data_list.__len__() == 0:
		
		flag_temp = data_list[0].flag
		standard0 = True
		for example in data_list:
			if example.flag != flag_temp:
				standard0 = False
				break
		if standard0:
			return str[:-2]
	"""
		
	


if __name__ == "__main__":
	model = Model()
	filename = "./mushroom/agaricus-lepiota.data"
	model.initialize(filename)
	print(model.find_node(model.data_list, flag="gini_index")[1])