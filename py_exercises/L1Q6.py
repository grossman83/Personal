import pdb

if __name__ == '__main__':
	
	blah = input("type two numbers separate by a , (example: 4,5)")
	strs = blah.split(',')
	ints = [int(k) for k in strs]

	my_list = []
	for i in list(range(ints[0])):
		my_list.append([i*j for j in list(range(ints[1]))])


	pdb.set_trace()
