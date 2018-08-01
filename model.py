import math
import example
import copy


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
			self.data_list.append(example.Data(line_list[0:-1], flag=line_list[-1]))
			
	def find_node(self, list_input, flag=None):
		if not flag:
			flag = self.flag
		list_handle = copy.deepcopy(list_input)
		dimension = list_handle[0].data.size
		if flag == "info_gain": # 信息增益
			list_entropy = []
			for i in range(dimension):
				list_entropy.append(Model.gain(list_handle, i))
			node_index = list_entropy.index(max(list_entropy))
			for example in list_handle:
				example.data[node_index] = None
			return list_handle, node_index
		elif flag == "gain_ratio":     # 增益率
			list_gain = []
			for i in range(dimension):
				list_gain.append(Model.gain_ratio(list_handle, i))
			node_index = list_gain.index(max(list_gain))
			for example in list_handle:
				example.data[node_index] = None
			return list_handle, node_index
		elif flag == "gini_index":     # 基尼指数
			list_gini = []
			for i in range(dimension):
				list_gini.append(Model.gini_index(list_handle, i))
			node_index = list_gini.index(min(list_gini))
			for example in list_handle:
				example.data[node_index] = None
			return list_handle, node_index
		else:
			return False

	def generate(self, data_list, string, final_list, flag=None):
		# 生成节点node
		if data_list.__len__() == 0:
			return False
		temp_flag = data_list[0].flag
		temp_status = True
		for data in data_list:
			if data.flag != temp_flag:
				temp_status = False
				break
		if temp_status:
			final_list.append(string + temp_flag)
			return True
		temp_data = data_list[0]
		label_list = []
		num_list = []
		temp_status = True
		for ele in temp_data.data:
			if ele:
				temp_status = False
				break
		if temp_status:         # 不考虑D中样本在A上取值相同
			for data in data_list:
				if data.flag in label_list:
					num_list[label_list.index(data.flag)] += 1
				else:
					label_list.append(data.flag)
					num_list.append(1)
			max_num = max(num_list)
			final_list.append(string+label_list[num_list.index(max_num)])
			return True
		
		# 从A中找到最优划分属性a*
		new_list, node_index = self.find_node(data_list, flag)
		new_set = []
		class_list = []
		for index in range(new_list.__len__()):
			if data_list[index].data[node_index] == "?":        # 为？的样本暂时丢弃
				continue
			elif data_list[index].data[node_index] in class_list:
				new_set[class_list.index(data_list[index].data[node_index])].append(new_list[index])
			else:
				new_set.append([new_list[index]])
				class_list.append(data_list[index].data[node_index])
		return_status = True
		for list_index in range(new_set.__len__()):

			temp_status = self.generate(new_set[list_index], string+str(node_index)+":"+class_list[list_index]+"->",final_list, flag)
			return_status &= temp_status
		if not return_status:
			for data in data_list:
				if data.flag in label_list:
					num_list[label_list.index(data.flag)] += 1
				else:
					label_list.append(data.flag)
					num_list.append(1)
			max_num = max(num_list)
			final_list.append(string+label_list[num_list.index(max_num)])
		return True
		

if __name__ == "__main__":
	model = Model()
	filename = "./car/data.dat"
	model.initialize(filename)
	print(model.find_node(model.data_list, flag="gini_index")[1])
	print(model.data_list[0].data, model.data_list[0].flag)
	print("start!")
	tree_list = []
	model.generate(model.data_list, "", tree_list)
	with open("tree.txt", "w+") as fi:
		fi.write("".join(tree_list))
