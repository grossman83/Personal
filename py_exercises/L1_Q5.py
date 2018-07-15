import pdb

class simple_class:
	def __init__(self):
		self.astr = []

	def get_str(self):
		self.astr = input("type again: ")

	def print_str(self):
		print(self.astr)





if __name__ == '__main__':
	blah = simple_class()
	blah.get_str()

	blah.print_str()
	pdb.set_trace()
