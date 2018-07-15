import pdb


if __name__ == '__main__':
	
	num1 = 2000
	num2 = 3000

	real_range = list(range(max(num1,num2+1)))[num1:]

	for k in real_range:
		num_k = str(k)
		if all([int(sl)%2 == 0 for sl in  num_k]):
			print(num_k+', ')

