import example


class Test:
	def __init__(self):
		self.data_list = []
		self.model = []
		
	def initialize(self, filename):
		with open(filename, "r") as fi:
			temp_list = fi.readlines()
		for line in temp_list:
			line_list = line.split(",")
			self.data_list.append(example.Data(line_list[0:-1], flag=line_list[-1]))
	
	def init_model(self, model_file):
		with open(model_file, "r") as fi:
			temp_list = fi.readlines()
		for line in temp_list:
			if line.endswith("\n"):
				line = line[:-1]
			self.model.append(line.split("->"))
	
	def cal_accuracy(self):
		correct = 0
		total = 0
		for data in self.data_list:
			data.find_branch(self.model)
			print("flag:"+data.flag, "predict:"+data.prediction)
			if data.flag == data.prediction:
				correct += 1
				total += 1
			else:
				total += 1
		return float(correct/total)


if __name__ == "__main__":
	test = Test()
	test.initialize("./car/data.dat")
	test.init_model("tree.txt")
	print(test.cal_accuracy())