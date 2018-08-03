import random


def divide(filename):
	with open(filename, "r") as fi:
		line_list = fi.readlines()
	f1 = open("../car/train.txt", "w+")
	f2 = open("../car/test.txt", "w+")
	for line in line_list:
		temp = random.uniform(0, 1)
		print(temp)
		if float(temp) > 0.4:
			f2.write(line)
		else:
			f1.write(line)
	f1.close()
	f2.close()
	
	
if __name__ == "__main__":
	divide("../car/data.dat")